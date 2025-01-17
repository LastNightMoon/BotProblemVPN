from telebot.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from modules.botStates.InfoState import InfoState
from modules.botStates.PayState import PayState
from modules.botStates.TaskState import TaskState
from modules.botStates.help.HelpState import HelpState
from modules.botStates.BaseState import BaseState


class MainMenu(BaseState):
    main_button = {
        "help": {
            "state": HelpState,
            "text": "Помощь"
        },
        "info": {
            "text": "Информация",
            "state": InfoState,
        }, "pay":
        {
            "state": PayState,
            "text": "Оплата"
        },
        "task": {
            "text": "Сообщить о проблеме",
            "state": TaskState,
        }
    }

    def init_internal(self):
        keyboard = ReplyKeyboardMarkup(True, True)
        for button in self.main_button.values():
            keyboard.add(KeyboardButton(button["text"]))
        self.send("Добро пожаловать в главное меню VPN - сервиса.", reply_markup=keyboard)

    def receive_message(self, message: Message, user_data: dict):
        for button in self.main_button.values():
            if button["text"] == message.text:
                return button["state"](self)
        return self

    def receive_callback(self, call: CallbackQuery, user_data: dict):
        return self
