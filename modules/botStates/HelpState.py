from telebot.types import Message, CallbackQuery

from modules.botStates.BaseState import BaseState


class HelpState(BaseState):
	main_button = [
		"Помощь с стандартными ошибками",
		"Помощь с получением токена доступа"
		"Помощь в подключении",
		"Назад в основное меню",
	]

	def init_internal(self):
		helpText = "тут общий текст помощи"

		self.send(helpText)

	def receive_message(self, message: Message):
		if message.text == self.main_button[0]:
			self.send("я не в курсе о чём вы")
		elif message.text == self.main_button[1]:
			self.send("твово")
		elif message.text == self.main_button[2]:
			self.send("Выберите операционную систему")
			return
		elif message.text == self.main_button[3]:
			self.send("")
		return self

	def receive_callback(self, call: CallbackQuery):
		return self



