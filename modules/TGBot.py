from modules.botStates.MainMenu import MainMenu

import telebot
from telebot import types
from telebot.types import Message, CallbackQuery
import os

from modules.botStates.NewUserState import NewUserState


class TGBot:
    def __init__(self):
        self.token = os.environ['TOKEN_BOT']
        self.bot = telebot.TeleBot(self.token)
        self.data = {}

        @self.bot.message_handler(content_types=['text'])
        def receive_message(message: Message):
            print(message.text)
            if (not (message.text == '/start' or message.text == "Назад в основное меню") and
                    message.from_user.id in self.data.keys()):
                self.data[message.from_user.id]["state"] = (self.data[message.from_user.id]["state"].
                                                            receive_message(message,
                                                                            self.data[message.from_user.id]["data"]))
            elif message.text == "/start":
                self.data[message.from_user.id] = {
                    "state": NewUserState(self.bot, message.from_user.id, message.from_user.username), }
            else:
                self.data[message.from_user.id] = {
                    "state": MainMenu(self.bot, message.from_user.id, message.from_user.username), "data": {}}
            print(self.data)

        @self.bot.callback_query_handler(func=lambda call: True)
        def receive_callback(call: CallbackQuery):
            print(call.data)

            if call.from_user.id in self.data.keys():
                self.data[call.from_user.id]["state"] = (self.data[call.from_user.id]["state"].
                                                         receive_callback(call, self.data[call.from_user.id]["data"]))
            # elif :
            # 	self.data[message.from_user.id] = {"state" : MainMenu()}
            else:
                self.data[call.from_user.id] = {"state": MainMenu(self.bot, call.from_user.id, call.from_user.username),
                                                "data": {}}
            print(self.data)

        self.bot.infinity_polling(timeout=1000)
