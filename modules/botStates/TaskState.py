import os

from telebot.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

from modules.botStates.help.HelpState import HelpState
from modules.botStates.BaseState import BaseState


class TaskState(BaseState):
    main_button = {

    }

    def init_internal(self):
        self.send("Расскажите, что у вас случилось?")

    def receive_message(self, message: Message, user_data: dict):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Да", callback_data="yes"))
        keyboard.add(InlineKeyboardButton("Нет", callback_data="no"))
        user_data["req"] = message.text
        self.send(f"Проблема: {message.text}\nВсё правильно?", reply_markup=keyboard)
        return self

    def receive_callback(self, call: CallbackQuery, user_data: dict):
        if call.data == "yes":
            self.bot.send_message(os.environ["CHANEL"],
                                  f"Новый запрос от {call.from_user.username} : " + user_data["req"])
            self.send("Запрос передан на исполнение")
        elif call.data == "no":
            self.init_internal()
        return self
