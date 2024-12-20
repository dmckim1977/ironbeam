import logging
import os

from dotenv import load_dotenv

import ironbeam as ib

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

auth = ib.Auth(username=os.getenv("IRONBEAM_USERNAME"),
               apikey=os.getenv("IRONBEAM_APIKEY"))

print(auth.username)
print(auth.apikey)

token = auth.authorize()

print(token)
print(auth.token)

auth.save_token()
