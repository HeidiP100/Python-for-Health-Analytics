import requests

YEAR = 2020
DATASET = "dec/pl"
URL = (f"https://api.census.gov/data/{YEAR}/{DATASET}")
API_KEY = "7d0327180a3169ad783e4b028f83387fcd8d2c60"

state_code = input(
    "Enter the State FIPS code that you would like data for: "
)

variables = input(
    "Enter the variable names that you would like data for: "
)

params = {
    "get": variables,
    "for": f"state:{state_code}",
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

print(f"Found {len(data) - 1} Rows of Data.")

for i in data:
    print(i)