from datetime import datetime
from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import Network, NotBlank, Size


class EveEntityModel(BaseModel):
    """EVE 组织架构表对应 pydantic 模型"""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    entity_id: Optional[int] = Field(default=None, description='实体ID (ESI ID)')
    parent_id: Optional[int] = Field(default=0, description='父级ID 联盟为0')
    ancestors: Optional[str] = Field(default='', description='祖级列表')
    entity_name: Optional[str] = Field(default=None, description='名称')
    ticker: Optional[str] = Field(default=None, description='简称')
    entity_type: Optional[Literal['1', '2']] = Field(default=None, description='类型 1联盟 2军团')
    is_authorized: Optional[Literal['0', '1']] = Field(default='0', description='授权状态')
    ceo_id: Optional[int] = Field(default=None, description='CEO/执行官ID')
    executor_corp_id: Optional[int] = Field(default=None, description='执行军团ID')
    creator_id: Optional[int] = Field(default=None, description='创建者ID')
    member_count: Optional[int] = Field(default=0, description='成员数量')
    tax_rate: Optional[float] = Field(default=0, description='税率')
    date_founded: Optional[datetime] = Field(default=None, description='创立时间')
    faction_id: Optional[int] = Field(default=None, description='阵营ID')
    icon: Optional[str] = Field(default='', description='图标URL')
    home_station_id: Optional[int] = Field(default=None, description='总部空间站')
    url: Optional[str] = Field(default='', description='官网地址')
    war_eligible: Optional[bool] = Field(default=True, description='是否可被宣战')
    order_num: Optional[int] = Field(default=0, description='显示顺序')
    status: Optional[Literal['0', '1']] = Field(default='0', description='状态（0正常 1停用）')
    del_flag: Optional[Literal['0', '2']] = Field(default='0', description='删除标志')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')

    @NotBlank(field_name='entity_name', message='组织名称不能为空')
    @Size(field_name='entity_name', min_length=0, max_length=100, message='组织名称长度不能超过100个字符')
    def get_entity_name(self) -> Union[str, None]:
        return self.entity_name

    @NotBlank(field_name='order_num', message='显示排序不能为空')
    def get_order_num(self) -> Union[int, None]:
        return self.order_num

    def validate_fields(self) -> None:
        self.get_entity_name()
        self.get_order_num()


class EveEntityQueryModel(EveEntityModel):
    """组织不分页查询模型"""

    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


class EveEntityTreeModel(BaseModel):
    """组织树模型"""

    model_config = ConfigDict(alias_generator=to_camel)

    id: int = Field(description='实体ID')
    label: str = Field(description='名称')
    parent_id: int = Field(description='父级ID')
    children: Optional[list['EveEntityTreeModel']] = Field(default=None, description='子节点')


class DeleteEveEntityModel(BaseModel):
    """删除组织模型"""

    model_config = ConfigDict(alias_generator=to_camel)

    entity_ids: str = Field(default=None, description='需要删除的实体ID')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[str] = Field(default=None, description='更新时间')
