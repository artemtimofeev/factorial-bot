import config
from modules.utils.message import Message
from modules.handlers import Handler
from modules.message_queue import MessageQueue
from modules.bot import Bot


def start():
    bot = Bot(token=config.API_KEY)

    message_queue = MessageQueue()

    while True:
        new_message = bot.get_new_message()
        if new_message is not None and new_message.user_id in [182040882, 348350925, 406197915, 579989535]:
            response = Handler().answer(new_message)
            message_queue.push(response)

            messages_to_send = message_queue.pop()
            for message in messages_to_send:
                bot.send_message(message)


if __name__ == "__main__":
    start()
