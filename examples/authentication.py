import logging
import os

from dotenv import load_dotenv

import ironbeam as ib

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

# # Basic usage
client = ib.Ironbeam(apikey=os.getenv("IRONBEAM_APIKEY"))
client.authorize(username=os.getenv("IRONBEAM_USERNAME"))
print(client.token)
# Use client...
client.logout()

# Context manager usage
with ib.Ironbeam(apikey=os.getenv("IRONBEAM_APIKEY")) as client:
    client.authorize(username=os.getenv("IRONBEAM_USERNAME"))
    # Use client...
    # Auto logout on exit
