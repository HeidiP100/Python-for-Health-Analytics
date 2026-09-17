import requests

YEAR = 2020
DATASET = "dec/pl"
URL = (f"https://api.census.gov/data/{YEAR}/{DATASET}")
API_KEY = "7d0327180a3169ad783e4b028f83387fcd8d2c60"

params = {
    "get": "NAME,P1_001N",
    "for": "state:*",
    "key": API_KEY,
}

response = requests.get(URL, params=params)

print(response)
if response.status_code != 200:
    print(f"Request failed ({response.status_code})")
    print(response.text)
    raise SystemExit(1)

response.raise_for_status()
data = response.json()

print(f"Got {len(data) - 1} rows back.")

for i in data:
    print(i)