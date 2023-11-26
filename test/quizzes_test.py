import unittest
from app.controllers.quizzes_controller import QuizzesController
from datetime import datetime

class QuizzesTest(unittest.TestCase):

    def setUp(self):
        # Run tests on non-production data
        self.ctrl = QuizzesController('assignments_test.json')

    def test_expose_failure_01(self):
        """
        This test case aims to expose a crash when adding a quiz with title passed as integer variable.
        This fails as this will give unsupported operand type(s) for +: 'int' and 'str'
        Expected crash: quizzes_controller.py, line 63
        """

        self.ctrl.clear_data()
        # Passing valid integer as quiz title
        quiz_id = self.ctrl.add_quiz(12345,"text", datetime.now(), datetime.now())
        # Check that we have one quiz in the list
        quizzes = self.ctrl.get_quizzes()
        # Ideally, one quiz should be added and should be checked below
        self.assertEquals(len(quizzes), 1, "There is no quiz.")
        

    def test_expose_failure_02(self):
        """
        This test case aims to expose a crash when attempting to add a question with datetime type passed as title.
        This occurs as the save data is not able to serialize the title (datetime object) into a valid json.
        Expected crash: quizzes_controller.py, line 81 which effectively calls save data in line 55
        """
        self.ctrl.clear_data()
        quiz_id = self.ctrl.add_quiz("Quiz title", "text", datetime.now(), datetime.now())
        # Check that one quiz has been added in the list
        quizzes = self.ctrl.get_quizzes()
        self.assertEquals(len(quizzes), 1, "There is exactly one quiz.")
        # Add a question using the same quiz id but we pass datetime object as title in place of string
        question_id = self.ctrl.add_question(quiz_id, datetime.now(), "Sample question")
        # Answer and check if the valid question is added.
        self.assertIsNotNone(question_id, "A valid question_id is fetched.")


    def test_expose_failure_03(self):
        """
        This test case aims to expose a crash when attempting to add text containing Unicode escape sequence '\udc00'.
        This occurs as generate_id fails when encoding as utf-8 and is part of utf-16
        Expected crash: quizzes_controller.py, line 91
        """
        self.ctrl.clear_data()
        quiz_id = self.ctrl.add_quiz("Quiz title","text", datetime.now(), datetime.now())
        # Add a question using quiz id
        question_id = self.ctrl.add_question(quiz_id, title="Question 1",text="Sample question")
        question = self.ctrl.get_question_by_id(question_id)
        # Assert and check if the same question id can be fetched which has been added.
        self.assertEquals(question_id, question.id, "Correct question is fetched.")
        # Test case fails when the value of parameter text contains value conains unicode escape sequence '\udc00'.
        answer_id = self.ctrl.add_answer(question_id, text='Value is \udc00', is_correct=None)
        # Assert if valid answer id answer can be fetched. 
        self.assertIsNotNone(answer_id, "A valid answer_id has returned.")

if __name__ == '__main__':
    unittest.main()