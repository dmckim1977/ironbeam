import logging
import os

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
quotes_response = client.market.get_quotes(["XCME:NQ.H25", "XCME:ES.H25"],
                                           bearer_token=client.token)

# Get as pandas DataFrame with readable columns
df = quotes_response.to_pandas()
print(df)
