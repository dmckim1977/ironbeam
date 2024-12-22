import logging
import os

from dotenv import load_dotenv

import ironbeam as ib

load_dotenv()

logging.basicConfig(level=logging.INFO)

# # Using apikey in query params
client = ib.Ironbeam(apikey=os.getenv("IRONBEAM_APIKEY"))
client.authorize(username=os.getenv("IRONBEAM_USERNAME"))

# Trader Info
trader_info = client.info.get_trader_info(bearer_token=client.token)
print(f"Accounts: {trader_info.accounts}")
print(f"Trader ID: {trader_info.trader_id}")
print(f"Is Live: {trader_info.is_live}")

# User Info
user_info = client.info.get_user_info(bearer_token=client.token)
print(f"Account Title: {user_info.account_title}")
print(f"Accounts: {user_info.accounts}")
print(f"Email: {user_info.email_address1}")

# Security definitions
security_defs = client.info.get_security_definitions(
    symbols=["XCME:ES.H25"], bearer_token=client.token
)

for definition in security_defs.security_definitions:
    print(f"Symbol: {definition.symbol}")
    print(f"Product: {definition.product_description}")
    print(f"Market Group: {definition.market_group}")
    print(f"Expiration: {definition.get_expiration_time()}")

# Margin information
margin_info = client.info.get_security_margin(
    symbols=["XCME:ES.H25", "XCME:NQ.H25"], bearer_token=client.token
)

df = margin_info.to_pandas()

# Main margin information
print("Margin Info:")
print(df)

# Schedule details if any
print("\nSchedule Details:")
print(df)
