import unittest
import os
from budget_constructor import Question, CompleteSurvey, \
    questionnaire, fetch_survey, budget_feeder

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
        print(file_name)
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
        '''
        budget_feeder docstring:
            1.takes information from intake survey
            2.translates into new python dictionary,
            3.instantiates a CompleteBudget instance out of that dictionary,
            4.writes new budgets to file
            5. overwrites existing versions of budget file.
            :param survey: CompleteSurvey
            :return: None
        '''
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

###UNCOMMENT BELOW IF WILLING TO TEST USER INPUT FUNCTIONS###

# class TestFetchSurvey(unittest.TestCase):
#
#     def test_fetch_survey(self):
#         survey = fetch_survey()
#         assert isinstance(survey, CompleteSurvey), 'fetch_survey did not work'


if __name__ == '__main__':
    unittest.main()