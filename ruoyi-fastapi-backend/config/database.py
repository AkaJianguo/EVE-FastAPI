import asyncpg.exceptions
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from config.env import GetConfig

# 加载数据库配置
db_settings = GetConfig().get_database_config()

# 创建异步引擎
engine = create_async_engine(
    db_settings.database_url,
    echo=db_settings.db_echo,
    pool_size=db_settings.db_pool_size,
    max_overflow=db_settings.db_max_overflow,
    pool_recycle=db_settings.db_pool_recycle,
    pool_timeout=db_settings.db_pool_timeout,
    connect_args={"command_timeout": 60}
)

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
    try:
        async with engine.begin() as conn:
            # 1. 仅创建 Base (public 模式) 关联的表
            await conn.run_sync(Base.metadata.create_all)

            # 2. 严禁运行 SdeBase.metadata.create_all
            # raw 模式的数据表结构是静态的，应由数据导入脚本管理，
            # 避免应用启动时意外修改或尝试创建这些表。
    except asyncpg.exceptions.InvalidPasswordError as e:
        print('[错误] 数据库密码错误，请检查 .env 文件中的 DB_PASSWORD。')
        print(f'详细信息: {e}')
    except ConnectionRefusedError:
        print(f'[错误] 无法连接到数据库 {db_settings.db_host}:{db_settings.db_port}。')
        print('[提示] 请检查 SSH 隧道是否已开启并正确绑定在 5433 端口。')
    except Exception as e:
        print(f'[错误] 数据库初始化失败: {e}')
