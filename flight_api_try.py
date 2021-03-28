"""
API Documentation:
https://developers.amadeus.com/self-service/apis-docs/guides/authorization-262
The amadeus API gives a cURL example, the below link explains how to 
translate to Python requests
https://stackoverflow.com/questions/60412783/transform-curl-oauth2-to-python-script


plane fare tax == 7.5

"""
from decouple import config
import requests
import json

client_secret = config('amadeus_secret')
client_id = config('amadeus_client')

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

departure, destination, departure_date, return_date = input("Enter departing "
                                                            "airport (ex: DCA),"
                                                            "arrival airport, "
                                                            "departure date (YYYY-MM-DD)"
                                                            "and return date: ").split()

# url request access_token
url = "https://test.api.amadeus.com/v1/security/oauth2/token" 

params = {
    "client_secret": client_secret, # SECRET_KEY
    "grant_type": "client_credentials",
    "client_id": client_id # API_KEY
}
# make request
response = requests.post(url, data=params)


#print(response.json()['access_token']) # just the token 
print(response.json())

# put my credentials in variable
headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
print(headers)

going_url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={departure}&destinationLocationCode={destination}&currencyCode=USD&departureDate={departure_date}&adults=1&max=2"


returning_url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={destination}&destinationLocationCode={departure}&currencyCode=USD&departureDate={return_date}&adults=1&max=2"
# make query 
going = requests.get(going_url, headers=headers)

returning = requests.get(returning_url, headers=headers)

print("\n\n\nHere's the response:\n\n\nDeparting info:\n\n\n")

jprint(going.json())

print("Returning info:\n\n\n")
jprint(returning.json())

print(f"\n\n\nThe estimated cost for one adult ticket from {departure} to {destination} on {departure_date} is: \n${going.json()['data'][0]['price']['grandTotal']}\n\n\n")

#print(type())

print(f"\n\n\nThe estimated cost for one adult ticket from {destination} to {departure} on {return_date} is: \n${returning.json()['data'][0]['price']['grandTotal']}")


#jprint(going.json()['dictionaries']['carriers']) # prints one item dict with airline

for item in going.json()['dictionaries']['carriers']:
    going_airline = item

for item in returning.json()['dictionaries']['carriers']:
    returning_airline = item 

if going_airline == returning_airline:
    print("The airline is ",going.json()['dictionaries']['carriers'][going_airline])

else:
    print("The going airline is: \n")
    print(going.json()['dictionaries']['carriers'][going_airline])

    print("the returing airline is:\n")
    print(returning.json()['dictionaries']['carriers'][returning_airline])