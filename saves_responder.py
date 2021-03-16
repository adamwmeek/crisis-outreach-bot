import os
from dotenv import load_dotenv
import logging as saves_logger

class SavesResponder:

    def _reload_response(self):
        with open(self.RESPONSE_FILENAME, 'r') as handle:
            self.RESPONSE_MESSAGE = ''
            contents = handle.readlines()

            self.RESPONSE_MESSAGE = ''.join(map(str, contents))
            saves_logger.debug(f'Loaded response: {self.RESPONSE_MESSAGE}')
            return self.RESPONSE_MESSAGE

    def _reload_keywords(self):
        self.KEYWORDS.clear()
        with open(self.KEYWORDS_FILENAME, 'r') as handle:
            contents = handle.readlines()

            for line in contents:
                line = line.strip('\r')
                line = line.strip('\n')
                self.KEYWORDS.append(line.lower())
                saves_logger.debug(f'Added keyword: {line}')

    def _add_keyword(self, keyword):
        self.KEYWORDS.append(keyword.lower())

        with open(self.KEYWORDS_FILENAME, 'w') as handle:
                handle.writelines(self.KEYWORDS)

    def _remove_keyword(self, keyword):
        self.KEYWORDS.remove(keyword.lower())

        with open(self.KEYWORDS_FILENAME, 'w') as handle:
                handle.writelines(self.KEYWORDS)

    def __init__(self):
        self.KEYWORDS_FILENAME = 'keywords.txt'
        self.RESPONSE_FILENAME = 'response.txt'
        self.VOLUNTEER_MESSAGE = 'I picked up on a keyword in conversation: '

        load_dotenv()
        self.TOKEN = os.getenv('BOT_TOKEN')
        self.VOLUNTEER_CHANNEL_ID = int(os.getenv('VOLUNTEER_CHANNEL_ID'))
        self.KEYWORDS = []
        self.RESPONSE_MESSAGE = ''
        self._reload_keywords()
        self._reload_response()