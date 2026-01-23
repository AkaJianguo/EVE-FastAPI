from config.database import AsyncSessionLocal

async def get_db():
    """
    [Public 模式依赖] 获取数据库会话
    用途：常规业务读写
    行为：自动提交事务
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def get_sde_db():
    """
    [Raw 模式依赖] 获取 SDE 数据库会话
    用途：查询 EVE 静态数据
    行为：只读模式（默认不提交）
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # 注意：此处故意不执行 session.commit()
            # SDE 数据应视为只读资源，防止业务逻辑无意中修改静态数据。
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
