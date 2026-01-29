# 路径: your_project/module_task/market_task.py
import logging
import datetime
import asyncio
# 注意这里：因为代码扁平化了，导入路径可能需要微调，确保能搜到 eve_logic
from .eve_logic.aggloader_v3 import MarketAggregator 

logger = logging.getLogger(__name__)

# --- 直接定义为顶层异步函数，不要放在 class 里面 ---
async def sync_market_data():
    """
    全量同步任务：每30分钟执行一次
    包含：抓取、分表入库、Pandas金融聚合、Top 10 站点统计
    """
    logger.info("--- [开始] 执行 EVE 全宇宙行情同步任务 ---")
    start_time = datetime.datetime.now()
    
    try:
        # 将耗时的同步流程放入线程，避免阻塞主事件循环
        def _run_sync_pipeline() -> int:
            aggregator = MarketAggregator()
            oid = aggregator.fetch_market_data()
            logger.info(f"步骤1：数据抓取完成，批次 ID: {oid}")
            aggregator.run_aggregations(oid)
            logger.info(f"步骤2：批次 {oid} 金融聚合计算完成")
            aggregator.save_top_stations(oid)
            logger.info(f"步骤3：批次 {oid} 首页 Top 10 统计完成")
            return oid

        orderset_id = await asyncio.to_thread(_run_sync_pipeline)
        
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).seconds
        
        msg = f"Batch {orderset_id} 同步成功，耗时 {duration} 秒。"
        logger.info(f"--- [结束] {msg} ---")
        return msg

    except Exception as e:
        logger.error(f"--- [失败] 任务执行异常: {str(e)} ---")
        raise e