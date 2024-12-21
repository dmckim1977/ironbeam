from datetime import datetime
from typing import List

import pandas as pd
from pydantic import BaseModel, Field, validator


class Quote(BaseModel):
    """Represents a single quote from the market data."""
    symbol: str = Field(..., alias='s')
    last_price: float = Field(..., alias='l')
    last_size: int = Field(..., alias='sz')
    change: float = Field(..., alias='ch')
    open: float = Field(..., alias='op')
    high: float = Field(..., alias='hi')
    low: float = Field(..., alias='lo')
    aggressor_side: str = Field(..., alias='ags')
    tick_direction: str = Field(..., alias='td')
    settlement: float = Field(..., alias='stt')
    settlement_date: str = Field(..., alias='stts')
    settlement_timestamp: int = Field(..., alias='sttst')
    prev_settlement: float = Field(..., alias='pstt')
    prev_settlement_date: str = Field(..., alias='pstts')
    settlement_change: float = Field(..., alias='sttch')
    high_bid: float = Field(..., alias='hb')
    low_ask: float = Field(..., alias='la')
    bid: float = Field(..., alias='b')
    bid_timestamp: int = Field(..., alias='bt')
    bid_size: int = Field(..., alias='bs')
    implied_bid_count: int = Field(..., alias='ibc')
    ask: float = Field(..., alias='a')
    ask_timestamp: int = Field(..., alias='at')
    ask_size: int = Field(..., alias='as')
    trade_timestamp: int = Field(..., alias='tt')
    trade_date: str = Field(..., alias='tdt')
    security_status: str = Field(..., alias='secs')
    session_date: str = Field(..., alias='sdt')
    open_interest: int = Field(..., alias='oi')
    total_volume: int = Field(..., alias='tv')
    block_volume: int = Field(..., alias='bv')
    physical_volume: int = Field(..., alias='pv')

    def to_dict(self):
        """Convert to dict with human-readable timestamps."""
        data = self.model_dump()
        # Convert timestamps to datetime
        for field in ['bid_timestamp', 'ask_timestamp', 'trade_timestamp',
                      'settlement_timestamp']:
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
    symbols: List[str] = Field(..., min_items=1, max_items=10)

    @validator('symbols')
    def validate_symbols(cls, v):
        # Validate each symbol format (you might want to add more specific validation)
        for symbol in v:
            if ':' not in symbol:
                raise ValueError(
                    f"Invalid symbol format: {symbol}. Expected format: EXCHANGE:SYMBOL.CONTRACTCODE")
        return v
