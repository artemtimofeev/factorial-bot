from modules.utils.message import Message
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import Event


class Handler:
    def __init__(self, user_id, state=None):
        self.user_id = user_id
        self.state = state

    def default_answer(self) -> Message:
        response = Message(user_id=self.user_id)
        response.set_text("Привет! "
                          "Если у тебя есть какой-то вопрос, нажми на нужную кнопку🙂")

        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('Узнать решение задачи', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Другой вопрос', color=VkKeyboardColor.SECONDARY)

        response.set_keyboard(keyboard)

        self.state = "start"

        return response

    def answer(self, message: Event) -> Message:
        response = Message(user_id=self.user_id)

        if self.state is None:
            response = self.default_answer()

        elif self.state == "start":
            if message.text == "Другой вопрос":
                response.set_text("Напишите свой вопрос здесь, и на него ответит менеджер чата😊 \n\n"
                                  "Чтобы вернуть бота, нажмите кнопку ниже или напишите \"Начать\".")

                keyboard = VkKeyboard(one_time=False)
                keyboard.add_button('Начать', color=VkKeyboardColor.PRIMARY)
                response.set_keyboard(keyboard)

                self.state = "manager"
            elif message.text == "Узнать решение задачи":
                response.set_text("РЕШЕНИЕ: "
                                  "\n\n"
                                  "*текст*")
                keyboard = VkKeyboard(one_time=False)
                keyboard.add_button('Начать', color=VkKeyboardColor.PRIMARY)
                response.set_keyboard(keyboard)
            else:
                response = self.default_answer()

        elif message.text == "Начать":
            response = self.default_answer()

        return response
