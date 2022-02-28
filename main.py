import config
import threading
from modules.handlers import Handler
from modules.message_queue import MessageQueue
from modules.bot import Bot


stop = "no"


def check_messages(bot, message_queue, users):
    while not stop == "yes":
        new_message = bot.get_new_message()
        if new_message is not None:  # and new_message.user_id in [182040882, 348350925, 406197915, 579989535]:
            if new_message.user_id not in users:
                users[new_message.user_id] = Handler(user_id=new_message.user_id)
            response = users[new_message.user_id].answer(new_message)
            message_queue.push(response)


def send_messages(bot, message_queue):
    while not stop == "yes":
        messages_to_send = message_queue.pop()
        for message in messages_to_send:
            bot.send_message(message)


if __name__ == "__main__":
    bot = Bot(token=config.API_KEY)
    message_queue = MessageQueue()
    users = {}

    checking_thread = threading.Thread(target=check_messages, args=(bot, message_queue, users))
    answering_thread = threading.Thread(target=send_messages, args=(bot, message_queue))

    checking_thread.start()
    answering_thread.start()

    stop = input("Остановить?")

    if stop == "yes":
        checking_thread.join()
        answering_thread.join()
