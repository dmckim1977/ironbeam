import logging
import os

from dotenv import load_dotenv

import ironbeam as ib

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

client = ib.Ironbeam()

print(client.apikey)

client.authorize(username=os.getenv("IRONBEAM_USERNAME"),
               apikey=os.getenv("IRONBEAM_APIKEY"))

print(client.token)


# auth.save_token()

# client.logout()
