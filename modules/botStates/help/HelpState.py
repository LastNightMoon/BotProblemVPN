from telebot.types import Message, CallbackQuery

from modules.botStates.BaseState import BaseState
from modules.botStates.help.OSHelpState import OSHelpState


class HelpState(BaseState):
	main_button = [
		"Помощь с стандартными ошибками",
		"Помощь с получением токена доступа",
		"Помощь в подключении",
		"Назад в основное меню",
	]

	def init_internal(self):
		helpText = "Тут вы можете узнать ответы на основные вопросы."
		self.send(helpText, reply_markup=self.generate_reply_keyboard(self.main_button))

	def receive_message(self, message: Message, user_data: dict):
		if message.text == self.main_button[0]:
			self.send("я не в курсе о чём вы, ошибок нет, если есть напишите через подачу заявок.")
		elif message.text == self.main_button[1]:
			self.send("Токен доступа к серверу вы получили при регистрации, чтобы вы можете испотзовать его на всех своих устройствах, если вы хотите получить нового пользователя зайдите с другого аккаунта.")
		elif message.text == self.main_button[2]:
			return OSHelpState(self.bot, self.chat)
		return self

	def receive_callback(self, call: CallbackQuery, user_data: dict):
		return self



