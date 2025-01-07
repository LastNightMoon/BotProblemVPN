import os

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from modules.botStates.BaseState import BaseState


class PayState(BaseState):
    def init_internal(self):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Подтвердить", callback_data="pay"))
        self.send(
            "В настоящее время ИП и подобное не открыто, поэтому приём через онлайн кассу невозможен Поэтому пока переводом [Телефон](+79535588202) Т-Банк, как переведёте, нажмите на подтвердить, сообщению уйдёт администратору, если перевод был, продление будет зафиксировано",
            parse_mode="Markdown", reply_markup=keyboard)

    def receive_callback(self, call: CallbackQuery, user_data: dict):
        if call.data == "pay":
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton("Да", callback_data=f"yap_yes_{self.chat}_{self.user_name}"))
            keyboard.add(InlineKeyboardButton("Нет", callback_data=f"yap_not_{self.chat}_{self.user_name}"))
            self.bot.send_message(os.environ["CHANEL"], f"Пользователь {self.user_name} совершил оплату?", reply_markup=keyboard)
            self.send("Запрос отправлен.")
        return self