"""
1. This file pertains to anything having to do with data entry from the app user.
2. The intake questionnaire is generated based on Question objects
3. A CompleteSurvey object is generated out of a collection of Questions
4. a CompleteBudget object is generated based on the data in a CompleteSurvey
5. There are additional functions below the class Objects grouped here
which help the these distinct classes interface with each other. These are:
    a. fetch_survey
        -read an existing survey from file back into memory to edit a response
    b. intake_questionnaire
        - generate questionnaire
        - ensure questionnaire input is appropriate per Question object type
    c. review_survey
        - display newly collected survey to the console for review
    d. budget_feeder
        - take a CompleteSurvey and generate a CompleteBudget based on info
        present in given survey.
        - write budget to file
"""


import os
from datetime import datetime
from functions import *
SEPARATOR = "*" * 80
TODAY = datetime.today()
meals_lodging_month_format = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# crew query has to be between 2 and 4
# driver query can't be > 2
questionnaire = {"title query": "what trip is this budget for? "
                                "(ex: Midwest, 2021 ex: JEN, 2022)",
                 "days query": "including travel days, how many days "
                                   "is this trip?",
                 "nights query": "how many nights in the hotel? "
                                 "(if none enter 0)",
                 "crew query": "how many crew on this trip? "
                               "(options: 2, 3 or 4)",
                 "driver query": "how many drivers on this trip? "
                                 "(options: 0, 1, or 2)",
                 "vehicle query": "how many vehicles are we taking on this "
                                  "on this trip? (options between 0 and 3)",
                 "driver ot query": "estimated driver ot hours? ",
                 "toll query": "for tolls: enter a destination city and "
                               "state (ex===> Winchester, VA"
                               " ex===> New York, NY)",
                 "flight query": "enter departing airport code "
                                 "arrival airport code, departure date "
                                 "and return date "
                                 "comma separated "
                                 "(ex===> DCA, MDW, 2021-12-14, 2021-12-17)",
                 "meals and lodging query": "Enter city "
                                            "(ex: Chicago, New-Orleans), "
                                            "state (ex: VA) and month (ex: Mmm) "
                                            "comma separated. "
                                            "(ex===> New-York, NY, 2021, Dec)",
                 }


class Question():
    """a question which can be used to:
        1. Prompt for input
        2. Store response to input
        3. return a response to question if one is stored in memory
    """
    def __init__(self, question):
        self.question = question
        self.response = ' '
        self.question_type = ' '

    def generate_question_type(self):
        for q_type in questionnaire.keys():
            if self.question == questionnaire.get(q_type):
                self.question_type = q_type
                return self.question_type

    def ask(self):
        # to prompt user
        return self.question

    def record_answer(self, answer):
        self.response = answer

    # reads a record back into memory
    def fetch_response(self, question):
        if isinstance(question, Question):
            return self.response
        else:
            return f"Error: no response recorded for {question}."

    def fetch_question_response(self, question):
        # return the question and response as a dict pair
        if isinstance(question, Question):
            return f"{self.question} : {self.response}"
        else:
            return f"Error: no response recorded for {question}."

    def __repr__(self):
        return f"Question(<question>)"


