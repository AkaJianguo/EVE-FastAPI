from collections.abc import Sequence
from typing import Any

from sqlalchemy import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant
from common.vo import CrudResponseModel
from exceptions.exception import ServiceException, ServiceWarning
from module_admin.dao.eve_entity_dao import EveEntityDao
from module_admin.entity.do.eve_do import EveEntity
from module_admin.entity.vo.eve_entity_vo import DeleteEveEntityModel, EveEntityModel, EveEntityTreeModel
from utils.common_util import CamelCaseUtil


class EveEntityService:
    """EVE 组织架构模块服务层"""

    @classmethod
    async def get_entity_tree_services(
        cls, query_db: AsyncSession, page_object: EveEntityModel, data_scope_sql: ColumnElement
    ) -> list[dict[str, Any]]:
        entity_list_result = await EveEntityDao.get_entity_list_for_tree(query_db, page_object, data_scope_sql)
        entity_tree_model_result = cls.list_to_tree(entity_list_result)
        return [entity.model_dump(exclude_unset=True, by_alias=True) for entity in entity_tree_model_result]

    @classmethod
    async def get_entity_for_edit_option_services(
        cls, query_db: AsyncSession, page_object: EveEntityModel, data_scope_sql: ColumnElement
    ) -> list[dict[str, Any]]:
        entity_list_result = await EveEntityDao.get_entity_info_for_edit_option(query_db, page_object, data_scope_sql)
        return CamelCaseUtil.transform_result(entity_list_result)

    @classmethod
    async def get_entity_list_services(
        cls, query_db: AsyncSession, page_object: EveEntityModel, data_scope_sql: ColumnElement
    ) -> list[dict[str, Any]]:
        entity_list_result = await EveEntityDao.get_entity_list(query_db, page_object, data_scope_sql)
        return CamelCaseUtil.transform_result(entity_list_result)

    @classmethod
    async def check_entity_name_unique_services(cls, query_db: AsyncSession, page_object: EveEntityModel) -> bool:
        entity_id = -1 if page_object.entity_id is None else page_object.entity_id
        entity = await EveEntityDao.get_entity_detail_by_info(
            query_db, EveEntityModel(entity_name=page_object.entity_name, parent_id=page_object.parent_id)
        )
        if entity and entity.entity_id != entity_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def add_entity_services(cls, query_db: AsyncSession, page_object: EveEntityModel) -> CrudResponseModel:
        if not await cls.check_entity_name_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增组织{page_object.entity_name}失败，名称已存在')
        parent_info = await EveEntityDao.get_entity_by_id(query_db, page_object.parent_id or 0)
        if parent_info and parent_info.status != CommonConstant.DEPT_NORMAL:
            raise ServiceException(message=f'组织{parent_info.entity_name}停用，不允许新增')
        page_object.ancestors = f"{parent_info.ancestors},{page_object.parent_id}" if parent_info else '0'
        try:
            await EveEntityDao.add_entity_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:  # noqa: BLE001
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_entity_services(cls, query_db: AsyncSession, page_object: EveEntityModel) -> CrudResponseModel:
        if not await cls.check_entity_name_unique_services(query_db, page_object):
            raise ServiceException(message=f'修改组织{page_object.entity_name}失败，名称已存在')
        if page_object.entity_id == page_object.parent_id:
            raise ServiceException(message=f'修改组织{page_object.entity_name}失败，上级不能是自己')
        if (
            page_object.status == CommonConstant.DEPT_DISABLE
            and (await EveEntityDao.count_children_entity_dao(query_db, page_object.entity_id)) > 0
        ):
            raise ServiceException(message=f'修改组织{page_object.entity_name}失败，该组织包含未停用的子节点')
        new_parent = await EveEntityDao.get_entity_by_id(query_db, page_object.parent_id or 0)
        old_entity = await EveEntityDao.get_entity_by_id(query_db, page_object.entity_id)
        try:
            if new_parent and old_entity:
                new_ancestors = f"{new_parent.ancestors},{new_parent.entity_id}" if new_parent.ancestors else f"0,{new_parent.entity_id}"
                old_ancestors = old_entity.ancestors
                page_object.ancestors = new_ancestors
                await cls.update_entity_children(query_db, page_object.entity_id, new_ancestors, old_ancestors)
            edit_entity = page_object.model_dump(exclude_unset=True)
            await EveEntityDao.edit_entity_dao(query_db, edit_entity)
            if page_object.status == CommonConstant.DEPT_NORMAL and page_object.ancestors and page_object.ancestors != '0':
                await cls.update_parent_entity_status_normal(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='更新成功')
        except Exception as e:  # noqa: BLE001
            await query_db.rollback()
            raise e

    @classmethod
    async def delete_entity_services(cls, query_db: AsyncSession, page_object: DeleteEveEntityModel) -> CrudResponseModel:
        if page_object.entity_ids:
            entity_id_list = page_object.entity_ids.split(',')
            try:
                for entity_id in entity_id_list:
                    if (await EveEntityDao.count_children_entity_dao(query_db, int(entity_id))) > 0:
                        raise ServiceWarning(message='存在下级组织,不允许删除')
                    if (await EveEntityDao.count_entity_user_dao(query_db, int(entity_id))) > 0:
                        raise ServiceWarning(message='组织存在用户,不允许删除')
                    await EveEntityDao.delete_entity_dao(query_db, EveEntityModel(entity_id=entity_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:  # noqa: BLE001
                await query_db.rollback()
                raise e
        raise ServiceException(message='传入组织ID为空')

    @classmethod
    async def entity_detail_services(cls, query_db: AsyncSession, entity_id: int) -> EveEntityModel:
        entity = await EveEntityDao.get_entity_detail_by_id(query_db, entity_id=entity_id)
        return EveEntityModel(**CamelCaseUtil.transform_result(entity)) if entity else EveEntityModel()

    @classmethod
    def list_to_tree(cls, entity_list: Sequence[EveEntity]) -> list[EveEntityTreeModel]:
        _entity_list = [EveEntityTreeModel(id=item.entity_id, label=item.entity_name, parent_id=item.parent_id) for item in entity_list]
        mapping: dict[int, EveEntityTreeModel] = dict(zip([i.id for i in _entity_list], _entity_list))
        container: list[EveEntityTreeModel] = []
        for d in _entity_list:
            parent = mapping.get(d.parent_id)
            if parent is None:
                container.append(d)
            else:
                children: list[EveEntityTreeModel] = parent.children or []
                children.append(d)
                parent.children = children
        return container

    @classmethod
    async def replace_first(cls, original_str: str, old_str: str, new_str: str) -> str:
        if original_str.startswith(old_str):
            return original_str.replace(old_str, new_str, 1)
        return original_str

    @classmethod
    async def update_parent_entity_status_normal(cls, query_db: AsyncSession, entity: EveEntityModel) -> None:
        entity_id_list = entity.ancestors.split(',')
        await EveEntityDao.update_entity_status_normal_dao(query_db, list(map(int, entity_id_list)))

    @classmethod
    async def update_entity_children(
        cls, query_db: AsyncSession, entity_id: int, new_ancestors: str, old_ancestors: str
    ) -> None:
        children = await EveEntityDao.get_children_entity_dao(query_db, entity_id)
        update_children = []
        for child in children:
            child_ancestors = await cls.replace_first(child.ancestors, old_ancestors, new_ancestors)
            update_children.append({'entity_id': child.entity_id, 'ancestors': child_ancestors})
        if children:
            await EveEntityDao.update_entity_children_dao(query_db, update_children)

    @classmethod
    async def cascade_authorized(cls, query_db: AsyncSession, alliance_id: int, target_status: str) -> None:
        await EveEntityDao.cascade_authorized(query_db, alliance_id, target_status)
        await query_db.commit()
