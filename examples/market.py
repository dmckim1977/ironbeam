import logging
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

import ironbeam as ib
from ironbeam.exceptions import IronbeamAPIError, IronbeamResponseError

load_dotenv()

logging.basicConfig(level=logging.INFO)

# # Using apikey in query params
client = ib.Ironbeam(apikey=os.getenv("IRONBEAM_APIKEY"))
client.authorize(username=os.getenv("IRONBEAM_USERNAME"))

try:
    # This will fail validation
    quotes = client.market.get_quotes(["invalid_symbol"], bearer_token=client.token)
except ValueError as e:
    print(f"Validation error: {e}")
except IronbeamResponseError as e:
    print(f"API error: {e.status} - {e.message}")
except IronbeamAPIError as e:
    print(f"Request error: {e}")

try:
    # This will fail the max items check
    quotes = client.market.get_quotes(["XCME:ES.H25"] * 11, bearer_token=client.token)
except ValueError as e:
    print(f"Validation error: {e}")

# Get quotes response
quotes_response = client.market.get_quotes(
    ["XCME:NQ.H25", "XCME:ES.H25"], bearer_token=client.token
)

# Get as pandas DataFrame with readable columns
df = quotes_response.to_pandas()
print(df)

# Get depth for single or multiple symbols
depth = client.market.get_depth(symbols=["XCME:ES.H25"], bearer_token=client.token)

# Get as dict of DataFrames (one per symbol)
dfs = depth.to_pandas()

# Look at depth for first symbol
print(dfs["XCME:ES.H25"])

# Get trades for last hour
end_time = datetime.now()
start_time = end_time - timedelta(hours=40)

trades = client.market.get_trades(
    symbol="XCME:ES.H25",
    from_time=start_time,
    to_time=end_time,
    max_trades=100,
    bearer_token=client.token,
)

# print(trades)

# Convert to DataFrame
df = trades.to_pandas()
print(df.tail())
