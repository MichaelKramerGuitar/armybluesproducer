"""
https://www.dataquest.io/blog/python-api-tutorial/

https://realpython.com/python-json/
"""
from decouple import config
api_key = config('gsa_key')

import requests

import json

city, state, year, month = input("Enter city (ex: Chicago, New-Orleans), state(ex: VA), and year(YYYY) and month(Mmm):  ").split()

#response = requests.get(f"https://api.gsa.gov/travel/perdiem/v2/rates/city/{city}/state/{state}/year/{year}?api_key=7oANrDjl02Pf5iODnJ1GvDasiTXCkXtfWJNaypzu")
#response = requests.get("https://api.gsa.gov/travel/perdiem/v2/rates/city/Fairfax/state/VA/year/2019?api_key=7oANrDjl02Pf5iODnJ1GvDasiTXCkXtfWJNaypzu")
response = requests.get(f"https://api.gsa.gov/travel/perdiem/v2/rates/city/{city}/state/{state}/year/{year}?api_key=7{api_key}")
"""
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
"""
#jprint(response.json())

all_data = response.json()['rates'][0]

#jprint(all_data['rate'])

#print(f"the len of all_data'rate'is: {len(all_data['rate'])}")

print(f"\nThe daily meal rate for {city}, {state}, in {month}, {year} is ${all_data['rate'][0]['meals']}\n\n")

for m in all_data['rate'][0]["months"]["month"]:
    if m["short"] == month.title():
        print(f"The daily lodging rate for {city}, {state}, in {month}, {year} is ${m['value']}")

# =============================================================================
# for index, item in enumerate(all_months):
#     print(index, item)
# =============================================================================

# =============================================================================
# rates = all_months[2]
# 
# print(rates)
# =============================================================================

#meal_rate = response.json()['rate']

#print(meal_rate)

# =============================================================================
# print(response.json())
# print(response.status_code)
# =============================================================================

