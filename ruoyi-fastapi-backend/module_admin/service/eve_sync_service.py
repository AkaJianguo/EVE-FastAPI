from datetime import datetime, timedelta
from typing import Any, Optional

import httpx
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from module_admin.entity.do.eve_do import EveAlliance, EveCorporation
from utils.log_util import logger


class EveSyncService:
    """
    EVE/ESI 同步服务：军团与联盟资料
    """

    @classmethod
    async def sync_corporation(cls, query_db: AsyncSession, corp_id: Optional[int]) -> Optional[EveCorporation]:
        """
        同步军团信息（24 小时缓存）。若不存在或超过 24 小时则调用 ESI 更新。
        """

        if not corp_id:
            return None

        corp = await query_db.get(EveCorporation, corp_id)
        if corp and cls.__is_fresh(corp.update_time):
            return corp

        corp_data: dict[str, Any] | None = None
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f'https://esi.evetech.net/latest/corporations/{corp_id}/')
                resp.raise_for_status()
                corp_data = resp.json()
        except Exception as e:  # noqa: BLE001
            logger.warning(f'同步军团信息失败，corp_id={corp_id}: {e}')
            return corp

        record = cls.__build_corp_record(corp_id, corp_data)
        await cls.__upsert_corporation(query_db, record)
        return await query_db.get(EveCorporation, corp_id)

    @classmethod
    async def sync_alliance(cls, query_db: AsyncSession, alliance_id: Optional[int]) -> Optional[EveAlliance]:
        """
        同步联盟信息（24 小时缓存）。若不存在或超过 24 小时则调用 ESI 更新。
        """

        if not alliance_id:
            return None

        alliance = await query_db.get(EveAlliance, alliance_id)
        if alliance and cls.__is_fresh(alliance.update_time):
            return alliance

        alliance_data: dict[str, Any] | None = None
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f'https://esi.evetech.net/latest/alliances/{alliance_id}/')
                resp.raise_for_status()
                alliance_data = resp.json()
        except Exception as e:  # noqa: BLE001
            logger.warning(f'同步联盟信息失败，alliance_id={alliance_id}: {e}')
            return alliance

        record = cls.__build_alliance_record(alliance_id, alliance_data)
        await cls.__upsert_alliance(query_db, record)
        return await query_db.get(EveAlliance, alliance_id)

    @classmethod
    async def check_corp_authorized(cls, query_db: AsyncSession, corp_id: Optional[int]) -> bool:
        """查询军团授权状态，is_authorized == '1' 视为通过。"""

        if not corp_id:
            return True
        result = await query_db.execute(
            select(EveCorporation.is_authorized).where(EveCorporation.corporation_id == corp_id)
        )
        status = result.scalar_one_or_none()
        return status == '1'

    @staticmethod
    def __is_fresh(update_time: Optional[datetime]) -> bool:
        if not update_time:
            return False
        return datetime.now() - update_time < timedelta(hours=24)

    @staticmethod
    def __parse_datetime(value: Any) -> Optional[datetime]:
        if not value:
            return None
        try:
            if isinstance(value, str):
                return datetime.fromisoformat(value.replace('Z', '+00:00')).replace(tzinfo=None)
            if isinstance(value, datetime):
                return value
        except Exception:  # noqa: BLE001
            return None
        return None

    @classmethod
    def __build_corp_record(cls, corp_id: int, data: dict[str, Any]) -> dict[str, Any]:
        return {
            'corporation_id': corp_id,
            'alliance_id': data.get('alliance_id'),
            'name': data.get('name') or str(corp_id),
            'ticker': data.get('ticker') or '',
            'ceo_id': data.get('ceo_id') or 0,
            'creator_id': data.get('creator_id'),
            'member_count': data.get('member_count') or 0,
            'tax_rate': data.get('tax_rate') or 0,
            'date_founded': cls.__parse_datetime(data.get('date_founded')),
            'description': data.get('description'),
            'home_station_id': data.get('home_station_id'),
            'faction_id': data.get('faction_id'),
            'shares': data.get('shares'),
            'url': data.get('url') or '',
            'war_eligible': data.get('war_eligible') if data.get('war_eligible') is not None else True,
            'icon': f'https://images.evetech.net/corporations/{corp_id}/logo?size=128',
            'status': '0',
            'update_time': datetime.now(),
        }

    @classmethod
    def __build_alliance_record(cls, alliance_id: int, data: dict[str, Any]) -> dict[str, Any]:
        return {
            'alliance_id': alliance_id,
            'name': data.get('name') or str(alliance_id),
            'ticker': data.get('ticker') or '',
            'executor_corporation_id': data.get('executor_corporation_id'),
            'creator_corporation_id': data.get('creator_corporation_id'),
            'creator_id': data.get('creator_id'),
            'date_founded': cls.__parse_datetime(data.get('date_founded')),
            'faction_id': data.get('faction_id'),
            'icon': f'https://images.evetech.net/alliances/{alliance_id}/logo?size=128',
            'status': '0',
            'update_time': datetime.now(),
        }

    @classmethod
    async def __upsert_corporation(cls, query_db: AsyncSession, record: dict[str, Any]) -> None:
        table = EveCorporation.__table__
        record_to_insert = {**record}
        record_to_insert.setdefault('create_time', datetime.now())
        insert_stmt = insert(table).values(**record_to_insert)
        update_values = {k: v for k, v in record.items() if k not in {'corporation_id', 'create_time', 'is_authorized'}}
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=[table.c.corporation_id],
            set_=update_values,
        )
        await query_db.execute(upsert_stmt)
        await query_db.commit()

    @classmethod
    async def __upsert_alliance(cls, query_db: AsyncSession, record: dict[str, Any]) -> None:
        table = EveAlliance.__table__
        record_to_insert = {**record}
        record_to_insert.setdefault('create_time', datetime.now())
        insert_stmt = insert(table).values(**record_to_insert)
        update_values = {k: v for k, v in record.items() if k not in {'alliance_id', 'create_time'}}
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=[table.c.alliance_id],
            set_=update_values,
        )
        await query_db.execute(upsert_stmt)
        await query_db.commit()
