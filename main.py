import config
from modules.message import Message
from modules.bot import Bot


def start():
    bot = Bot(token=config.API_KEY)
    while True:
        new_message = bot.get_new_message()
        if new_message is not None:
            user_id, text = new_message.user_id, new_message.text
            response = Message(user_id=new_message.user_id)
            response.set_text("дарова димас")
            bot.send_message(response)


if __name__ == "__main__":
    start()
