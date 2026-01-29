from datetime import datetime

from sqlalchemy import BigInteger, Boolean, CHAR, Column, DateTime, Float, Integer, String

from config.database import Base


class EveEntity(Base):
    """EVE 组织架构表（合并联盟与军团）"""

    __tablename__ = 'eve_entity'
    __table_args__ = {'comment': 'EVE 组织架构表 (合并联盟与军团)'}

    entity_id = Column(BigInteger, primary_key=True, nullable=False, comment='实体ID (ESI ID)')
    parent_id = Column(BigInteger, nullable=True, default=0, comment='父级ID (联盟为0)')
    ancestors = Column(String(100), nullable=True, default='', comment='祖级列表')
    entity_name = Column(String(100), nullable=False, comment='名称 (Alliance/Corp)')
    ticker = Column(String(20), nullable=False, comment='简称')
    entity_type = Column(CHAR(1), nullable=False, comment='类型：1=联盟, 2=军团')
    is_authorized = Column(CHAR(1), nullable=True, default='0', comment='授权状态 (0未授权 1已授权)')

    ceo_id = Column(BigInteger, nullable=True, comment='CEO ID (军团) 或执行官ID (联盟)')
    executor_corp_id = Column(BigInteger, nullable=True, comment='执行军团ID (联盟)')
    creator_id = Column(BigInteger, nullable=True, comment='创建者ID')
    member_count = Column(Integer, nullable=True, default=0, comment='成员数量 (军团)')
    tax_rate = Column(Float, nullable=True, default=0, comment='税率 (军团)')
    date_founded = Column(DateTime, nullable=True, comment='创立时间')
    faction_id = Column(BigInteger, nullable=True, comment='阵营ID')
    icon = Column(String(255), nullable=True, default='', comment='图标URL')

    home_station_id = Column(BigInteger, nullable=True, comment='总部空间站 (军团)')
    url = Column(String(255), nullable=True, default='', comment='官网地址')
    war_eligible = Column(Boolean, nullable=True, default=True, comment='是否可被宣战 (军团)')

    order_num = Column(Integer, nullable=True, default=0, comment='显示顺序')
    status = Column(CHAR(1), nullable=True, default='0', comment='状态 (0正常 1停用)')
    del_flag = Column(CHAR(1), nullable=True, default='0', comment='删除标志（0存在 2删除）')
    create_by = Column(String(64), nullable=True, default='', comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_by = Column(String(64), nullable=True, default='', comment='更新者')
    update_time = Column(DateTime, nullable=True, default=datetime.now, comment='更新时间')
    remark = Column(String(500), nullable=True, comment='备注')
