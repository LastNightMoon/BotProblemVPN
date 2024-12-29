from telebot.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from modules.botStates.HelpState import HelpState
from modules.botStates.BaseState import BaseState


class MainMenu(BaseState):
	main_button = {
		"help": {
			"state": HelpState,
			"text": "Помощь"
		},
		# "": {
		#
		# }
	}

	def init_internal(self):
		keyboard = ReplyKeyboardMarkup(True, True)
		for button in self.main_button.values():
			keyboard.add(KeyboardButton(button["text"]))
		self.send("Добро пожаловать в главное меню VPN - сервиса.", reply_markup=keyboard)

	def receive_message(self, message: Message):
		for button in self.main_button.values():
			if button["text"] == message.text:
				return button["state"](self.bot, self.chat)
		return self

	def receive_callback(self, call: CallbackQuery):
		return self
