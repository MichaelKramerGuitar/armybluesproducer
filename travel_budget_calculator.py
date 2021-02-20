"""
Postconditions:
1. Intake how many crew and which crew
2. Intake Lodging rate
3. Intake meal locality rate
4. Intake number of days of trip
5. Intake Driver overtime hours
6. Intake Tolls
7. Print Cost breakdown to the console for Individual Rooms
OR cost for consolidated rooms depending on value of covid boolean
"""

from armybluesproducer_CLI.groups import blues_roster, crew, drivers

import datetime


tdy = input("What trip is this budget for? (for example, \"Midwest 2021\" or \"JEN 2023\"):\n")

crew_counter = 0
crew_query = input("How many crew members on this trip:\n")
crew_on_job = []

if crew_query.isnumeric():
    while crew_counter < int(crew_query):
        first_name = input(f'What\'s {crew_counter + 1} crew member\'s first name without punctuation?:\n')
        for member in crew:
            if first_name.lower() in member.first_name:
                crew_on_job.append(member)
                crew_counter += 1


print("Crew members on this job:\n")
for member in crew_on_job:
    print(f"{member.first_name.title()}, {member.last_name.title()}, E{member.rank}, {member.job.title()}, {member.gender}")
        
driver_counter = 0
driver_query = input("\nHow many drivers on this trip:\n")
drivers_on_job = []

if driver_query.isnumeric():
    while driver_counter < int(driver_query):
        first_name = input(f'What\'s {driver_counter + 1} driver\'s first name without punctuation?:\n')
        for member in drivers:
            if first_name.lower() in member.first_name:
                drivers_on_job.append(member)
                driver_counter += 1


room_cost = input("\nWhat does fedtravel.com say room fee is per person?: ")

sales_tax_query = input("\nWhat's the sales tax of the state in which you'll be staying? (just enter the integer and leave out \"%\" sign- if 6% please enter 6): ")
sales_tax = float(sales_tax_query)*.01

meal_cost = input("\nWhat does fedtravel.com say locality M&IE is per day (use full day number for each day of the trip to pad budget)?: ")
incidentals = input("\nWhat does fedtravel.com say Incedental Expenses are per day?: ")



plane_fare = input("\n'y' or 'n': Are you flying? ")
if 'y' in plane_fare:
    plane_fare = input("\nWhat does fedtravel.com say for price of one round trip ticket? ")

trip_duration = input("\nincluding travel days, how many days is this trip? ")

nights = input("\nHow many nights are you spending in a hotel? ")

if drivers_on_job:
    driver_ot = 50 # driver overtime for our purposes is always $50/hr

    driver_hours = input("\nApproximately how many hours total after 3pm and on weekends are the driver(s) going to be on the clock? ")

    tolls = input("\n'y' or 'n': Are there tolls? ")
    if 'y' in tolls:
        toll_price = input("\nHow much is one pass per vehicle (use the most expensive figure for padding)?: ")
        vehicles = input("\nHow many vehicles (busses/trucks) are we planning to take? ")
    else:
        toll_price = None


trip_personnel = blues_roster + crew_on_job + drivers_on_job # total people on trip

print(f'\nThere are {len(trip_personnel)} members on this trip, {tdy.title()} - here is the roster\n '
      f'***NOTE*** This is a mockup and subject to change, particularly crew personnel:\n')
for member in trip_personnel:
    print(f"{member.first_name.title()}, {member.last_name.title()}, E{member.rank}, {member.job.title()}, {member.gender.title()}")

