"""

Postconditions:

"""

from budget_constructor import *

valid_action = False
ACTIONS = ["make new budget", "edit existing budget"]
YES_OR_NO = ['y','n']
SEPARATOR = "*" * 80
while not valid_action:
    print("Please choose one of below actions by typing it to the console..."
          "(ex: edit existing budget)")
    for i, action in enumerate(ACTIONS):
        print(f"     {i+1}. {action}")
    action = input("===> ")
    if action in ACTIONS:
        valid_action = True
    else:
        print(f"{action} is not in {ACTIONS}. Please try again.")

if action == ACTIONS[0]:  # create a new budget
    good_survey = False
    while good_survey is False:
        print(SEPARATOR)
        survey = intake_questionnaire()
        new_survey = CompleteSurvey(survey)
        err = new_survey.write_to_file()  # in subdirectory intake_questionnaires
        if err:  # there was a problem writing survey to file
            print(err)
        print(SEPARATOR)
        print("Here is the survey as you've just filled it out...")
        print(SEPARATOR)
        review_survey(new_survey)
        print(SEPARATOR)
        valid_y_n = False
        while not valid_y_n:
            cont = input('Type "y" if you wish to continue. Type "n" if you\'d '
                     'like to redo your survey===> ')
            if cont not in YES_OR_NO:
                print(f'{cont} is invalid input: Type "y" if you wish to '
                f'continue. Type "n" if you\'d like to redo your survey===> ')
            elif cont == YES_OR_NO[1]:  # need to edit new_survey
                question_types = new_survey.get_keys()
                for q_type in question_types:
                    if new_survey[q_type]:
                        print(f"{q_type} : {new_survey[q_type]} ")
                    else:  # NoneType in the val
                        print(f"{q_type}: None")
                editing = True; valid_type = False;
                print(SEPARATOR)
                while editing is True:
                    while not valid_type:
                        print(
                                "Please choose which value above you'd like to "
                                "edit by typing the corresponding key.\nYou "
                                f"may choose from...")
                        for i, q_type in enumerate(question_types):
                            print(f"     {i + 1}. {q_type}")
                        question_type = input("===> ")
                        if question_type in question_types:
                            valid_type = True

                        new_response = input(
                        f"Please enter your new response for {question_type}: ")
                        new_survey.edit_response(question_type, new_response)
                        print("writing updated response to file...")
                        new_survey.write_to_file()
                        cont = input(
                        'Would you like to continue editing, "y" or "n"===> ')
                        if cont in YES_OR_NO:
                            valid_y_n = True
                        if cont == YES_OR_NO[1]:  # stop editing, good survey
                            editing = False; good_survey = True
            else:
                valid_y_n = True; good_survey = True
        print(SEPARATOR)
        budget_feeder(new_survey)

if action == ACTIONS[1]:  # edit existing survey
    existing_survey = fetch_survey()
    question_types = existing_survey.get_keys()
    print(f"\n{existing_survey['title query']} recorded:\n")
    for q_type in question_types:
        if existing_survey[q_type]:
            print(f"{q_type} : {existing_survey[q_type]} ")
        else:  # NoneType in the val
            print(f"{q_type}: None")
    editing = True; valid_type = False; valid_y_n = False
    print(SEPARATOR)
    while editing:
        while not valid_type:
            print(
                "Please choose which value above you'd like to "
                "edit by typing the corresponding key.\nYou "
                f"may choose from...")
            for i, q_type in enumerate(question_types):
                print(f"     {i+1}. {q_type}")
            question_type = input("===> ")
            if question_type in question_types:
                valid_type = True

        new_response = input(f"Please enter your new response for {question_type}: ")
        existing_survey.edit_response(question_type, new_response)
        print("writing updated response to file...")
        existing_survey.write_to_file()
        cont = input('Would you like to continue editing, "y" or "n"===> ')
        if cont in YES_OR_NO:
            valid_y_n = True; valid_type = False
        if cont == YES_OR_NO[1]:  # stop editing
            editing = False
    print(SEPARATOR)
    print("Updating budget data...")
    budget_feeder(existing_survey)
