"""
This is a file of helper functions. These fall into three categories:
    1. Fetching data from the respective API's
    2. Making calculations based both user input and API responses.
    3. Making estimated calculations on the Person objects as far as
    potential roster and room assignments based on roster
        a. room assignments depend on both gender and rank which are attributes
        of the Person object. 
"""

import json
from decouple import config
import requests
import random
from groups import blues_roster, crew, drivers

API_KEY = config('gsa_key')
CLIENT_SECRET = config('amadeus_secret')
CLIENT_ID = config('amadeus_client')
TOLL_GURU = config('toll_guru')

STATE_SALES_TAX = {"AL": 4.0, "AK": 0.0,"AZ": 5.6,
                    "AR": 6.5, "CA": 7.25, "CO": 2.9,
                    "CT": 6.35, "DE": 0.0,"FL": 6.0,
                    "GA": 4.0, "HI": 4.0, "ID": 6.0,
                    "IL": 6.25, "IN": 7.0, "IA": 6.0,
                    "KS": 6.5, "LA": 6.0, "ME": 4.45,
                    "MD": 6.0, "MA": 6.5, "MI": 6.0,
                    "MN": 6.875, "MS": 7.0, "MO": 4.225,
                    "MT": 0.0, "NE": 5.5, "NV": 6.85,
                    "NH": 0.0, "NJ": 6.625, "NM": 5.125,
                    "NY": 4.0, "NC": 4.75, "ND": 5.0,
                    "OH": 5.75, "OK": 4.5, "OR": 0.0,
                    "PA": 6.0, "RI": 7.0, "SC": 6.0,
                    "SD": 4.5, "TN": 7.0, "TX": 6.25,
                    "UT": 6.1, "VT": 6.0, "VA": 5.5,
                    "WA": 6.5, "WV": 6.0, "WI": 5.0, "WY": 4.0}

FLIGHT_TAX = 7.5
GOVT_FLIGHT_FLAT = 600  # use this fig. to pad flight info
DRIVER_OT = 50
WORK = '"Ft Myer, VA"'
WORK_STATE = 'VA'

def json_neat_print(data):
    '''
    a very simple function for neatly printing a json object to the console
    :param data: json raw data
    :return: formatted string of Python JSON object
    '''
    text = json.dumps(data, sort_keys=True, indent=4)
    print(text)

def sales_tax_calc(state, before_tax):
    '''
    given a state and a price before tax, calculate the full cost for a hotel
    booking, for example.
    :param state: Two letter state code (ex. MD, CA)
    :param before_tax: float price before tax
    :return price after tax (float)
    :return -1 for improper state formate
    '''
    if len(state) != 2:
        return -1   # state was not proper format
    elif state.upper() in STATE_SALES_TAX.keys():
        tax = (STATE_SALES_TAX.get(state.upper())/100)
        price_after_tax = (before_tax + (tax * before_tax))
    else:
        return None
    return price_after_tax

def flight_tax_calc(price):
    '''
    calculate the full cost of a flight estimate after tax given the list ticket
    price.
    :param price (float)
    :return price_after_tax (float)
    '''
    tax = FLIGHT_TAX/100
    price_after_tax = (price + (price * tax))
    return price_after_tax


def get_meals_lodging(city, state, year, month):
    '''
    contact gsa.gov's API to get the ME&I (Meals and Incidentals) and Lodging
    rates given the city, state, year and month of trip.
    :param city: any U.S. city, ex: Chicago, New-Orleans
    :param state: two letter code, ex: VA, MD, CA
    :param year: YYYY
    :param month: Mmm
    :return: daily meal and lodging rate per person
    '''

    response = requests.get(
            f"https://api.gsa.gov/travel/perdiem/v2/rates/city/{city}"
            f"/state/{state}/year/{year}?api_key={API_KEY}")
    if response.status_code == 200:
        try:
            all_data = response.json()['rates'][0]
            meal_rate = all_data['rate'][0]['meals']
            # lodging rates vary per month
            for m in all_data['rate'][0]["months"]["month"]:
                if m["short"] == month.title():
                    lodging_before_tax = m['value']
                    # add tax to lodging
                    lodging = sales_tax_calc(state, lodging_before_tax)
            return meal_rate, lodging
        except IndexError:  # hit the api with invalid inputs
            return None
    else:
        return None

