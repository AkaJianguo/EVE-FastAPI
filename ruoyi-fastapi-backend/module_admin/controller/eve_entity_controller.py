from datetime import datetime
from typing import Annotated

from fastapi import Path, Query, Request, Response
from pydantic_validation_decorator import ValidateFields
from sqlalchemy import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

from common.annotation.log_annotation import Log
from common.aspect.data_scope import DataScopeDependency
from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.enums import BusinessType
from common.router import APIRouterPro
from common.vo import DataResponseModel, ResponseBaseModel
from module_admin.entity.do.eve_do import EveEntity
from module_admin.entity.vo.eve_entity_vo import DeleteEveEntityModel, EveEntityModel, EveEntityQueryModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.eve_entity_service import EveEntityService
from utils.log_util import logger
from utils.response_util import ResponseUtil


eve_entity_controller = APIRouterPro(
    prefix='/eve/entity', order_num=7, tags=['EVE 组织管理'], dependencies=[PreAuthDependency()]
)


@eve_entity_controller.get(
    '/list/exclude/{entity_id}',
    summary='获取编辑组织的下拉树接口',
    description='用于获取组织下拉树，不包含指定组织及其子组织',
    response_model=DataResponseModel[list[EveEntityModel]],
    dependencies=[UserInterfaceAuthDependency('eve:entity:list')],
)
async def get_eve_entity_tree_for_edit_option(
    request: Request,
    entity_id: Annotated[int, Path(description='实体ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    data_scope_sql: Annotated[ColumnElement, DataScopeDependency(EveEntity)],
) -> Response:
    entity_query = EveEntityModel(entity_id=entity_id)
    entity_query_result = await EveEntityService.get_entity_for_edit_option_services(query_db, entity_query, data_scope_sql)
    logger.info('获取成功')
    return ResponseUtil.success(data=entity_query_result)


@eve_entity_controller.get(
    '/list',
    summary='获取组织列表接口',
    description='用于获取组织列表',
    response_model=DataResponseModel[list[EveEntityModel]],
    dependencies=[UserInterfaceAuthDependency('eve:entity:list')],
)
async def get_eve_entity_list(
    request: Request,
    entity_query: Annotated[EveEntityQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    data_scope_sql: Annotated[ColumnElement, DataScopeDependency(EveEntity)],
) -> Response:
    entity_query_result = await EveEntityService.get_entity_list_services(query_db, entity_query, data_scope_sql)
    logger.info('获取成功')
    return ResponseUtil.success(data=entity_query_result)


@eve_entity_controller.post(
    '',
    summary='新增组织接口',
    description='用于新增组织',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('eve:entity:add')],
)
@ValidateFields(validate_model='add_dept')
@Log(title='组织管理', business_type=BusinessType.INSERT)
async def add_eve_entity(
    request: Request,
    add_entity: EveEntityModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_entity.create_by = current_user.user.user_name
    add_entity.create_time = datetime.now()
    add_entity.update_by = current_user.user.user_name
    add_entity.update_time = datetime.now()
    add_entity_result = await EveEntityService.add_entity_services(query_db, add_entity)
    logger.info(add_entity_result.message)
    return ResponseUtil.success(msg=add_entity_result.message)


@eve_entity_controller.put(
    '',
    summary='编辑组织接口',
    description='用于编辑组织',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('eve:entity:edit')],
)
@ValidateFields(validate_model='edit_dept')
@Log(title='组织管理', business_type=BusinessType.UPDATE)
async def edit_eve_entity(
    request: Request,
    edit_entity: EveEntityModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
    data_scope_sql: Annotated[ColumnElement, DataScopeDependency(EveEntity)],
) -> Response:
    if not current_user.user.admin:
        await EveEntityService.get_entity_list_services(query_db, EveEntityModel(entity_id=edit_entity.entity_id), data_scope_sql)
    edit_entity.update_by = current_user.user.user_name
    edit_entity.update_time = datetime.now()
    edit_entity_result = await EveEntityService.edit_entity_services(query_db, edit_entity)
    logger.info(edit_entity_result.message)
    return ResponseUtil.success(msg=edit_entity_result.message)


@eve_entity_controller.delete(
    '/{entity_ids}',
    summary='删除组织接口',
    description='用于删除组织',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('eve:entity:remove')],
)
@Log(title='组织管理', business_type=BusinessType.DELETE)
async def delete_eve_entity(
    request: Request,
    entity_ids: Annotated[str, Path(description='需要删除的实体ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
    data_scope_sql: Annotated[ColumnElement, DataScopeDependency(EveEntity)],
) -> Response:
    entity_id_list = entity_ids.split(',') if entity_ids else []
    if entity_id_list and not current_user.user.admin:
        await EveEntityService.get_entity_list_services(query_db, EveEntityModel(entity_id=int(entity_id_list[0])), data_scope_sql)
    delete_entity = DeleteEveEntityModel(entity_ids=entity_ids)
    delete_entity.update_by = current_user.user.user_name
    delete_entity.update_time = datetime.now()
    delete_entity_result = await EveEntityService.delete_entity_services(query_db, delete_entity)
    logger.info(delete_entity_result.message)
    return ResponseUtil.success(msg=delete_entity_result.message)


@eve_entity_controller.get(
    '/{entity_id}',
    summary='获取组织详情接口',
    description='用于获取指定组织的详情信息',
    response_model=DataResponseModel[EveEntityModel],
    dependencies=[UserInterfaceAuthDependency('eve:entity:query')],
)
async def query_detail_eve_entity(
    request: Request,
    entity_id: Annotated[int, Path(description='实体ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
    data_scope_sql: Annotated[ColumnElement, DataScopeDependency(EveEntity)],
) -> Response:
    if not current_user.user.admin:
        await EveEntityService.get_entity_list_services(query_db, EveEntityModel(entity_id=entity_id), data_scope_sql)
    detail_entity_result = await EveEntityService.entity_detail_services(query_db, entity_id)
    logger.info(f'获取entity_id为{entity_id}的信息成功')
    return ResponseUtil.success(data=detail_entity_result)
