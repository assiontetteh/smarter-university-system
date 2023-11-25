import unittest
from app.controllers.quizzes_controller import QuizzesController
from datetime import datetime

class QuizzesTest(unittest.TestCase):

    def setUp(self):
        # Run tests on non-production data
        self.ctrl = QuizzesController('quizzes_test.json')

    def test_expose_failure_01(self):
        """
        This test case aims to expose a crash when adding a quiz with missing parameters.
        Expected crash: quizzes_controller.py, line 64
        """

        self.ctrl.clear_data()
        # Not passing the available_date param
        # This will give missing positional argument: 'available_date'
        quiz_id = self.ctrl.add_quiz(title="Quiz title",text="text", due_date=datetime.now())
        # Check that we have one quiz in the list
        quizzes = self.ctrl.get_quizzes()
        # Since there is no quiz, the assertEquals function below fails
        self.assertEquals(len(quizzes), 1, "There is no quiz.")
        

    def test_expose_failure_02(self):
        """
        This test case aims to expose a crash when attempting to add a question to a non-existent id.
        Expected crash: quizzes_controller.py, line 76
        """
        self.ctrl.clear_data()
        quiz_id = self.ctrl.add_quiz(title="Quiz title",text="text", available_date=datetime.now(), due_date=datetime.now())
        # Check that we have one quiz in the list
        quizzes = self.ctrl.get_quizzes()
        self.assertEquals(len(quizzes), 1, "There is exactly one quiz.")
        # Get that quiz by using the quiz_id
        quiz = self.ctrl.get_quiz_by_id(quiz_id)
        # Add a question usng an invalid quiz id
        question_id = self.ctrl.add_question(quiz_id="2333", title="Question 1",text="Sample question")
        self.assertIsNotNone(question_id,"This question cannot be added")


    def test_expose_failure_03(self):
        """
        This test case aims to expose a crash when attempting to add an answer with incorrect parameter type.
        Expected crash: quizzes_controller.py, line 92
        """
        self.ctrl.clear_data()
        quiz_id = self.ctrl.add_quiz(title="Quiz title",text="text", available_date=datetime.now(), due_date=datetime.now())
        # Check that we have one quiz in the list
        quizzes = self.ctrl.get_quizzes()
        self.assertEquals(len(quizzes), 1, "There is exactly one quiz.")
        # Get that quiz by using the quiz_id
        quiz = self.ctrl.get_quiz_by_id(quiz_id)
        # Add a question using quiz id
        question_id = self.ctrl.add_question(quiz_id, title="Question 1",text="Sample question")
        # Test case fails when the value of parameter is_correct is passed as None instead of boolean.
        answer_id=self.ctrl.add_answer(question_id, text="Sample answer", is_correct=None)
        self.assertEquals(len(answer_id), 1, "There is answer for this question cannot be added.")

if __name__ == '__main__':
    unittest.main()
