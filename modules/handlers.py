from modules.utils.message import Message
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import Event

PROBLEM_1_SOLUTION = """
Помещая одну за одной скрепки в сосуды, мы будем наблюдать появление водяного бугорка. Вода стремится принять сферическую форму благодаря силе поверхностного натяжения. Именно эта сила не даёт жидкости вытечь даже при том условии, что её объём больше объёма сосуда. Сила поверхностного натяжения пропорциональна длине контура, ограничивающего поверхность жидкости: чем больше контур, тем больше сила, поэтому чем шире сосуд, тем больший объем имеет выпуклость. Таким образом, можем сделать вывод, что в пиалу поместится больше скрепок, чем в стакан, до того, как начнёт выливаться вода.

Оценим количество скрепок в сосудах: Будем считать, что максимально возможная высота бугорка 1 мм, и что он имеет цилиндрическую форму. По формуле для цилиндра (V = πD²h/4) объём выпуклости составляет для пиалы около 7850 кубических мм, а для стакана - 1960 кубических мм. Тогда легко вычислить, что в пиалу поместится 7850/35⋍224 скрепки, а в стакан - 56, то есть в четыре раза меньше.
"""


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

    def answer(self, message: Event):
        response = [Message(user_id=self.user_id), ]

        if self.state is None:
            response[0] = self.default_answer()

        elif self.state == "start":
            if message.text == "Другой вопрос":
                response[0].set_text("Напишите свой вопрос здесь, и на него ответит менеджер чата😊 \n\n"
                                  "Чтобы вернуть бота, нажмите кнопку ниже или напишите \"Начать\".")

                keyboard = VkKeyboard(one_time=False)
                keyboard.add_button('Начать', color=VkKeyboardColor.PRIMARY)
                response[0].set_keyboard(keyboard)

                self.state = "manager"
            elif message.text == "Узнать решение задачи":
                response[0].set_text(f"РЕШЕНИЕ: "
                                  "\n\n"
                                  f"{PROBLEM_1_SOLUTION}")
                keyboard = VkKeyboard(one_time=False)
                keyboard.add_button('Начать', color=VkKeyboardColor.PRIMARY)
                response[0].set_keyboard(keyboard)
                response.append(Message(user_id=self.user_id, send_time=15))
                response[1].set_text("Понравилась задачка?")
                keyboard = VkKeyboard(inline=True)
                keyboard.add_button('👍', color=VkKeyboardColor.POSITIVE)
                keyboard.add_button('👎', color=VkKeyboardColor.NEGATIVE)
                response[1].set_keyboard(keyboard)

                self.state = "evaluate"
            else:
                response[0] = self.default_answer()
        elif self.state == "evaluate":
            if message.text == '👍':
                response[0].set_text("Можешь скинуть её друзьям, пусть проверят себя!")
            elif message.text == '👎':
                response[0].set_text("(")
            else:
                response[0] = self.default_answer()
            self.state = "start"
        elif message.text == "Начать":
            response[0] = self.default_answer()

        return tuple(response)
