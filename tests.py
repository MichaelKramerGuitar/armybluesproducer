import unittest
import os
from budget_constructor import Question, CompleteSurvey, \
    questionnaire, fetch_survey, budget_feeder, intake_questionnaire

class TestQuestion(unittest.TestCase):

    def setUp(self) -> None:
        self.question = Question(questionnaire.get('title query'))
        self.response = "Midwest, 2021"
        self.question_type = self.question.generate_question_type()


    def test_question_instantiation(self):
        assert isinstance(self.question, Question), f"question instantiation fails."

    def test_generate_question_type(self):
        for q_type in questionnaire.keys():
            if self.question == questionnaire.get(q_type):
                self.assertEqual(self.question_type, q_type,
                                 'expect "title query"')
    def test_ask(self):
        self.assertEqual(self.question.ask(), questionnaire.get(self.question_type))

class TestCompleteSurvey(unittest.TestCase):

    def setUp(self) -> None:
        self.feeder = {'title query': 'Test, 2021',
              'duration query': '3',
              'nights query': '2',
              'days query': '3',
              'crew query': '4',
              'driver query': '1',
              'vehicle query': '2',
              'driver ot query': '15',
              'toll query': 'Winchester, VA',
              'flight query': 'DCA, MDW, 2021-12-14, 2021-12-17',
              'meals and lodging query': 'New-York, NY, 2021, Dec'}

        self.survey = CompleteSurvey(self.feeder)

    def test_survey_instantiation(self):
        assert isinstance(self.survey, CompleteSurvey), 'perhaps the '\
                                                        'attributes do not '\
                                                        'match the feeder keys.'

    def test_question_types_returns_list(self):
        question_types = self.survey.get_keys()
        assert type(question_types) == list, 'ensure we\'re returned a list'

    def test_write_to_file(self):
        dir_name = os.getcwd()
        sub_dir = "intake_questionnaires"
        path = os.path.join(dir_name, sub_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        try:
            event, year = self.survey.title.split(', ')
        except Exception as e:
            return e
        file_name = f"{event}_{year}_intake_data.txt"
        with open(os.path.join(dir_name, sub_dir, file_name), 'w') as intake:
            for q_type in self.survey.get_keys():
                answer = \
                    self.survey.fetch_response(q_type)
                next_line = f'{q_type} : {answer}\n'
                try:
                    intake.write(next_line)
                except Exception as e:
                    return e
            intake.close()
        path_to_file = os.path.join(dir_name, sub_dir, file_name)
        assert os.path.isfile(path_to_file)

    def test_edit_response(self):
        question_type = 'crew query'
        new_response = '3'
        self.assertNotEqual(new_response, self.survey[question_type],
                            "new_response is the same as what we're trying to "
                            "update.")
        self.survey.edit_response(question_type, new_response)
        self.assertEqual(new_response, self.survey[question_type],
                         "the survey was not properly updated")

class TestBudgetFeederCompleteBudget(unittest.TestCase):
    '''
    ***please note***
    budget_feeder() has all of the API calls.
    These are in functions.py:
        1. get_meals_lodging (line 84)
        2. get_com_flight_price (line 114)
        3. get_tolls (line 248)
    Additionally, budget_feeder calls the following functions defined in
    functions.py:
        4. sales_tax_calc (line 54)
        5. get_gov_flight (line 175)
        6. get_crew (line 190)
        7. get_drivers (line 221)
        8. get_driver_ot (line 234)
        9. get_total_rooms (line 290)
        10. json_extract (line 344) which is a code snippet by Todd Birchard
        of the 'Hackers and Slackers' blog.
    Further, the .write_to_file() CompleteBudget method defined in
    budget_constructor.py

    '''
    def setUp(self) -> None:
        self.feeder = {'title query': 'Test, 2021',
              'duration query': '3',
              'nights query': '2',
              'days query': '3',
              'crew query': '4',
              'driver query': '1',
              'vehicle query': '2',
              'driver ot query': '15',
              'toll query': 'Winchester, VA',
              'flight query': 'DCA, MDW, 2021-12-14, 2021-12-17',
              'meals and lodging query': 'New-York, NY, 2021, Dec'}

        self.survey = CompleteSurvey(self.feeder)
        self.budget = budget_feeder(self.survey)

    def test_write_to_file(self):

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
        with open(os.path.join(dir_name, sub_dir, file_name),
                  'w') as budget:
            for calc_type in self.budget.keys():
                val = \
                    self.__getitem__(calc_type)
                next_line = f'{calc_type} : {val}\n'
                try:
                    budget.write(next_line)
                except Exception as e:
                    return e
            budget.close()
        path_to_file = os.path.join(dir_name, sub_dir, file_name)
        assert os.path.isfile(path_to_file)


class TestFetchSurvey(unittest.TestCase):

    def setUp(self) -> None:
        self.file_name = 'Test_2021_intake_data.txt'

    def test_fetch_survey(self):
        survey = fetch_survey(self.file_name)
        assert isinstance(survey, CompleteSurvey), 'fetch_survey did not work'

class TestIntakeQuestionnaire(unittest.TestCase):

    def setUp(self) -> None:
        self.survey = {'title query': 'TestIntake, 2021',
              'duration query': '3',
              'nights query': '2',
              'days query': '3',
              'crew query': '4',
              'driver query': '1',
              'vehicle query': '2',
              'driver ot query': '15',
              'toll query': 'Boston, MA',
              'flight query': 'DCA, BOS, 2021-12-14, 2021-12-17',
              'meals and lodging query': 'Boston, MA, 2021, Nov'}

    def test_intake_questionnaire(self):
        survey = intake_questionnaire(self.survey)
        self.assertEqual(self.survey, survey, "intake questionnaire is broken")


if __name__ == '__main__':
    unittest.main()