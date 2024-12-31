import telebot
from telebot.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton


class BaseState:
	def __init__(self, bot: telebot.TeleBot, chat: int):
		self.bot = bot
		self.chat = chat
		self.init_internal()

	def send(self, *args, **kwargs):
		if "reply_markup" not in kwargs:
			kwargs["reply_markup"] = ReplyKeyboardMarkup(True, True)
			kwargs["reply_markup"].add(KeyboardButton("Назад в основное меню"))
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