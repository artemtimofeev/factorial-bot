from modules.message import Message
from modules.bot import Bot


def start():
    bot = Bot(token="ceb2beb453eeb9d564a9249b70a3dd3e60bedaae6528f7ca4414444adee3d5ff9665eed50562aa306cb34")
    while True:
        new_message = bot.get_new_message()
        if new_message is not None:
            user_id, text = new_message.user_id, new_message.text
            response = Message(user_id=new_message.user_id)
            response.set_text("дарова димас")
            bot.send_message(response)


if __name__ == "__main__":
    start()
