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

### For distancing protocol, single rooms
covid = True

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
    print(f"{member.first_name.title()}, {member.last_name.title()}, E{member.rank}, {member.job}, {member.gender}")
        
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
                
md_sales_tax = .06               
room_cost = input("\nWhat does fedtravel.com say room fee is per person?: ")

govt_meal = 14.05
meal_cost = input("\nWhat does fedtravel.com say locality M&IE is per day (use full day number for each day of the trip to pad budget)?: ")

tolls = input("\n'y' or 'n': Are there tolls? ")
if 'y' in tolls:
    toll_price = input("\nHow much is one pass per vehicle (use the most expensive figure for padding)?: ")
    vehicles = input("\nHow many vehicles (busses/trucks) are we planning to take? ")
else:
    toll_price = None

plane_fare = input("\n'y' or 'n': Are you flying? ")
if 'y' in plane_fare:
    plane_fare = input("\nWhat does fedtravel.com say for price of one round trip ticket? ")

trip_duration = input("\nincluding travel days, how many days is this trip? ")

nights = input("\nHow many nights are you spending in a hotel? ")

driver_hours = input("\nApproximately how many hours total after 3pm and on weekends are the driver(s) going to be on the clock? ")
                
driver_ot = 50


trip_personnel = blues_roster + crew_on_job + drivers_on_job # total people on trip

print(f'\nThere are {len(trip_personnel)} members on this trip - here is the roster:\n')
for member in trip_personnel:
    print(f"{member.first_name.title()}, {member.last_name.title()}, E{member.rank}, {member.job}, {member.gender}")

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
if len(females) > 2:
    female_rooms = ((len(females)//2) + len(females))

else:
    female_rooms = 1


if female_rooms == 1:                            
    doubled_rooms = ((len(grunts)//2) + len(grunts)%2) # for male E8 and under
    print(f"\nTotal doubled rooms: {doubled_rooms}")
    single_rooms = (len(sgms) + female_rooms)# For E9's, Officers and Drivers and female single room
    print(f"\nTotal single rooms, one is for a female under E8: {single_rooms}")
    total_rooms = single_rooms + doubled_rooms + female_rooms
else:
    doubled_rooms = ((len(grunts)//2) + len(grunts)%2 + female_rooms) # for male pairs E8 and under and female pairs E8
    print(f"\nTotal doubled rooms: {doubled_rooms}")
    single_rooms = len(sgms)# For E9's, Officers and Drivers
    print(f"\nTotal single rooms: {single_rooms}")
    total_rooms = single_rooms + doubled_rooms + female_rooms

print(f"\nTotal rooms for band in non-covid times: {total_rooms}")
print(f"\nTotal single rooms for the Blues in COVID times is {len(trip_personnel)}")
    


hotel_tax = int(room_cost)*md_sales_tax
if covid:
    lodging = ((hotel_tax) + float(room_cost))*int(nights)*len(trip_personnel) # total lodging is room_cost plus tax times trip duration in days
    print(f"\nTotal lodging cost for INDIVIDUAL ROOMS: ${lodging}")

else:
    lodging = ((hotel_tax + float(room_cost))*int(nights)*total_rooms)
    print(f"\nTotal lodging cost for non-COVID room doubling scenario: ${lodging}")

meals = ((float(meal_cost) + govt_meal)*int(trip_duration)*len(trip_personnel)) # meals is locality plus govt times trip duration in days times number of people

print(f"Total cost for meals: ${meals}") 

driver_overtime = (int(driver_hours)*driver_ot*len(drivers_on_job)) # total driver overtime is approximate overtime hours at $50/hr times number of drivers on job
print(f"total driver overtime: ${driver_overtime}")

if toll_price:
    toll_cost = (float(toll_price)*2*int(vehicles)) # total toll cost is price per toll times 2 (round trip) times the number of vehicles we're taking
    print(f"Total cost for tolls: ${toll_cost}")

    budget = (lodging + meals + toll_cost + driver_overtime)
    print(f"\n\nTOTAL: ${budget}")

if 'n' not in plane_fare:
    air_fare = (int(plane_fare)*len(trip_personnel))
    print(f"Total air fare is: ${air_fare}")

    budget = (lodging + meals + float(plane_fare) + float(driver_overtime))
    print(f"\n\nTOTAL: ${budget}")