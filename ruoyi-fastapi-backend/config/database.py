from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from config.env import DATABASE_URL

# 创建异步引擎
engine = create_async_engine(DATABASE_URL, echo=False)

# 创建异步 Session 工厂
# 此工厂同时服务于 public 和 raw 模式
AsyncSessionLocal = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    """
    [Public 模式] 应用数据模型基类
    用于系统常规业务表，如用户、日志等
    """
    pass


class SdeBase(AsyncAttrs, DeclarativeBase):
    """
    [Raw 模式] EVE SDE 静态数据模型基类
    强制绑定到 'raw' schema。
    注意：此模式下的表由外部自动化脚本维护，严禁在此处进行 create_all 操作。
    """
    metadata = MetaData(schema="raw")


async def init_create_table():
    """
    初始化数据库表结构
    """
    async with engine.begin() as conn:
        # 1. 仅创建 Base (public 模式) 关联的表
        await conn.run_sync(Base.metadata.create_all)

        # 2. 严禁运行 SdeBase.metadata.create_all
        # raw 模式的数据表结构是静态的，应由数据导入脚本管理，
        # 避免应用启动时意外修改或尝试创建这些表。
