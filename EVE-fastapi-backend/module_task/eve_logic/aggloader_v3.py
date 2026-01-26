import os
import io
import csv
import json
import base64
import logging
import datetime
import pandas as pd
import numpy as np
import redis
import httpx  # 建议在 FastAPI 环境下使用 httpx 替代 requests
from sqlalchemy import create_engine, text
from configparser import ConfigParser
from concurrent.futures import as_completed

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[logging.FileHandler("logs/market_aggregator.log"), logging.StreamHandler()]
)

class MarketAggregator:
    def save_top_stations(self, orderset_id: int):
        """
        计算并存储全宇宙交易量最大的 10 个空间站 (用于首页展示)
        逻辑参考原版 aggloader-esi.py
        """
        table_suffix = (orderset_id // 100) % 10
        logging.info(f"正在计算批次 {orderset_id} 的 Top 10 活跃站点...")

        # 定义查询逻辑：统计卖单数量最多的前10个空间站
        # 注意：这里关联了你定义的 row 模式下的空间站表
        sql_template = """
        SELECT 
            json_agg(t) 
        FROM (
            SELECT 
                count(*) as order_count,
                s.data->>'name' as "stationName",
                o."stationID",
                sum(o.volume) as total_volume
            FROM market.orders_{suffix} o
            LEFT JOIN row.npc_stations s ON o."stationID" = s.id
            WHERE o."orderSet" = :oid AND o.buy = :is_buy
            GROUP BY o."stationID", s.data->>'name'
            ORDER BY order_count DESC
            LIMIT 10
        ) t
        """

        with self.engine.connect() as conn:
            # 统计卖单 Top 10 (fp-sell)
            sell_res = conn.execute(
                text(sql_template.format(suffix=table_suffix)), 
                {"oid": orderset_id, "is_buy": False}
            ).fetchone()
            if sell_res and sell_res[0]:
                self.redis.set("fp-sell", json.dumps(sell_res[0]))

            # 统计买单 Top 10 (fp-buy)
            buy_res = conn.execute(
                text(sql_template.format(suffix=table_suffix)), 
                {"oid": orderset_id, "is_buy": True}
            ).fetchone()
            if buy_res and buy_res[0]:
                self.redis.set("fp-buy", json.dumps(buy_res[0]))

            # 更新最后刷新时间
            self.redis.set("fp-lastupdate", datetime.datetime.utcnow().isoformat())
    def __init__(self, config_path=None):
        # 自动定位项目根目录下的配置文件；支持 ENV_STATE 切换本地/生产
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))

        if config_path is None:
            env_state = os.getenv("ENV_STATE", "").lower()
            cfg_name = "esi.prod.cfg" if env_state == "production" else "esi.local.cfg"
            config_path = os.path.join(project_root, cfg_name)
            logging.info(f"ENV_STATE={env_state or 'local'}, 选择配置: {config_path}")
        else:
            logging.info(f"使用传入的配置文件: {config_path}")

        self.config = ConfigParser()

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"找不到配置文件，请确保 {config_path} 存在！")

        self.config.read(config_path, encoding='utf-8')
        
        # 优先使用环境变量注入的敏感信息，避免写死在本地文件
        self.client_id = os.getenv("EVE_CLIENT_ID", self.config.get('oauth', 'clientid', fallback=''))
        self.client_secret = os.getenv("EVE_CLIENT_SECRET", self.config.get('oauth', 'secret', fallback=''))
        self.refresh_token = os.getenv("EVE_REFRESH_TOKEN", self.config.get('oauth', 'refreshtoken', fallback=''))
        
        # 数据库与 Redis 初始化
        self.engine = create_engine(self.config.get('database', 'connectionstring'))
        self.redis = redis.StrictRedis(
            host=self.config.get('redis', 'host', fallback='localhost'),
            port=self.config.getint('redis', 'port', fallback=6379)
        )
        self.user_agent = self.config.get('requests', 'useragent')
        self.temp_dir = "/tmp/eve_market"
        os.makedirs(self.temp_dir, exist_ok=True)

    def get_access_token(self):
        """获取 SSO 授权令牌"""
        client_id = self.client_id
        secret = self.client_secret
        refresh_token = self.refresh_token
        
        auth = base64.b64encode(f"{client_id}:{secret}".encode()).decode()
        headers = {'Authorization': f'Basic {auth}', 'User-Agent': self.user_agent}
        data = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
        
        with httpx.Client() as client:
            resp = client.post('https://login.eveonline.com/oauth/token', data=data, headers=headers)
            return resp.json()['access_token']

    def fetch_market_data(self) -> int:
        """执行全宇宙抓取逻辑 (简化示意)"""
        # 1. 在 market 模式中记录新批次
        with self.engine.begin() as conn:
            orderset_id = conn.execute(text(
                "INSERT INTO market.orderset (downloaded) VALUES (now()) RETURNING id"
            )).scalar()
        if orderset_id is None:
            raise ValueError("Failed to generate orderset id from database")
        
        csv_path = os.path.join(self.temp_dir, f"orderset-{orderset_id}.csv")
        logging.info(f"开始抓取批次 {orderset_id} -> {csv_path}")

        # [此处保留你原有的 getData 和 processData 逻辑，但需将输出字段对齐 market.orders 表结构]
        # ... 抓取逻辑 ...

        # 2. 批量入库 (使用 COPY 提高稳定性)
        table_suffix = (orderset_id // 100) % 10
        with self.engine.begin() as conn:
            # 注意：此处明确指向 market 模式
            sql = f"""
            COPY market.orders_{table_suffix} 
            ("orderID", "typeID", issued, buy, volume, price, "stationID", region, "orderSet") 
            FROM '{csv_path}' WITH (FORMAT csv, DELIMITER '\t')
            """
            conn.execute(text(sql))
            
        return int(orderset_id)

    def run_aggregations(self, orderset_id: int):
        """核心 Pandas 算法：计算 5% 深度价格"""
        table_suffix = (orderset_id // 100) % 10
        logging.info(f"正在对 orders_{table_suffix} 进行金融聚合统计...")

        # 从数据库读取原始数据
        query = f'SELECT * FROM market.orders_{table_suffix} WHERE "orderSet" = :oid'
        df = pd.read_sql(query, self.engine, params={"oid": orderset_id})

        # 构造聚合标识
        df['what'] = df['region'].astype(str) + '|' + df['typeID'].astype(str) + '|' + df['buy'].astype(str).str.lower()

        # 核心算法：5% 价格深度 (Secret Sauce)
        def calculate_five_percent(group: pd.DataFrame) -> float:
            # 过滤极端异常值
            min_p, max_p = group['price'].min(), group['price'].max()
            if group['buy'].iloc[0]: # 买单：过滤掉极低价
                group = group[group['price'] >= max_p / 100]
                group = group.sort_values('price', ascending=False)
            else: # 卖单：过滤掉极高价
                group = group[group['price'] <= min_p * 100]
                group = group.sort_values('price', ascending=True)

            total_vol = float(group['volume'].sum())
            threshold = total_vol * 0.05
            group['cumsum'] = group['volume'].cumsum()
            
            # 找到前 5% 的成交区间
            five_p_slice = group[group['cumsum'] <= threshold].copy()
            if five_p_slice.empty:
                return group['price'].iloc[0]
            price_arr = five_p_slice['price'].to_numpy(dtype=float, copy=False)
            vol_arr = five_p_slice['volume'].to_numpy(dtype=float, copy=False)
            return float(np.average(price_arr, weights=vol_arr))

        def weighted_average(prices: pd.Series) -> float:
            price_arr = prices.to_numpy(dtype=float, copy=False)
            volume_arr = df.loc[prices.index, 'volume'].to_numpy(dtype=float, copy=False)
            return float(np.average(price_arr, weights=volume_arr))

        # 执行聚合计算
        agg_df = df.groupby('what').agg(
            weightedaverage=('price', weighted_average),
            maxval=('price', 'max'),
            minval=('price', 'min'),
            volume=('volume', 'sum'),
            numorders=('price', 'count')
        )
        
        # 应用 5% 算法
        agg_df['fivepercent'] = df.groupby('what').apply(calculate_five_percent)
        agg_df['orderSet'] = orderset_id

        # 3. 输出到 market.aggregates
        agg_df.to_sql('aggregates', self.engine, schema='market', if_exists='append', index=True)

        # 4. 同步到 Redis (响应毫秒级查询)
        pipe = self.redis.pipeline()
        for row in agg_df.itertuples():
            # 数据格式：加权平均|5%深度|最高|最低|成交量
            val = f"{row.weightedaverage}|{row.fivepercent}|{row.maxval}|{row.minval}|{row.volume}"
            pipe.set(str(row.Index), val, ex=5400) # 1.5小时过期
        pipe.execute()

        logging.info(f"批次 {orderset_id} 处理完成")

if __name__ == "__main__":
    aggregator = MarketAggregator()
    # orderset_id = aggregator.fetch_market_data()
    # aggregator.run_aggregations(orderset_id)