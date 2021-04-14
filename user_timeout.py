import datetime

class UserTimeout:
    def __init__(self):
        self.TIMEOUT_LENGTH = datetime.timedelta(minutes=30)
        self.user_table = {}

    """ Checks if a user is in the dictionary and if they are still in the timeout period. """
    def check_if_user_in_timeout(self, username):
        if username in self.user_table:
            if datetime.datetime.now() - self.user_table[username] > self.TIMEOUT_LENGTH:
                self.user_table[username] = datetime.datetime.now()
                return False
            else:
                return True

    def add_user_to_timeout(self, username):
        self.user_table[username] = datetime.datetime.now()
        return False
