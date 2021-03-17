import datetime
from freezegun import freeze_time
import unittest
from saves_responder import SavesResponder
from user_timeout import UserTimeout

class SavesResponderTests(unittest.TestCase):

    """ Ensure that the responder loads the default response from the file. """
    def test_response_list_not_empty_after_loading(self):
        under_test = SavesResponder()
        if not under_test.RESPONSE_MESSAGE:
            self.fail('Default response message was empty')
        
    """ Ensure that the responder loads the default keywords from the file. """
    def test_keyword_list_lowercase_on_load(self):
        under_test = SavesResponder()
        for keyword in under_test.KEYWORDS:
            if any(l.isupper() for l in keyword): 
                self.fail(f'letter in {keyword} uppercase')

class UserTimeoutTests(unittest.TestCase):

    """ Ensure that timeout period state changes after adding user. """
    def test_timeout_state_changes_after_addition(self):
        under_test = UserTimeout()
        status = under_test.check_if_user_in_timeout('test-user')
        self.assertFalse(status, 'User should not have started in timeout')

        status = under_test.check_if_user_in_timeout('test-user')
        self.assertTrue(status, 'User should have been in timeout after checking')
    
    """ Ensure that timeout state expires after timeout period. """
    def test_timeout_state_changes_after_addition(self):
        under_test = UserTimeout()
        status = under_test.check_if_user_in_timeout('test-user')
        self.assertFalse(status, 'User should not have started in timeout')
        status = under_test.check_if_user_in_timeout('test-user')
        self.assertTrue(status, 'User should have been in timeout after checking')

        future_time = datetime.datetime.now() + under_test.TIMEOUT_LENGTH + datetime.timedelta(minutes=1)

        with freeze_time(future_time):
            status = under_test.check_if_user_in_timeout('test-user')
            self.assertFalse(status, 'User should have left timeout status after timeout period')

if __name__ == '__main__':
    unittest.main()