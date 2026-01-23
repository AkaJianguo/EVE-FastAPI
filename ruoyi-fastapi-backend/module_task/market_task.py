# 路径: your_project/module_task/market_task.py
import logging
import datetime
from .eve_logic.aggloader_v3 import MarketAggregator  # 确保路径与你的目录结构一致

logger = logging.getLogger(__name__)

class MarketTask:
    """
    EVE 市场数据定时任务调度类
    对接 Ruoyi-FastAPI 的 sys_job 模块
    """

    async def sync_market_data(self):
        """
        全量同步任务：每30分钟执行一次
        包含：抓取、分表入库、Pandas金融聚合、Top 10 站点统计
        """
        logger.info("--- [开始] 执行 EVE 全宇宙行情同步任务 ---")
        start_time = datetime.datetime.now()
        
        try:
            # 实例化之前重构的逻辑核心类
            aggregator = MarketAggregator()
            
            # 1. 执行数据抓取并利用 COPY 入库 (market.orders_n 分表)
            # 返回当前生成的批次 ID (orderset_id)
            orderset_id = aggregator.fetch_market_data()
            logger.info(f"步骤1：数据抓取完成，批次 ID: {orderset_id}")
            
            # 2. 执行核心 Pandas 聚合计算 (5% 深度价格)
            # 计算结果将存入 market.aggregates 并同步至 Redis
            aggregator.run_aggregations(orderset_id)
            logger.info(f"步骤2：批次 {orderset_id} 金融聚合计算并同步 Redis 完成")

            # 3. 统计全宇宙买卖最活跃的 Top 10 站点
            # 结果存入 Redis (fp-sell, fp-buy) 供首页快速渲染
            aggregator.save_top_stations(orderset_id)
            logger.info(f"步骤3：批次 {orderset_id} 首页 Top 10 站点统计完成")
            
            end_time = datetime.datetime.now()
            duration = (end_time - start_time).seconds
            
            msg = f"Batch {orderset_id} 同步成功，耗时 {duration} 秒。"
            logger.info(f"--- [结束] {msg} ---")
            return msg

        except Exception as e:
            logger.error(f"--- [失败] 任务执行过程中出现异常: {str(e)} ---")
            # 抛出异常以便 Ruoyi 的 sys_job_log 能够记录错误堆栈
            raise e