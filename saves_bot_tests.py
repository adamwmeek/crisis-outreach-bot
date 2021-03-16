import unittest
from saves_responder import SavesResponder

class SavesResponderTests(unittest.TestCase):

    """ Ensure that the responder loads the response from the file """
    def test_response_list_not_empty_after_loading(self):
        under_test = SavesResponder()
        if not under_test.RESPONSE_MESSAGE:
            self.fail('Default response message was empty')
        
    def test_keyword_list_lowercase_on_load(self):
        under_test = SavesResponder()
        for keyword in under_test.KEYWORDS:
            if any(l.isupper() for l in keyword): 
                self.fail(f'letter in {keyword} uppercase')

if __name__ == '__main__':
    unittest.main()