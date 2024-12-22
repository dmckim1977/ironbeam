from datetime import datetime
from typing import List, Optional

import pandas as pd
from pydantic import BaseModel, Field, field_validator

from ironbeam.exceptions import IronbeamResponseError


class TraderInfo(BaseModel):
    """Response model for trader info endpoint."""

    accounts: List[str]  # List of account IDs
    is_live: bool = Field(..., alias="isLive")
    trader_id: str = Field(..., alias="traderId")
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


class UserInfo(BaseModel):
    """Response model for user info endpoint."""

    account_category: Optional[int] = Field(None, alias="accountCategory")
    account_title: Optional[str] = Field(None, alias="accountTitle")
    email_address1: Optional[str] = Field(None, alias="emailAddress1")
    email_address2: Optional[str] = Field(None, alias="emailAddress2")
    group: Optional[str] = None
    is_clearing_account: Optional[bool] = Field(None, alias="isClearingAccount")
    phone1: Optional[str] = None
    phone2: Optional[str] = None
    sub_group: Optional[str] = Field(None, alias="subGroup")
    accounts: List[str]
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


class SecurityDefinitionLeg(BaseModel):
    """Individual leg of a security definition."""

    symbol: str
    ratio: int
    side: str
    security_id: str = Field(..., alias="securityId")
    exchange: str
    leg_exchange_symbol: str = Field(..., alias="legExchangeSymbol")


class SecurityDefinition(BaseModel):
    """Detailed security definition information."""

    symbol: str = Field(..., alias="exchSym")
    exchange_source: str = Field(..., alias="exchangeSource")
    activation_time: Optional[int] = Field(None, alias="activationTime")
    expiration_time: Optional[int] = Field(None, alias="expirationTime")
    market_complex: str = Field(..., alias="marketComplex")
    market_group: str = Field(..., alias="marketGroup")
    market_symbol: str = Field(..., alias="marketSymbol")
    cfi_code: Optional[str] = Field(None, alias="cfiCode")
    allow_open_orders: bool = Field(..., alias="allowOpenOrders")
    maturity_month: Optional[int] = Field(None, alias="maturityMonth")
    maturity_year: Optional[int] = Field(None, alias="maturityYear")
    product_description: Optional[str] = Field(None, alias="productDescription")
    security_type: str = Field(..., alias="securityType")
    security_id: str = Field(..., alias="securityId")
    legs: Optional[List[SecurityDefinitionLeg]] = None
    depth_levels: Optional[int] = Field(None, alias="depthLevels")
    min_price_increment: Optional[float] = Field(None, alias="minPriceIncrement")
    reg_code: Optional[str] = Field(None, alias="regCode")
    currency_code: str = Field(..., alias="currencyCode")
    display_factor: Optional[float] = Field(None, alias="displayFactor")
    allow_trading: bool = Field(..., alias="allowTrading")
    exchange_symbol: Optional[str] = Field(None, alias="exchangeSymbol")
    creation_date: Optional[int] = Field(None, alias="creationDate")

    def get_activation_time(self) -> Optional[datetime]:
        """Convert activation_time to datetime."""
        return (
            datetime.fromtimestamp(self.activation_time / 1000)
            if self.activation_time
            else None
        )

    def get_expiration_time(self) -> Optional[datetime]:
        """Convert expiration_time to datetime."""
        return (
            datetime.fromtimestamp(self.expiration_time / 1000)
            if self.expiration_time
            else None
        )

    def get_creation_date(self) -> Optional[datetime]:
        """Convert creation_date to datetime."""
        return (
            datetime.fromtimestamp(self.creation_date / 1000)
            if self.creation_date
            else None
        )


class SecurityDefinitionsResponse(BaseModel):
    """Response from the security definitions endpoint."""

    security_definitions: List[SecurityDefinition] = Field(
        ..., alias="securityDefinitions"
    )
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


class MarginScheduleDetail(BaseModel):
    """Margin schedule detail for a security."""

    start_time: int = Field(..., alias="startTime")
    end_time: int = Field(..., alias="endTime")
    margin: float

    def get_start_time(self) -> datetime:
        """Convert start_time to datetime."""
        return datetime.fromtimestamp(self.start_time / 1000)

    def get_end_time(self) -> datetime:
        """Convert end_time to datetime."""
        return datetime.fromtimestamp(self.end_time / 1000)


class SecurityMarginAndValue(BaseModel):
    """Security margin and value information."""

    symbol: str = Field(..., alias="exchSym")
    current_price: Optional[float] = Field(None, alias="currentPrice")
    current_time: Optional[int] = Field(None, alias="currentTime")
    current_value: Optional[float] = Field(None, alias="currentValue")
    initial_margin_long: Optional[float] = Field(None, alias="initialMarginLong")
    initial_margin_short: Optional[float] = Field(None, alias="initialMarginShort")
    maint_margin_long: Optional[float] = Field(None, alias="maintMarginLong")
    maint_margin_short: Optional[float] = Field(None, alias="maintMarginShort")
    span_settle_price: Optional[float] = Field(None, alias="spanSettlePrice")
    span_settle_value: Optional[float] = Field(None, alias="spanSettleValue")
    margin_schedule_details: Optional[List[MarginScheduleDetail]] = Field(
        None, alias="marginScheduleDetails"
    )

    def get_current_time(self) -> Optional[datetime]:
        """Convert current_time to datetime."""
        return (
            datetime.fromtimestamp(self.current_time / 1000)
            if self.current_time
            else None
        )


class SecurityMarginAndValueResponse(BaseModel):
    """Response from the security margin endpoint."""

    security_margin_and_values: List[SecurityMarginAndValue] = Field(
        ..., alias="securityMarginAndValues"
    )
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
        """
        Convert to a single DataFrame for margin information.

        Returns:
            DataFrame: Contains margin information for all securities
        """
        margin_data = []

        for security in self.security_margin_and_values:
            margin_dict = {
                "symbol": security.symbol,
                "current_price": security.current_price,
                "current_time": security.get_current_time(),
                "current_value": security.current_value,
                "initial_margin_long": security.initial_margin_long,
                "initial_margin_short": security.initial_margin_short,
                "maint_margin_long": security.maint_margin_long,
                "maint_margin_short": security.maint_margin_short,
                "span_settle_price": security.span_settle_price,
                "span_settle_value": security.span_settle_value,
            }
            margin_data.append(margin_dict)

        return pd.DataFrame(margin_data)
