import unittest
from database import *
from card import *
from controller import * 

class TestCardMethods(unittest.TestCase):

    def test_extract_one_card(self):
        self.assertEqual(Controller.extractOneCardFromCardList([Card(answer="aTest", category="cTest", question="qTest"), Card(answer="aTest2", category="cTest2", question="qTest2")]).category,"cTest2" )

    def test_make_request_body(self):
        self.assertEqual(Card(answer="aTest", category="cTest", question="qTest").makeRequestBody(), {"question" : "qTest", "answer" : "qTest", "category" : "cTest"})

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()