import telebot
from telebot.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from modules.botStates.BaseState import BaseState


class OSHelpState(BaseState):
    main_button = {
        "Windows": ["Шаг 1", "Шаг 2"], "Linux": [""], "Android": [""], "Product Apple": [""]
    }

    def init_internal(self):
        self.send("VPN можно подключить на любые девайсы, инструкции как "
                  "подключать для разных ОС представлены здесь.",
                  reply_markup=self.generate_reply_keyboard(list(self.main_button.keys())))

    def receive_message(self, message: Message, user_data: dict):
        if message.text in self.main_button.keys():
            for message in self.main_button[message.text]:
                self.send(message)
        return self

    def receive_callback(self, call: CallbackQuery, user_data: dict):
        return self
