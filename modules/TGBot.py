from modules.botStates.MainMenu import MainMenu

import telebot
from telebot import types
from telebot.types import Message, CallbackQuery
import os


class TGBot:
	def __init__(self):
		self.token = os.environ['TOKEN_BOT']
		self.bot = telebot.TeleBot(self.token)
		self.data = {}

		@self.bot.message_handler(content_types = ['text'])
		def receive_message(message: Message):
			print(message.text)
			if (not (message.text == '/start' or message.text == "Назад в основное меню") and
					message.from_user.id in self.data.keys()):
				self.data[message.from_user.id]["state"].receive_message(message)
			# elif :
			# 	self.data[message.from_user.id] = {"state" : MainMenu()}
			else:
				self.data[message.from_user.id] = {"state": MainMenu(self.bot, message.from_user.id)}

		@self.bot.callback_query_handler(func = lambda call: True)
		def receive_callback(message: CallbackQuery):
			print(message.data)

		self.bot.infinity_polling()