def get_com_flight_price(departure, destination, departure_date, return_date):
    '''
    contact the amadeus commercial flight prices API to get an estimated
    plane fare cost given a departing airport code, destination airport code,
    and particularly formatted dates for departure and return.
    :param departing == 3 char Airport Code (ex: DCA, MDW, IAD)
    :param returning == 3 char Airport Code
    :param dep_date == departure date, format: YYYY-MM-DD
    :param ret_date == return date
    :return commercial rates: going_flight and airline, returning_flight
     and airline

    '''
    # url request access_token
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"

    params = {
        "client_secret": CLIENT_SECRET,  # SECRET_KEY
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID  # API_KEY
    }
    # make request
    response = requests.post(url, data=params)
    # put my credentials in variable
    headers = {"Authorization": f"Bearer {response.json()['access_token']}"}

    going_url = f"https://test.api.amadeus.com/v2/shopping/" \
                f"flight-offers?originLocationCode={departure}" \
                f"&destinationLocationCode={destination}&" \
                f"currencyCode=USD&departureDate={departure_date}&adults=1&max=2"

    returning_url = f"https://test.api.amadeus.com/v2/shopping/" \
                    f"flight-offers?originLocationCode={destination}" \
                    f"&destinationLocationCode={departure}" \
                    f"&currencyCode=USD&departureDate={return_date}" \
                    f"&adults=1&max=2"

    # make queries
    going = requests.get(going_url, headers=headers)
    returning = requests.get(returning_url, headers=headers)
    if going.status_code == 200 and returning.status_code == 200:
        try:
            going_before_tax = going.json()['data'][0]['price']['grandTotal']
            # price before tax
            going_flight = flight_tax_calc(float(going_before_tax))
            for airline in going.json()['dictionaries']['carriers']:
                going_airline = going.json()['dictionaries']['carriers'][airline]

            # returning flight info
            returning_before_tax = returning.json()['data'][0]['price']['grandTotal']
            # add tax
            returning_flight = flight_tax_calc(float(returning_before_tax))
            for airline in returning.json()['dictionaries']['carriers']:
                returning_airline = \
                    returning.json()['dictionaries']['carriers'][airline]
            return going_flight, going_airline, returning_flight, returning_airline
        except IndexError or KeyError:
            return None
    else:  # status code other than 200
        return None

def get_gov_flight(quantity_on_job, flight_rate=GOVT_FLIGHT_FLAT):
    '''
    using a flat, more expensive rate for government flights due to flexible
    cancellation policy, get an estimate for total plane fare cost given the
    constant and total personnel on the job.
    :param quantity_on_job is total members flying
    :param flight_rate is the rate for gov't ticket, higher than
    commercial because of flexible change and cancellation
    :return quantity_on_job * flight_rate

    '''
    flight_rate = flight_rate
    total_personnel = int(quantity_on_job)
    return flight_rate*total_personnel

def get_crew(quantity_on_job):
    '''
    given the number of crew on the job, return a list of crew Person objects
    making sure both Seipp and Duarte are on every budget.
    :param quantity_on_job == number of tech on job
    :return list of tech members on job, always include female for price padding
    '''
    quantity = int(quantity_on_job)
    crew_on_job = []
    # below people always on budgets, Seipp is crew
    # leader and Duarte pads lodging fig.
    budget_constant_list = ['seipp', 'duarte']
    for person in budget_constant_list:
        for member in crew:
            if person.title() in member.last_name.title():
                crew_on_job.append(member)
    remainder = quantity - len(budget_constant_list)
    while remainder < quantity:
        num = random.randint(0, len(crew) - 1)
        for person in budget_constant_list:
            if crew[num].last_name.title() not in person.title() and\
                    crew[num] not in crew_on_job:
                crew_on_job.append(crew[num])
                remainder += 1
            else:
                continue
    if len(crew_on_job) > quantity:  # if there are too many in the list
        crew_on_job = crew_on_job[:quantity]
    return crew_on_job

# default to one, occassionally we'll need to override
def get_drivers(quantity_on_job='1'):
    '''
    Given a total number of drivers on job, return a list of driver Person
    objects
    :param quantity_on_job == number of drivers on job
    :return drivers
    '''
    quantity = int(quantity_on_job)
    job_drivers = []
    for i in range(quantity):
        job_drivers.append(drivers[i])
    return job_drivers

