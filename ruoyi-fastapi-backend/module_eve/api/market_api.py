import asyncio
import json
from typing import Any, Iterable

from fastapi import Request, Response
from redis.asyncio import Redis

from common.router import APIRouterPro
from module_eve.schemas.market import MarketIndexResponse, StationHotTop
from utils.response_util import ResponseUtil

market_router = APIRouterPro(prefix="/index", tags=["EVE 行情中心"], auto_register=False)


def _load_station_list(raw: Any) -> list[StationHotTop]:
    if raw is None:
        return []
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return []
    if not isinstance(parsed, Iterable):
        return []
    result: list[StationHotTop] = []
    for item in parsed:
        if isinstance(item, dict):
            result.append(StationHotTop(**item))
    return result


@market_router.get(
    "/hot-stations",
    summary="获取热门空间站榜单",
    description="读取 Redis 缓存的买卖榜单与最后刷新时间",
    response_model=MarketIndexResponse,
)
async def get_hot_stations(request: Request) -> Response:
    redis_client: Redis = request.app.state.redis

    sell_raw, buy_raw, last_update = await asyncio.gather(
        redis_client.get("fp-sell"),
        redis_client.get("fp-buy"),
        redis_client.get("fp-lastupdate"),
    )

    sell_top = _load_station_list(sell_raw)
    buy_top = _load_station_list(buy_raw)
    last_update_value = last_update or ""

    result = MarketIndexResponse(
        sell_top=sell_top,
        buy_top=buy_top,
        last_update=last_update_value,
    )
    return ResponseUtil.success(model_content=result)


__all__ = ["market_router"]