grunts = []
sgms = []
females = []

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
        female_rooms = ((len(females)//2) + len(females))

    else:
        female_rooms = 1

if female_rooms:
    if female_rooms == 1:
        doubled_rooms = ((len(grunts)//2) + len(grunts)%2) # for male E8 and under
        print(f"\nTotal male NCO's E8 and below ({len(grunts)}) floor divided by 2 (throw out the remainder) + ({len(grunts)}%2), modulo operation, which will be 1 if E8's and below is an odd number\n"
              f" = ({(len(grunts)//2)} + {len(grunts)%2}) = Total doubled rooms: {doubled_rooms}")
        single_rooms = (len(sgms) + female_rooms)# For E9's, Officers and Drivers and female single room
        print(f"\nTotal single rooms for E9 and above ({len(sgms)}) + one room for female under E8: {single_rooms}")
        total_rooms = single_rooms + doubled_rooms + female_rooms

else:
    doubled_rooms = ((len(grunts)//2) + len(grunts)%2 + female_rooms) # for male pairs E8 and under and female pairs E8
    print(f"\nTotal male NCO's E8 and below ({len(grunts)}) floor divided by 2 (throw out the remainder) + ({len(grunts)}%2), modulo operation, which will be 1 if E8's and below is an odd number\n"
        f" = ({(len(grunts) // 2)} + {len(grunts) % 2}) + female rooms ({female_rooms}) = Total doubled rooms: {doubled_rooms}")
    single_rooms = len(sgms)# For E9's, Officers and Drivers
    print(f"\nTotal single rooms E9 and above: {single_rooms}")
    total_rooms = single_rooms + doubled_rooms + female_rooms

print(f"\nTotal rooms for band in non-covid times =\n"
              f"doubled rooms ({doubled_rooms}) + single rooms ({single_rooms}) + female rooms ({female_rooms})\n"
              f"={total_rooms}")
print(f"\nTotal single rooms for the Blues in COVID times is {len(trip_personnel)}\n")
    


hotel_tax = int(room_cost)*float(sales_tax)
print(f"\nroom cost (${room_cost}) x sales tax (${sales_tax}) = hotel sales tax per room (${hotel_tax})")
normal_lodging = ((hotel_tax + float(room_cost))*int(nights)*total_rooms)
print(f"\nTOTAL LODGING cost for non-COVID room doubling scenario = \n"
f"(hotel tax per room (${hotel_tax}) + single room cost (${float(room_cost)})) x total nights ({int(nights)}) x total rooms ({total_rooms})\n"
f"= ${round(normal_lodging, 2)}")

covid_lodging = ((hotel_tax) + float(room_cost))*int(nights)*len(trip_personnel) # total lodging is room_cost plus tax times trip duration in days
print(f"\nTOTAL LODGING cost for INDIVIDUAL ROOMS =\n"
    f"(hotel sales tax per room(${hotel_tax}) + single room cost (${float(room_cost)})) x total nights ({int(nights)}) x total rooms ({len(trip_personnel)})\n"
    f"= ${round(covid_lodging, 2)}")

meals = ((float(meal_cost) + float(incidentals))*int(trip_duration)*len(trip_personnel)) # meals is locality plus govt times trip duration in days times number of people

print(f"\nTotal cost for meals =\n" 
 f"(M&IE (${float(meal_cost)}) + incidentals (${incidentals})) x days in the trip ({int(trip_duration)}) x quantity of people ({len(trip_personnel)})\n"
f"= ${round(meals, 2)}\n"
      "***NOTE***\n"
      "this budget is only calculating full days meal cost to pad the figure\n")

if drivers_on_job:
    driver_overtime = (int(driver_hours)*driver_ot*len(drivers_on_job)) # total driver overtime is approximate overtime hours at $50/hr times number of drivers on job
    print(f"\ntotal driver overtime =\n"
          f"estimated driver OT hours ({int(driver_hours)}) x driver OT rate (${driver_ot}) x quantity of drivers({len(drivers_on_job)})\n"
            f"= ${driver_overtime}")

    if toll_price:
        toll_cost = (float(toll_price)*2*int(vehicles)) # total toll cost is price per toll times 2 (round trip) times the number of vehicles we're taking
        print(f"\nTotal cost for tolls =\n"
              f"toll cost (${float(toll_price)}) x round trip (2) x number of vehicles ({int(vehicles)})\n"
                f"${round(toll_cost, 2)}")

        normal_budget = (normal_lodging + meals + toll_cost + driver_overtime)
        covid_budget = (covid_lodging + meals + toll_cost + driver_overtime)
        print("\n\n"
              "NON-COVID BREAKDOWN:\n"
              f"shared rooms lodging (${normal_lodging}) + meals (${meals}) + tolls (${toll_cost}) + Driver OT (${driver_overtime})\n"
              f"NON-COVID TOTAL = ${round(normal_budget, 2)}")

        print("\n\n"
              "COVID BREAKDOWN:\n"
              f"single rooms lodging (${covid_lodging}) + meals (${meals}) + tolls (${toll_cost}) + Driver OT (${driver_overtime})\n"
              f"NON-COVID TOTAL = ${round(covid_budget, 2)}")

if 'n' not in plane_fare:
    if drivers_on_job:
        air_fare = (int(plane_fare)*len(trip_personnel))
        print(f"\nTotal air fare is =\n"
              f"price per round trip ticket (${int(plane_fare)}) x total tickets (${len(trip_personnel)})\n"
        f"= ${round(air_fare, 2)}")

        normal_budget = (normal_lodging + meals + float(plane_fare) + float(driver_overtime))
        covid_budget = (covid_lodging + meals + float(plane_fare) + float(driver_overtime))
        print(f"\n\n"
              "NON COVID BREAKDOWN:\n"
              f"shared room total (${normal_lodging}) + meals (${meals}) + total plane fare (${float(plane_fare)}) + driver OT (${float(driver_overtime)})\n"
            f"TOTAL =  ${round(normal_budget, 2)}")

        print(f"\n\n"
              "COVID BREAKDOWN:\n" 
              f"single room total (${covid_lodging}) + meals (${meals}) + total plane fare (${float(plane_fare)}) + driver OT (${float(driver_overtime)})\n" 
              f"TOTAL =  ${round(covid_budget, 2)}")
    else:
        air_fare = (int(plane_fare) * len(trip_personnel))
        print(f"\nTotal air fare is =\n"
              f"price per round trip ticket (${int(plane_fare)}) x total tickets (${len(trip_personnel)})\n"
              f"= ${round(air_fare, 2)}")

        normal_budget = (normal_lodging + meals + float(air_fare))
        print(f"\n\n"
              "NON COVID BREAKDOWN:\n"
              f"shared rooms (${normal_lodging}) + meals (${meals}) + total plane fare (${air_fare})\n"
            f"NON-COVID TOTAL = ${round(normal_budget, 2)}")

        covid_budget = (covid_lodging + meals + float(air_fare))
        print(f"\n\n"
              "COVID BREAKDOWN:\n"
              f"individual rooms (${round(covid_lodging, 2)}) + meals (${meals}) + total plane fare (${air_fare})\n"
              f"COVID TOTAL = ${round(covid_budget, 2)}")

today = datetime.date.today()
print(f"\n\nthis budget was made for {tdy.title()}, on {today.month}/{today.day}/{today.year}")