def get_driver_ot(quantity_on_job, total_hours, rate=DRIVER_OT):
    '''
    Given the number of drivers on the job, estimated over time hours to be
    clocked and the constant overtime rate, return an estimated dollar amount
    in driver overtime.
    :param quantity_on_job == number of drivers on job
    :param total_hours == estimated overtime hours
    :return total_overtime
    '''
    quantity = int(quantity_on_job)
    total_hours = float(total_hours)
    return quantity * total_hours * rate


def get_tolls(destination):
    '''
    contact the tollguru API with a particularly formatted starting point from
    the constant, WORK, and a destination. Returns a complex json object that
    may be parsed with the helper function json_extract() for toll and toll
    road information.
    :param destination format == City, 2-letter-state-code (i.e. Winchester, VA)
    :return complex json object
    '''
    try:
        city, state = destination.split(',')
    except ValueError:  # handle input with no commas
        state = destination
    destination = f'"{destination}"'
    url = "https://dev.tollguru.com/v1/calc/gmaps"

    payload = "{\"from\":{\"address\":" + WORK + "},\"to\":{\"address\":" \
              + destination + "},\"waypoints\":[{\"address\":" \
              + WORK + "},{\"address\":" + destination +\
              "}],\"vehicleType\":\"2AxlesAuto\",\"departure_time\":1551541566,"\
              "\"fuelPrice\":2.79,\"fuelPriceCurrency\":" \
              "\"USD\",\"fuelEfficiency\":" \
              "{\"city\":24,\"hwy\":30,\"units\":" \
              "\"mpg\"},\"driver\":{\"wage\":30,\"rounding\":" \
              "15,\"valueOfTime\":0}" \
              ",\"hos\":{\"rule\":60," \
              "\"dutyHoursBeforeEndOfWorkDay\":" \
              "11,\"dutyHoursBeforeRestBreak\":" \
              "7,\"drivingHoursBeforeEndOfWorkDay\":11," \
              "\"timeRemaining\":60},\"units\":{\"currencyUnit\":\"AUD\"}}"

    headers = {
        'content-type': "application/json",
        'x-api-key': TOLL_GURU
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_total_rooms(trip_personnel):
    '''
    return the total rooms needed given the trip personnel. Note: E9's,
    civilians (classified in the Person object as E9s), officers and females
    under E9 if singular instance get individual rooms. E8's and below
    share rooms.
    :param trip_personnel == list of person objects on trip
    :return total_rooms , accounting for doubled rooms
    :note E9's, Officers (Person.rank == 10), Civilians (ie. Drivers),
    and females under E8 if
    only one on trip get individual rooms. All else double rooms
    '''
    grunts = []  # males under E8
    sgms = []  # single rooms, E9's, Officers, Drivers
    females = []  # under E8

    for member in trip_personnel:
        if (int(member.rank) < 9) and (member.gender != 'female'):
            grunts.append(member)
        if (int(member.rank) < 9) and (member.gender == 'female'):
            females.append(member)
        if int(member.rank) >= 9:
            sgms.append(member)

    # female_rooms is for female NCO's E8 and below
    female_rooms = 0
    if females:
        if len(females) > 2:
            # female_rooms is len(females) // 2 + len(females) % 2
            doubled_ftuple = divmod(len(females), 2)
            female_rooms = doubled_ftuple[0] + doubled_ftuple[1]

        else:
            female_rooms = 1

    if female_rooms:
        if female_rooms == 1:
            doubled_tuple = divmod(len(grunts), 2)
            # doubled_rooms is len(grunts) // 2 + len(grunts) % 2
            # for male E8 and under
            doubled_rooms = doubled_tuple[0] + doubled_tuple[1]
            # For E9's, Officers and Drivers and female single room
            single_rooms = (len(sgms) + female_rooms)
            total_rooms = single_rooms + doubled_rooms + female_rooms

    else:
        doubled_tuple = divmod(len(grunts), 2)
        # for male E8 and under plus female_rooms
        doubled_rooms = doubled_tuple[0] + doubled_tuple[1] + female_rooms
        single_rooms = len(sgms)  # For E9's, Officers and Drivers
        total_rooms = single_rooms + doubled_rooms + female_rooms

    return total_rooms

def json_extract(obj, key):
    """
    This code is an elegant solution for recursively parsing a complex json
    object by Todd Birchard of the 'Hackers and Slackers' blog. See the
    code snippet 'extract.py' within the below link to reference the source
    directly.

    https://hackersandslackers.com/extract-data-from-complex-json-python/

    """
    arr = []  # great way to handle mutable argument,
    # ensure it's cleared each time functions called

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

if __name__ =='__main__':
    try:
        # meals and lodging
        city, state, year, month = input(
        "Enter city (ex: Chicago, New-Orleans), state(ex: VA),"
        " and year(YYYY) and month(Mmm):  ").split(', ')
        print(city, state, year, month)
        meal_rate, lodging = get_meals_lodging(city, state, year, month)
        print(f"\nThe daily meal rate for {city}, {state}, "
              f"in {month}, {year} is ${meal_rate}\n\n")
        print(f"The daily lodging rate for {city}, {state},"
              f" in {month}, {year} is ${lodging:.2f}")
        # commercial flights
        departure, destination, departure_date, return_date = \
                                                    input("Enter departing "
                                                    "airport (ex: DCA),"
                                                    "arrival airport, "
                                                    "departure date (YYYY-MM-DD)"
                                                    "and return date: ").split(', ')
        going_flight, going_airline, returning_flight, returning_airline = \
                                                    get_com_flight_price(
                                                    departure, destination,
                                                    departure_date, return_date)
        print(
            f"\n\n\nThe estimated cost for one adult ticket from "
            f"{departure} to {destination} on {departure_date} is: "
            f"\n${going_flight:.2f} on {going_airline}\n\n\n")

        print(
            f"\n\n\nThe estimated cost for one adult ticket from  "
            f"{destination} to {departure} on {return_date} is: "
            f"\n${returning_flight:.2f} on {returning_airline}")
        # get crew on job
        quantity_on_job = input("How many crew members on this trip?: ")
        crew_on_job = get_crew(int(quantity_on_job))
        print("Crew members on this job:\n")
        for member in crew_on_job:
            print(
                f"{member.first_name.title()}, {member.last_name.title()}, "
                f"E{member.rank}, {member.job.title()}, {member.gender}")
        # get toll info
        destination = input("Enter destination City and "
                            "State (ie: Winchester, VA): ")
        tolls_obj = get_tolls(destination)
        json_neat_print(tolls_obj)
        # just curious don't really need
        has_tolls = json_extract(tolls_obj, "hasTolls")
        print(has_tolls)
        toll_roads = json_extract(tolls_obj, "road")
        toll_prices = json_extract(tolls_obj, "tagCost")
        print(f"Toll roads: {set(toll_roads)}")  # eliminate duplicate values
        print(f"Itemized tolls: {toll_prices}")
        print(f"Total tolls: {sum(toll_prices):,.2f}")

        # get drivers
        quantity_drivers_on_job = input("How many drivers on this job?: ")
        estimated_ot_hours = input("What's the estimated driver OT hours?: ")
        drivers_on_job = get_drivers(quantity_drivers_on_job)
        print("Drivers:")
        for driver in drivers_on_job:
            print(
                f"{driver.first_name.title()}, {driver.last_name.title()}")
        estimated_driver_ot = get_driver_ot(quantity_drivers_on_job,
                                            estimated_ot_hours)
        print(f"Estimated driver OT: ${estimated_driver_ot:,.2f}")

        # assign trip_personnel, total people on trip
        trip_personnel = blues_roster + crew_on_job + drivers_on_job

        # get total rooms with doubled rooms
        total_rooms = get_total_rooms(trip_personnel)
        print(f"Out of {len(trip_personnel)} people "
              f"we need {total_rooms} rooms for doubling rooms.")

        # get gov't flight rate
        quantity_on_job = input("Personnel Total flying?: ")
        # Get gov't flight padded figure
        gov_rate_flight_total = get_gov_flight(quantity_on_job)
        print(f"Padded figure for {quantity_on_job} people at "
              f"${GOVT_FLIGHT_FLAT} per person totaling "
              f"${gov_rate_flight_total:,}")


    except Exception as e:
        print(f"Python Error: {e}")
