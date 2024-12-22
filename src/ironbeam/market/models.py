from datetime import datetime
from typing import List, Optional

import pandas as pd
from pydantic import BaseModel, Field, field_validator

from ironbeam.exceptions import IronbeamResponseError


class Quote(BaseModel):
    """Represents a single quote from the market data."""

    symbol: str = Field(..., alias="s")
    last_price: float = Field(..., alias="l")
    last_size: int = Field(..., alias="sz")
    change: float = Field(..., alias="ch")
    open: float = Field(..., alias="op")
    high: float = Field(..., alias="hi")
    low: float = Field(..., alias="lo")
    aggressor_side: str = Field(..., alias="ags")
    tick_direction: str = Field(..., alias="td")
    settlement: float = Field(..., alias="stt")
    settlement_date: str = Field(..., alias="stts")
    settlement_timestamp: int = Field(..., alias="sttst")
    prev_settlement: float = Field(..., alias="pstt")
    prev_settlement_date: str = Field(..., alias="pstts")
    settlement_change: float = Field(..., alias="sttch")
    high_bid: float = Field(..., alias="hb")
    low_ask: float = Field(..., alias="la")
    bid: float = Field(..., alias="b")
    bid_timestamp: int = Field(..., alias="bt")
    bid_size: int = Field(..., alias="bs")
    implied_bid_count: int = Field(..., alias="ibc")
    ask: float = Field(..., alias="a")
    ask_timestamp: int = Field(..., alias="at")
    ask_size: int = Field(..., alias="as")
    trade_timestamp: int = Field(..., alias="tt")
    trade_date: str = Field(..., alias="tdt")
    security_status: str = Field(..., alias="secs")
    session_date: str = Field(..., alias="sdt")
    open_interest: int = Field(..., alias="oi")
    total_volume: int = Field(..., alias="tv")
    block_volume: int = Field(..., alias="bv")
    physical_volume: int = Field(..., alias="pv")

    def to_dict(self):
        """Convert to dict with human-readable timestamps."""
        data = self.model_dump()
        # Convert timestamps to datetime
        for field in [
            "bid_timestamp",
            "ask_timestamp",
            "trade_timestamp",
            "settlement_timestamp",
        ]:
            if data[field]:
                data[field] = datetime.fromtimestamp(data[field] / 1000)
        return data


class QuoteResponse(BaseModel):
    """Response from the quotes endpoint."""

    quotes: List[Quote]
    status: str
    message: str

    def to_pandas(self) -> pd.DataFrame:
        """Convert quotes to a pandas DataFrame with readable column names."""
        if not self.quotes:
            return pd.DataFrame()

        # Convert each quote to a dict with processed timestamps
        data = [quote.to_dict() for quote in self.quotes]
        return pd.DataFrame(data)


class QuoteRequest(BaseModel):
    """Validation model for quote requests."""

    symbols: List[str] = Field(..., min_length=1, max_items=10)

    @field_validator("symbols")
    def validate_symbols(cls, v):
        # Validate each symbol format (you might want to add more specific validation)
        for symbol in v:
            if ":" not in symbol:
                raise ValueError(
                    f"Invalid symbol format: {symbol}. "
                    f"Expected format: EXCHANGE:SYMBOL.CONTRACTCODE"
                )
        return v


class DepthLevel(BaseModel):
    """Individual level in the depth of market."""

    level: int = Field(..., alias="l")
    timestamp: int = Field(..., alias="t")
    side: str = Field(..., alias="s")  # 'B' for bid, 'A' for ask
    price: float = Field(..., alias="p")
    orders: int = Field(..., alias="o")
    size: float = Field(..., alias="sz")
    implied_orders: Optional[int] = Field(None, alias="ioc")
    implied_size: Optional[float] = Field(None, alias="is")

    def to_dict(self):
        """Convert to dict with human-readable timestamp."""
        data = self.model_dump(exclude_none=True)  # Exclude fields that are None
        if data["timestamp"]:
            data["timestamp"] = datetime.fromtimestamp(data["timestamp"] / 1000)
        return data


class Depth(BaseModel):
    """Depth data for a single symbol."""

    symbol: str = Field(..., alias="s")
    bids: List[DepthLevel] = Field(..., alias="b")
    asks: List[DepthLevel] = Field(..., alias="a")

    def to_dataframe(self) -> pd.DataFrame:
        """Convert depth to a pandas DataFrame."""
        bid_data = [{"side": "bid", **level.to_dict()} for level in self.bids]
        ask_data = [{"side": "ask", **level.to_dict()} for level in self.asks]

        df = pd.DataFrame(bid_data + ask_data)
        if not df.empty:
            # Sort by price descending for bids, ascending for asks
            df = df.sort_values(by=["side", "price"], ascending=["side" == "ask", True])
        return df


class DepthResponse(BaseModel):
    """Response from the depth endpoint."""

    depths: List[Depth] = Field(..., alias="depths")  # Changed from 'Depths'
    status: str
    message: str
    error1: Optional[str] = None

    @field_validator("status")
    def check_status(cls, v, values):
        if v == "ERROR":
            error = values.get("error1") or values.get("message")
            raise IronbeamResponseError(
                status=v, message=values.get("message"), error=error
            )
        return v

    def to_pandas(self) -> dict[str, pd.DataFrame]:
        """
        Convert depths to pandas DataFrames.

        Returns:
            dict: Symbol -> DataFrame mapping for all depth data
        """
        return {depth.symbol: depth.to_dataframe() for depth in self.depths}


class Trade(BaseModel):
    """Individual trade data."""

    symbol: str
    price: float
    size: float
    send_time: int = Field(..., alias="sendTime")
    tick_direction: str = Field(..., alias="tickDirection")
    aggressor_side: str = Field(..., alias="aggressorSide")
    trade_date: str = Field(..., alias="tradeDate")
    total_volume: float = Field(..., alias="totalVolume")
    change: Optional[float] = None
    sequence_number: Optional[int] = Field(None, alias="sequenceNumber")
    trade_id: Optional[int] = Field(None, alias="tradeId")

    def to_dict(self):
        """Convert to dict with human-readable timestamp."""
        data = self.model_dump(exclude_none=True)  # Exclude None values
        if data["send_time"]:
            data["send_time"] = datetime.fromtimestamp(data["send_time"] / 1000)
        return data


class TradesResponse(BaseModel):
    """Response from the trades endpoint."""

    traders: List[Trade]  # Field name from API response
    status: str
    message: str
    error1: Optional[str] = None

    @field_validator("status")
    def check_status(cls, v, values):
        if v == "ERROR":
            error = values.get("error1") or values.get("message")
            raise IronbeamResponseError(
                status=v, message=values.get("message"), error=error
            )
        return v

    def to_pandas(self) -> pd.DataFrame:
        """Convert trades to a pandas DataFrame."""
        if not self.traders:
            return pd.DataFrame()

        data = [trade.to_dict() for trade in self.traders]
        return pd.DataFrame(data)
