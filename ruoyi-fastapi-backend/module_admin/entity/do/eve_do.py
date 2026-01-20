from datetime import datetime

from sqlalchemy import BigInteger, Boolean, CHAR, Column, DateTime, Float, Integer, String, Text

from config.database import Base


class EveAlliance(Base):
    """联盟信息表"""

    __tablename__ = 'eve_alliance'
    __table_args__ = {'comment': '联盟信息表'}

    alliance_id = Column(BigInteger, primary_key=True, nullable=False, comment='联盟ID (ESI返回)')
    name = Column(String(100), nullable=False, comment='联盟全名')
    ticker = Column(String(20), nullable=False, comment='联盟简称')
    executor_corporation_id = Column(BigInteger, nullable=True, comment='执行军团ID')
    creator_corporation_id = Column(BigInteger, nullable=True, comment='创建军团ID')
    creator_id = Column(BigInteger, nullable=True, comment='创建者ID')
    date_founded = Column(DateTime, nullable=True, comment='创立时间')
    faction_id = Column(BigInteger, nullable=True, comment='阵营ID')
    icon = Column(String(255), nullable=True, default='', comment='联盟图标URL')
    status = Column(CHAR(1), nullable=True, default='0', comment='状态（0正常 1停用）')
    create_by = Column(String(64), nullable=True, default='', comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_by = Column(String(64), nullable=True, default='', comment='更新者')
    update_time = Column(DateTime, nullable=True, default=datetime.now, comment='更新时间')
    remark = Column(String(500), nullable=True, comment='备注')


class EveCorporation(Base):
    """军团信息表"""

    __tablename__ = 'eve_corporation'
    __table_args__ = {'comment': '军团信息表'}

    corporation_id = Column(BigInteger, primary_key=True, nullable=False, comment='军团ID (ESI返回)')
    alliance_id = Column(BigInteger, nullable=True, comment='所属联盟ID')
    name = Column(String(100), nullable=False, comment='军团全名')
    ticker = Column(String(20), nullable=False, comment='军团简称')
    ceo_id = Column(BigInteger, nullable=False, comment='CEO Character ID')
    creator_id = Column(BigInteger, nullable=True, comment='创建者ID')
    member_count = Column(Integer, nullable=True, default=0, comment='成员数量')
    tax_rate = Column(Float, nullable=True, default=0, comment='税率')
    date_founded = Column(DateTime, nullable=True, comment='创立时间')
    description = Column(Text, nullable=True, comment='军团描述')
    home_station_id = Column(BigInteger, nullable=True, comment='总部空间站ID')
    faction_id = Column(BigInteger, nullable=True, comment='阵营ID')
    shares = Column(BigInteger, nullable=True, comment='股份数量')
    url = Column(String(255), nullable=True, default='', comment='军团官网')
    war_eligible = Column(Boolean, nullable=True, default=True, comment='是否可被宣战')
    icon = Column(String(255), nullable=True, default='', comment='军团图标URL')
    is_authorized = Column(CHAR(1), nullable=True, default='0', comment='是否已授权（0否 1是）')
    status = Column(CHAR(1), nullable=True, default='0', comment='状态（0正常 1停用）')
    create_by = Column(String(64), nullable=True, default='', comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_by = Column(String(64), nullable=True, default='', comment='更新者')
    update_time = Column(DateTime, nullable=True, default=datetime.now, comment='更新时间')
    remark = Column(String(500), nullable=True, comment='备注')
