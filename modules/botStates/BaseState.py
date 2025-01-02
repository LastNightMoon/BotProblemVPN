from typing import Union

import telebot
from functools import singledispatchmethod
from telebot.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton


class BaseState:
	def __init__(self, bot_or_obj: Union[telebot.TeleBot, 'BaseState'], chat: int = None, user_name: str = None):
		if isinstance(bot_or_obj, telebot.TeleBot):
			self.bot = bot_or_obj
			self.chat = chat
			self.user_name = user_name
		elif isinstance(bot_or_obj, BaseState):
			self.bot = bot_or_obj.bot
			self.chat = bot_or_obj.chat
			self.user_name = bot_or_obj.user_name
		self.init_internal()

	def send(self, *args, **kwargs):
		if "reply_markup" not in kwargs:
			kwargs["reply_markup"] = ReplyKeyboardMarkup(resize_keyboard=True)
			kwargs["reply_markup"].add(KeyboardButton("Назад в основное меню"))
		kwargs["reply_markup"].resize_keyboard=True
		return self.bot.send_message(self.chat, *args, **kwargs)

	def init_internal(self):
		pass

	def receive_message(self, message: Message, user_data: dict):
		return self

	def receive_callback(self, call: CallbackQuery, user_data: dict):
		return self

	@staticmethod
	def generate_reply_keyboard(buttons : list[str]):
		keyboard = ReplyKeyboardMarkup(True, True)
		for button in buttons:
			keyboard.add(KeyboardButton(button))
		return keyboard