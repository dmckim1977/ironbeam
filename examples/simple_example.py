import logging
import os

import httpx
from dotenv import load_dotenv

import ironbeam as ib

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

client = ib.Ironbeam(apikey=os.getenv("IRONBEAM_APIKEY"))
client.authorize(username=os.getenv("IRONBEAM_USERNAME"))
print(client.token)

# Test with just a simple request to see what's happening
mode = "demo"
base_url = f"https://{'demo' if mode == 'demo' else 'live'}.ironbeamapi.com/v2"

# Test 1: Try with array parameter
test1_params = {
    "symbols[]": ["XCME:ES.H25", "XCME:NQ.H25"]
}

# Test 2: Try with different encoding
test2_params = {
    "symbols": ["XCME:ES.H25", "XCME:NQ.H25"]
}

# Test 3: Try with semicolon separator
test3_params = {
    "symbols": "XCME:ES.H25;XCME:NQ.H25"
}

# Test each one:
headers = {"Authorization": f"Bearer {client.token}"}

for i, p in enumerate([test1_params, test2_params, test3_params], 1):
    try:
        response = httpx.get(
            f"{base_url}/market/quotes",
            params=p,
            headers=headers,
        )
        print(f"\nTest {i}:")
        print(f"Status: {response.status_code}")
        print(f"URL: {response.url}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error in test {i}: {e}")