class CompleteSurvey():
    """
    a class that stores a complete survey read from memory as a dictionary
    """
    # this survey param is a simple dict_type, NOT a CompleteSurvey obj
    def __init__(self, survey):
        # survey is a dict with all questions as keys and answers as vals
        self.__survey = survey  # full dict
        self.title = survey['title query']
        self.days = survey['days query']  # days of trip
        self.nights = survey['nights query']  # nights in hotel
        self.crew = survey['crew query']
        self.drivers = survey['driver query']  # how many drivers on job
        self.vehicles = survey['vehicle query']
        self.driver_ot = survey['driver ot query']
        self.tolls = survey['toll query']
        self.flights = survey['flight query']
        self.meals_lodging = survey['meals and lodging query']

    # this is redundant to __getitem__
    def fetch_response(self, question):
        # get the answer to a specific question in the survey
        return self.__survey[question]

    def __generate_title(self):
        self.title = self.fetch_response('title query')

    def write_to_file(self):
        """
        Description: write intake data to file which will be read into main app
        :param survey: a dict of survey questions and corresponding
        user responses
        :return: error message if error
        """
        dir_name = os.getcwd()
        sub_dir = "intake_questionnaires"
        path = os.path.join(dir_name, sub_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        try:
            event, year = self.title.split(', ')
        except Exception as e:
            return e
        file_name = f"{event}_{year}_intake_data.txt"
        with open(os.path.join(dir_name, sub_dir, file_name), 'w') as intake:
            for q_type in self.__survey.keys():
                answer = \
                    self.fetch_response(q_type)
                next_line = f'{q_type} : {answer}\n'
                try:
                    intake.write(next_line)
                except Exception as e:
                    return e
            intake.close()

    def edit_response(self, question_type, new_response):
        try:
            self.__survey[question_type] = new_response
        except Exception as e:
            return f"Python Error!: {e}"

    def get_keys(self):
        '''
        get a list of all the keys of the CompleteSurvey.__survey attribute
        '''
        question_types = []
        for key in self.__survey.keys():
            question_types.append(key)
        return question_types

    def __getitem__(self, item):
        return self.__survey[item]

    def __repr__(self):
        return f"CompleteSurvey(<filled_out_dictionary>)"

    def __str__(self):
        if self.title:
            return self.title
        else:
            self.title = self.__generate_title()

class CompleteBudget():

    def __init__(self, budget):
        self.__budget = budget
        self.title = budget['title']

    def __getitem__(self, item):
        return self.__budget[item]

    def write_to_file(self):
        """
        Description: write intake data to file which will be read into main app
        :param survey: a dict of survey questions and corresponding
        user responses
        :return: error message if error
        """
        dir_name = os.getcwd()
        sub_dir = "budgets"
        path = os.path.join(dir_name, sub_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        try:
            event, year = self.title.split(', ')
        except Exception as e:
            return e
        file_name = f"{event}_{year}_budget_draft.txt"
        with open(os.path.join(dir_name, sub_dir, file_name), 'w') as budget:
            for calc_type in self.__budget.keys():
                val = \
                    self.__getitem__(calc_type)
                next_line = f'{calc_type} : {val}\n'
                try:
                    budget.write(next_line)
                except Exception as e:
                    return e
            budget.close()


def fetch_survey(*args):
    '''
    read an existing survey back into memory to edit a response
    '''
    dir_name = os.getcwd()
    sub_dir = "intake_questionnaires"
    path = os.path.join(dir_name, sub_dir)
    if os.path.exists(path):
        dir_list = os.listdir(path)
        intake_files = []
        for file in dir_list:
            if file.endswith('.txt'):
                intake_files.append(file)
        valid_file_name = False
        if args:  # for testing file name is passed in args, not input()
            file_name = args[0]
            valid_file_name = True

        while valid_file_name is False:
            print("Please choose an intake data file from the below "
                  "list by entering the full file name "
                  "(ex: this_file_intake_data.txt)")
            for i, file in enumerate(intake_files):
                print(f"     {i+1}. {file}")
            file_name = input("===> ")
            if file_name in intake_files:
                valid_file_name = True
            else:
                partition = '*'*80
                print(f"Error: {file_name} not in {intake_files}"
                        f"\n{partition}")
        os.chdir(path)  # change to subdirectory where file is
        with open(file_name, 'r') as intake_survey:
            edit_survey = {}
            list_of_dicts = intake_survey.readlines()
            for d in list_of_dicts:
                q_type, a = d.split(" : ")
                answer = a.strip("\n")
                edit_survey[q_type] = answer

        intake_survey.close()
        my_survey = CompleteSurvey(edit_survey)
        os.chdir(dir_name)  # change back to main proj directory
        return my_survey

def intake_questionnaire(*args):
    '''
    prompt for user input and clean user input for CompleteSurvey instance
    '''
    survey = {}  # container for survey questions and answers
    try:  # for testing, pre-filled survey is passed as a dict in args
        questionnaire_dict = args[0]
        for q_type in questionnaire_dict:
            answer = questionnaire_dict.get(q_type)
            # instantiate question for testing
            question = Question(questionnaire.get(q_type))
            # record the answer
            question.record_answer(answer)
            # write question to survey
            survey[q_type] = answer

    except IndexError:  # for actual use
        # Booleans for validating user input per question type
        title_query = False; crew_query = False; driver_query = False
        driver_ot_query = False; vehicle_query = False;
        toll_query = False; flight_query = False
        meals_lodging_query = False


        for q_type in questionnaire.keys():
            # instantiate Question from dict keys
            question = Question(questionnaire.get(q_type))
            quest_type = question.generate_question_type()
            print(quest_type)
            if quest_type == "title query":
                while title_query is False:
                    answer = input(f"{question.ask()}: ")
                    try:
                        event, year = answer.split(', ')

                        if int(year) >= TODAY.year:
                            # record the answer
                            question.record_answer(answer)
                            # write question to survey
                            survey[question.question_type] = question.fetch_response(
                                question)
                        else:
                            print(
                                f"Year must be equal to or greater than the current year: "
                                f"{TODAY.year}")
                            continue
                    except ValueError:
                        print("Error: Comma separate the input values: "
                              "(ex===> Midwest, 2021, ex===> JEN, 2022) "
                              "please try again.\n")
                        continue
                    else:
                        title_query = True
            elif quest_type == "crew query":
                # use question instance as prompt
                while crew_query is False:
                    answer = input(f"{question.ask()}: ")
                    if answer and answer.isnumeric():
                        print(int(answer) in range(2, 5))
                        if int(answer) in range(2, 5):  # between 2 and 4
                            # record the answer
                            question.record_answer(answer)
                            # write question to survey
                            survey[question.question_type] =\
                                question.fetch_response(question)
                            break
                        else:
                            continue
            elif quest_type == "driver query":
                while driver_query is False:
                    answer = input(f"{question.ask()}: ")
                    if answer and answer.isnumeric():
                        if int(answer) in range(3):  # needs to be 1 or 2
                            # record the answer
                            question.record_answer(answer)
                            # write question to survey
                            survey[question.question_type] =\
                                question.fetch_response(question)
                            driver_query = True

            elif quest_type == "vehicle query":
                while vehicle_query is False:
                    try:
                        answer = input(f"{question.ask()}: ")

                        if answer and int(answer) in range(4):
                            # record the answer
                            question.record_answer(answer)
                            # write question to survey
                            survey[question.question_type] = \
                                question.fetch_response(question)
                            vehicle_query = True;
                        else:
                            print('Error: please enter a value.')
                    except TypeError:
                        print(f'Error: "{answer}" is not the proper format, please '
                              "please a integer.")
                        continue

            elif quest_type == "driver ot query":
                while driver_ot_query is False:
                    try:
                        answer = input(f"{question.ask()}: ")
                        if answer and int(answer) >= 0:
                            # record the answer
                            question.record_answer(answer)
                            # write question to survey
                            survey[question.question_type] = \
                                question.fetch_response(question)
                            driver_ot_query = True;
                    except TypeError:
                        continue

            elif quest_type == "toll query":
                while toll_query is False:
                    try:
                        answer = input(f"{question.ask()}: ")
                        city, state = answer.split(', ')
                        if state.upper() not in STATE_SALES_TAX.keys():
                            print(f"{state} is an "
                                  f"Invalid State Code. Please try again...")
                        else:
                            # record the answer
                            question.record_answer(answer)
                            # write question to survey
                            survey[question.question_type] = \
                                question.fetch_response(question)
                            toll_query = True;
                    except ValueError:
                        print("Error: Comma separate the input values: "
                              "(ex===> Chicago, IL ex===> New York, NY) "
                              "please try again.")

            elif quest_type == "flight query":
                while flight_query is False:
                    try:
                        answer = input(f"{question.ask()}: ")
                        depart, dest, dep_date, ret_date = answer.split(', ')
                    except ValueError:
                        print("InputError: Comma separate the input values: " \
                                  "ex===> DCA, MDW, 2021-12-14, 2021-12-17\n" \
                                  "...please try again.")
                        continue


                    try:
                        year, month, day = dep_date.split('-')

                    except ValueError:
                        print(f"InputError: {dep_date} is not the proper " \
                             "format. Need===> YYYY-MM-DD\n...please try again.")
                        continue

                    if int(year) < TODAY.year:
                        print(
                            f"Year must be equal to or greater than the "
                            f'current year: "{TODAY.year}"')
                        continue

                    elif int(month) < 1 or int(month) > 12:
                        print(f"InputError: {month} is not a valid "
                            f"month. Please enter a number between "
                            f"1 and 12.")
                        continue
                    elif int(day) < 1 or int(day) > 31:
                        print(f"InputError: {day} is not in range "
                                f"of days in a typical month. Please "
                                f"enter a number between 1 and 31.")
                        continue
                    try:
                        year, month, day = ret_date.split('-')

                    except ValueError:
                        print(f"InputError: {ret_date} is not the proper " \
                              "format. Need===> YYYY-MM-DD\n...please try again.")
                        continue

                    if int(year) < TODAY.year:
                        print(
                            f"Year must be equal to or greater than the "
                            f'current year: "{TODAY.year}"')
                        continue

                    elif int(month) < 1 or int(month) > 12:
                        print(f"InputError: {month} is not a valid "
                            f"month. Please enter a number between "
                            f"1 and 12.")
                        continue

                    elif int(day) < 1 or int(day) > 31:
                        print(f"InputError: {day} is not in range "
                                f"of days in a typical month. Please "
                                f"enter a number between 1 and 31.")
                        continue

                    else:
                        # record the answer
                        question.record_answer(answer)
                        # write question to survey
                        survey[question.question_type] = \
                            question.fetch_response(question)
                        flight_query = True

            elif quest_type == "meals and lodging query":
                while meals_lodging_query is False:
                    try:
                        answer = input(f"{question.ask()}: ")
                        city, state, year, month = answer.split(', ')
                    except ValueError:
                        print("Error: Please comma separate values. "
                              "(ex===> New-York, NY, 2021, Dec")

                    if state.upper() not in STATE_SALES_TAX.keys():
                        print(f"{state} is an "
                              f"Invalid State Code. Please try again...")

                    elif int(year) < TODAY.year:
                        print(
                        f"Year must be equal to or greater than the current year: "
                        f"{TODAY.year}")

                    elif len(month) != 3 and month not in meals_lodging_month_format:
                        print(f'{month} is not in the ' 
                              f'proper format. Need "Mmm" '
                              f'(ex===> Dec)')
                    else:
                        # record the answer
                        question.record_answer(answer)
                        # write question to survey
                        survey[question.question_type] = \
                            question.fetch_response(question)
                        meals_lodging_query = True

            else:
                answer = input(f"{question.ask()}: ")
                # record the answer
                question.record_answer(answer)
                # write question to survey
                survey[question.question_type] =\
                    question.fetch_response(question)

    return survey

def review_survey(survey):
    """
     print newly collected survey to the console for review
     """
    if survey.title:
        print(f"\nScanning {survey.title} questionnaire...")
    else:
        print("Scanning questionnaire...")
    for q_type in survey.get_keys():
        if survey.fetch_response(q_type) is not None:
            print(f"{q_type}: {survey.fetch_response(q_type)}")
        else:
            if survey.title:
                print(f'no response recorded in {survey.title} for "{q_type}"')
            else:
                print(f'no response recorded in survey for "{q_type}"')


def budget_feeder(survey):
    '''
    1.takes information from intake survey
    2.translates into new python dictionary,
    3.instantiates a CompleteBudget instance out of that dictionary,
    4.writes new budgets to file
    5. overwrites existing versions of budget file.
    :param survey: CompleteSurvey
    :return: None
    '''
    non_covid_calc_totals = []
    covid_calc_totals = []
    budget = {}  # instantiate container for new budget
    budget['title'] = survey['title query']
    if survey['crew query']:
        crew_on_job = get_crew(survey['crew query'])

    if survey['driver query']:
        drivers_on_job = get_drivers(survey['driver query'])
        # list of Person objects
        trip_personnel = blues_roster + crew_on_job + drivers_on_job
    else:  # no drivers on trip
        trip_personnel = blues_roster + crew_on_job

    budget['total people'] = str(len(trip_personnel))
    # get number of shared rooms
    shared_rooms = get_total_rooms(trip_personnel)
    budget['non-covid rooms total'] = str(shared_rooms)

    if survey['toll query']:
        # Contacting the API's can take a few seconds, console msgs improve UI
        print("Fetching toll data...")
        tolls_obj = get_tolls(survey['toll query'])
        if tolls_obj is not None:
            toll_roads = json_extract(tolls_obj, "road")
            toll_prices = json_extract(tolls_obj, "tagCost")
            print(
                f"Toll roads: {set(toll_roads)}")  # eliminate duplicate values
            print(f"Itemized tolls: {toll_prices}")
            print(f"Total tolls: {sum(toll_prices):,.2f}")
            # For file
            budget['toll roads'] = set(toll_roads)  # eliminate duplicates
            budget['Itemized tolls'] = f'{toll_prices}'
            tolls_estimate = sum(toll_prices)*float(survey["vehicle query"])
            budget['sum tolls'] = \
                f'${tolls_estimate:,.2f}'

            non_covid_calc_totals.append(tolls_estimate)
            covid_calc_totals.append(tolls_estimate)

    if survey['flight query']:
        # For console
        departure, destination, departure_date, return_date = \
            survey['flight query'].split(', ')
        print("Fetching flight data...")
        try:
            going_flight, going_airline, returning_flight, returning_airline = \
                get_com_flight_price(
                    departure, destination,
                    departure_date, return_date)
        except TypeError:
            commercial_flight_total = None
            print(SEPARATOR)
            print("Make sure there are no spaces IN-FRONT of your flight "
                  "input.")
            print(SEPARATOR)
        else:
            print(
                f"\nThe estimated cost before tax for one adult ticket from "
                f"{departure} to {destination} on {departure_date} is: "
                f"\n${going_flight:.2f} on {going_airline}\n")

            going_flight_tax = flight_tax_calc(float(going_flight))  # get tax
            budget['individual departing flight rate'] = \
                f"${going_flight_tax:.2f} on {going_airline}"

            departing_flight_total = len(trip_personnel)*float(going_flight_tax)
            print(
                f"\nThe estimated cost before tax for one adult ticket from  "
                f"{destination} to {departure} on {return_date} is: "
                f"\n${returning_flight:.2f} on {returning_airline}")
            budget['individual returning flight rate'] = \
                f'${returning_flight:.2f} on ' \
                f'{returning_airline}'
            # get tax
            returning_flight_tax = flight_tax_calc(float(returning_flight))
            returning_flight_total = \
                len(trip_personnel) * float(returning_flight_tax)

            commercial_flight_total = \
                departing_flight_total + returning_flight_total
            budget['full band commercial airline estimate after tax'] = \
                f"${commercial_flight_total:,.2f}"

            non_covid_calc_totals.append(commercial_flight_total)
            covid_calc_totals.append(commercial_flight_total)

            print(SEPARATOR)
            print("Gov't rate flight...")
            print(f"${get_gov_flight(len(trip_personnel)):,.2f}")
            print(SEPARATOR)
            budget['full band govt rate flight total estimate'] = \
                f"${get_gov_flight(len(trip_personnel)):,.2f}"

    if survey['meals and lodging query']:
        # For console
        city, state, year, month = \
            survey['meals and lodging query'].split(', ')
        print("Fetching meal data...")
        try:
            meal_rate, lodging = get_meals_lodging(city, state, year, month)
            print(f"\nThe daily meal rate for {city}, {state}, "
                  f"in {month}, {year} is ${meal_rate}\n")
            print(f"The daily lodging rate for {city}, {state},"
                  f" in {month}, {year} is ${lodging:.2f}")
            print(SEPARATOR)
        except TypeError:
            print(SEPARATOR)
            print("Attention: The gsa.gov query came back other than 200 "
                "status code. Check your intake survey and edit format.")
            print(SEPARATOR)
        else:
            # For file
            full_band_meals = \
                float(meal_rate)*int(survey['days query'])*len(trip_personnel)

            budget['Full band meals & incidentals estimate'] = \
                f"${full_band_meals:,.2f} for {len(trip_personnel)} people for "\
                f"{survey['days query']} days"

            lodging_after_tax = sales_tax_calc(state, lodging)

            full_band_lodging = \
            float(lodging_after_tax)*int(survey["nights query"])*shared_rooms

            # no doubled rooms
            covid_lodging = \
            float(lodging_after_tax)*int(survey["nights query"])*len(trip_personnel)

            budget['Non-covid full band lodging estimate'] = \
            f'${full_band_lodging:,.2f} for {survey["nights query"]} nights '\
            f'for {shared_rooms} rooms at ${lodging:.2f} per night'

            budget['covid full band lodging individual rooms'] = \
            f'${covid_lodging:,.2f} for {survey["nights query"]} nights '\
            f'for {len(trip_personnel)} rooms at ${lodging:.2f} per person per night'

            non_covid_calc_totals.append(full_band_lodging)
            covid_calc_totals.append(covid_lodging)

    if survey['driver ot query']:
        driver_ot = \
        get_driver_ot(survey['driver query'], survey['driver ot query'])
        budget['driver ot estimate'] = f"${driver_ot:,.2f} for "\
                                            f"{survey['driver query']} drivers "\
                                            f"for {survey['driver ot query']} "\
                                            "estimated hours"

        non_covid_calc_totals.append(driver_ot)
        covid_calc_totals.append(driver_ot)

    for total in non_covid_calc_totals:  # iterate through all calculations
        if total is None:
            total = 0  # set None values to 0 for addition
    budget['NON-COVID ESTIMATED COST'] = \
            f"${sum(non_covid_calc_totals):,.2f}"
    for total in covid_calc_totals:
        if total is None:
                total = 0
    budget['COVID NO ROOM SHARING ESTIMATED COST'] = \
            f"${sum(covid_calc_totals):,.2f}"

    if commercial_flight_total in non_covid_calc_totals and covid_calc_totals:
        # switch out commercial flight rates in totals for gov flight rate
        non_covid_calc_totals.pop(1)
        non_covid_calc_totals.append(get_gov_flight(len(trip_personnel)))

        covid_calc_totals.pop(1)
        covid_calc_totals.append(get_gov_flight(len(trip_personnel)))

        # perform the aggregate sum again with gov flight rate
        for total in non_covid_calc_totals:  # iterate through all calculations
            if total is None:
                total = 0  # set None values to 0 for addition
        budget['NON-COVID ESTIMATED COST (GOV FLIGHT RATE)'] = \
            f"${sum(non_covid_calc_totals):,.2f}"
        for total in covid_calc_totals:
            if total is None:
                total = 0
        budget['COVID NO ROOM SHARING ESTIMATED COST (GOV FLIGHT RATE)'] = \
            f"${sum(covid_calc_totals):,.2f}"




    my_budget = CompleteBudget(budget)  # instantiate object
    # check if this is an update or new budget
    event, year = my_budget['title'].split(', ')
    file_name = f"{event}_{year}_budget_draft.txt"
    dir_name = os.getcwd()
    sub_dir = "budgets"
    path = os.path.join(dir_name, sub_dir)
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)  # pop into the budgets subdirectory
    if os.path.exists(file_name):
        print(f"Updating {event}_{year}_budget_draft.txt in "
                "your budgets subdirectory....")
    else:
        print('Writing a new file to a "budgets" subdirectory. '
                f"Please note this file is named: "
                f'{event}_{year}_budget_draft.txt.')
    os.chdir(dir_name)  # pop back into the project directory
    err = my_budget.write_to_file()  # write information to file
    if err:  # there was a problem writing the budget to a file
        print(err)


if __name__ == '__main__':
    # sample user input for quick CompleteSurvey instantiation and testing
    survey = {'title query': 'Midwest, 2021',
              'duration query': '3',
              'nights query': '2',
              'days query': '3',
              'crew query': '4',
             'driver query': '1',
              'vehicle query': '1',
              'driver ot query': '15',
              'toll query': 'Winchester, VA',
              'flight query': 'DCA, MDW, 2021-12-14, 2021-12-17',
              'meals and lodging query': 'New-York, NY, 2021, Dec'}

    # survey = intake_questionnaire()  # test the questionnaire
    # make a CompleteSurvey instance out of the survey you just collected
    my_survey = CompleteSurvey(survey)
    assert isinstance(my_survey, CompleteSurvey)
    # print survey instances title
    print(f"Survey for: {my_survey}")
    # print the response to a particular question
    print(my_survey["driver ot query"])
    review_survey(my_survey)  # check to see what populated in the survey
    err = my_survey.write_to_file()
    if err:
        print(err)
    print()
    print("*" * 80)
    print("Choose a survey to edit...")
    # choose existing survey from intake_questionnaires subdirectory to edit
    survey1 = fetch_survey()
    assert isinstance(survey1, CompleteSurvey)
    print(f"Printing type of fetched survey: {type(survey1)}")
    print("*" * 80)
    # get all the keys in CompleteSurvey.__survey dict
    question_types = survey1.get_keys()
    print(question_types)
    assert type(question_types) == list
    print(f"\n{survey1['title query']} recorded:\n")
    for q_type in question_types:
        print(f"{survey1[q_type]} for {q_type}")
    # change driver query value
    print("*" * 80)
    print(f'Driver query was: {survey1["driver query"]}')
    survey1.drivers = survey1.edit_response('driver query', '2')
    err = survey1.write_to_file()  # write edited response to file
    if err:
        print(err)
    print(f'Driver query is now: {survey1["driver query"]}')
    print("*" * 80)
    print("\nTesting above changes are reflected...")
    for q_type in question_types:
        print(f"{survey1[q_type]} for {q_type}")