import logging
import os

from dotenv import load_dotenv

import ironbeam as ib

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

client = ib.Historical(username=os.getenv("IRONBEAM_USERNAME"),
                       apikey=os.getenv("IRONBEAM_APIKEY"))

print(client.username)
print(client.apikey)
token = client.authorize()
print(token)
