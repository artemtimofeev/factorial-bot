import random
from datetime import datetime


class Message(object):
    def __init__(self, user_id=None, send_time=-1):
        self.user_id = user_id
        self.text = ""
        self.attachments = ""

        random.seed()

        self.random_id = random.randint(1, 2 ** 64)
        self.keyboard = None

        self.send_time = datetime.timestamp(datetime.now()) + send_time

    def set_send_time(self, send_time):
        self.send_time = send_time

    def set_text(self, text):
        self.text = text

    def add_text(self, text):
        self.text += '\n\n' + text

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_attachments(self, attachments: list):
        for att in attachments:
            self.attachments += att + ","

    def set_keyboard(self, keyboard):
        self.keyboard = keyboard

    def get_json(self):
        if self.keyboard is not None:
            parameters = {'user_id': self.user_id,
                          'random_id': self.random_id,
                          'message': self.text,
                          'attachment': self.attachments,
                          'keyboard': self.keyboard.get_keyboard()}
        else:
            parameters = {'user_id': self.user_id,
                          'random_id': self.random_id,
                          'message': self.text,
                          'attachment': self.attachments}
        return parameters

    def __lt__(self, other):
        return self.send_time < other.send_time

    def __eq__(self, other):
        return self.send_time == other.send_time
