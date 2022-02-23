import requests
from modules.message import Message
from vk_api import VkApi
from vk_api import exceptions as api_exceptions
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from modules.utils.queue import Queue


class Bot:
    def __init__(self, token):
        self.vk = VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk, wait=1)
        self.events = Queue()

    def get_new_message(self) -> Event:
        try:
            self.events.add(self.longpoll.check())
        except requests.exceptions.ReadTimeout:
            print("Request time out. Trying reconnect in 5 seconds")
        except requests.exceptions.ConnectionError:
            print("Another problems with connection.")

        for event in self.events:
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                return event

    def send_message(self, message: Message):
        try:
            self.vk.method('messages.send', message.get_json())
        except api_exceptions.ApiError as err:
            print(err)
