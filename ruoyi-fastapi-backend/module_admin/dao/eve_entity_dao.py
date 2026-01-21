from collections.abc import Sequence
from typing import Union

from sqlalchemy import ColumnElement, bindparam, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import immutabledict

from module_admin.entity.do.eve_do import EveEntity
from module_admin.entity.vo.eve_entity_vo import EveEntityModel


class EveEntityDao:
    """EVE 组织架构数据库操作层"""

    @classmethod
    async def get_entity_by_id(cls, db: AsyncSession, entity_id: int) -> Union[EveEntity, None]:
        return (await db.execute(select(EveEntity).where(EveEntity.entity_id == entity_id))).scalars().first()

    @classmethod
    async def get_entity_detail_by_id(cls, db: AsyncSession, entity_id: int) -> Union[EveEntity, None]:
        return (
            (await db.execute(select(EveEntity).where(EveEntity.entity_id == entity_id, EveEntity.del_flag == '0')))
            .scalars()
            .first()
        )

    @classmethod
    async def get_entity_detail_by_info(cls, db: AsyncSession, entity: EveEntityModel) -> Union[EveEntity, None]:
        return (
            (
                await db.execute(
                    select(EveEntity).where(
                        EveEntity.parent_id == entity.parent_id if entity.parent_id else True,
                        EveEntity.entity_name == entity.entity_name if entity.entity_name else True,
                        EveEntity.del_flag == '0',
                    )
                )
            )
            .scalars()
            .first()
        )

    @classmethod
    async def get_entity_info_for_edit_option(
        cls, db: AsyncSession, entity_info: EveEntityModel, data_scope_sql: ColumnElement
    ) -> Sequence[EveEntity]:
        return (
            (
                await db.execute(
                    select(EveEntity)
                    .where(
                        EveEntity.entity_id != entity_info.entity_id,
                        ~EveEntity.entity_id.in_(
                            select(EveEntity.entity_id).where(func.find_in_set(entity_info.entity_id, EveEntity.ancestors))
                        ),
                        EveEntity.del_flag == '0',
                        EveEntity.status == '0',
                        data_scope_sql,
                    )
                    .order_by(EveEntity.order_num)
                    .distinct()
                )
            )
            .scalars()
            .all()
        )

    @classmethod
    async def get_children_entity_dao(cls, db: AsyncSession, entity_id: int) -> Sequence[EveEntity]:
        return (
            (await db.execute(select(EveEntity).where(func.find_in_set(entity_id, EveEntity.ancestors)))).scalars().all()
        )

    @classmethod
    async def get_entity_list_for_tree(
        cls, db: AsyncSession, entity_info: EveEntityModel, data_scope_sql: ColumnElement
    ) -> Sequence[EveEntity]:
        return (
            (
                await db.execute(
                    select(EveEntity)
                    .where(
                        EveEntity.status == '0',
                        EveEntity.del_flag == '0',
                        EveEntity.entity_name.like(f"%{entity_info.entity_name}%") if entity_info.entity_name else True,
                        data_scope_sql,
                    )
                    .order_by(EveEntity.order_num)
                    .distinct()
                )
            )
            .scalars()
            .all()
        )

    @classmethod
    async def get_entity_list(
        cls, db: AsyncSession, page_object: EveEntityModel, data_scope_sql: ColumnElement
    ) -> Sequence[EveEntity]:
        return (
            (
                await db.execute(
                    select(EveEntity)
                    .where(
                        EveEntity.del_flag == '0',
                        EveEntity.entity_id == page_object.entity_id if page_object.entity_id is not None else True,
                        EveEntity.status == page_object.status if page_object.status else True,
                        EveEntity.entity_name.like(f"%{page_object.entity_name}%") if page_object.entity_name else True,
                        data_scope_sql,
                    )
                    .order_by(EveEntity.order_num)
                    .distinct()
                )
            )
            .scalars()
            .all()
        )

    @classmethod
    async def add_entity_dao(cls, db: AsyncSession, entity: EveEntityModel) -> EveEntity:
        db_entity = EveEntity(**entity.model_dump())
        db.add(db_entity)
        await db.flush()
        return db_entity

    @classmethod
    async def edit_entity_dao(cls, db: AsyncSession, entity: dict) -> None:
        await db.execute(update(EveEntity), [entity])

    @classmethod
    async def update_entity_children_dao(cls, db: AsyncSession, update_entities: list) -> None:
        await db.execute(
            update(EveEntity)
            .where(EveEntity.entity_id == bindparam('entity_id'))
            .values(
                {
                    'entity_id': bindparam('entity_id'),
                    'ancestors': bindparam('ancestors'),
                }
            ),
            update_entities,
            execution_options=immutabledict({'synchronize_session': None}),
        )

    @classmethod
    async def update_entity_status_normal_dao(cls, db: AsyncSession, entity_id_list: list) -> None:
        await db.execute(update(EveEntity).where(EveEntity.entity_id.in_(entity_id_list)).values(status='0'))

    @classmethod
    async def delete_entity_dao(cls, db: AsyncSession, entity: EveEntityModel) -> None:
        await db.execute(
            update(EveEntity)
            .where(EveEntity.entity_id == entity.entity_id)
            .values(del_flag='2', update_by=entity.update_by, update_time=entity.update_time)
        )

    @classmethod
    async def count_children_entity_dao(cls, db: AsyncSession, entity_id: int) -> int:
        return (
            (await db.execute(select(func.count('*')).select_from(EveEntity).where(EveEntity.parent_id == entity_id)))
            .scalars()
            .first()
            or 0
        )

    @classmethod
    async def count_entity_user_dao(cls, db: AsyncSession, entity_id: int) -> int:
        # 占位：如果未来需要与用户关联，再实现；当前返回0避免阻塞删除
        return 0

    @classmethod
    async def cascade_authorized(cls, db: AsyncSession, alliance_id: int, target_status: str) -> None:
        """授权级联：联盟及其子军团设置同一授权状态。"""
        await db.execute(
            update(EveEntity)
            .where(
                (EveEntity.entity_id == alliance_id)
                | (func.find_in_set(alliance_id, EveEntity.ancestors))
            )
            .values(is_authorized=target_status)
        )
