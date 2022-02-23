from modules.utils.message import Message
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import Event


class Handler:
    def __init__(self):
        pass

    def answer(self, message: Event) -> Message:
        response = Message(user_id=message.user_id)
        response.set_text("дарова")

        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('Посетить врача', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Употребить галоперидол', color=VkKeyboardColor.SECONDARY)

        response.set_keyboard(keyboard)

        return response
