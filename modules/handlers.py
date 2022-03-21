from modules.utils.message import Message
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import Event

PROBLEM_1_SOLUTION = """
Напишите своё решение здесь, мы проверим его в течение суток. Авторы первых трёх решений, которые окажутся грамотными и изобретательными, получат стикерпак! Так что поспешите)"""


class Handler:
    def __init__(self, user_id, state=None):
        self.user_id = user_id
        self.state = state

    def default_answer(self) -> Message:
        response = Message(user_id=self.user_id)
        response.set_text("Привет! "
                          "Если у тебя есть какой-то вопрос, нажми на нужную кнопку🙂")

        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('Отправить решение задачи', color=VkKeyboardColor.POSITIVE)
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
            elif message.text == "Отправить решение задачи":
                response[0].set_text(f"{PROBLEM_1_SOLUTION}")
                keyboard = VkKeyboard(one_time=False)
                keyboard.add_button('Начать', color=VkKeyboardColor.PRIMARY)
                response[0].set_keyboard(keyboard)
                #response.append(Message(user_id=self.user_id, send_time=15))
                #response[1].set_text("Понравилась задачка?")
                #keyboard = VkKeyboard(inline=True)
                #keyboard.add_button('👍', color=VkKeyboardColor.POSITIVE)
                #keyboard.add_button('👎', color=VkKeyboardColor.NEGATIVE)
                #response[1].set_keyboard(keyboard)
                #response[0].set_attachments(['photo-163278531_457239466', ])

                self.state = "manager"
            else:
                response[0] = self.default_answer()
        elif self.state == "evaluate":
            if message.text == '👍':
                response[0].set_text("Отлично! Если хочешь больше интересных физических историй и задачек, подпишись, чтобы не пропустить😊")
                keyboard = VkKeyboard(inline=True)
                link = "https://vk.com/widget_community.php?act=a_subscribe_box&oid=-163278531&state=1"
                keyboard.add_openlink_button(label='Подписаться', link=link)
                response[0].set_keyboard(keyboard)
            elif message.text == '👎':
                response[0].set_text("(")
            else:
                response[0] = self.default_answer()
            self.state = "start"
        elif message.text == "Начать":
            response[0] = self.default_answer()

        return tuple(response)
