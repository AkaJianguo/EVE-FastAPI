from typing import List

from pydantic import BaseModel, Field

from common.vo import ResponseBaseModel


class StationHotTop(BaseModel):
    order_count: int = Field(..., description="Order count")
    stationName: str = Field(..., description="Station name")
    stationID: int = Field(..., description="Station ID")
    total_volume: float = Field(..., description="Total volume")


class MarketIndexResponse(ResponseBaseModel):
    sell_top: List[StationHotTop] = Field(default_factory=list, description="Top sell stations")
    buy_top: List[StationHotTop] = Field(default_factory=list, description="Top buy stations")
    last_update: str = Field(default="", description="Last update timestamp")


__all__ = ["StationHotTop", "MarketIndexResponse"]
