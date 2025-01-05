import datetime

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from modules.botStates.BaseState import BaseState
from vpn.request import Request


class InfoState(BaseState):

    def init_internal(self):
        req = Request()
        user = req.get_user_info(self.user_name)
        self.send(f"Информация о вашем подключении:\n" +\
                  f"Скачано: {round(user.down / 1024**3, 1)} GB\n" +\
                  f"Загружено: {round(user.up / 1024**3, 1)} GB\n" +\
                  f"Последний день: {datetime.datetime.fromtimestamp(user.time / 1000).strftime("%d:%m:%Y") if user.time else "Воу, у вас бесконечное кол - во"} дней\n" +\
                  f"Ссылка для подключения:")
        self.send(f"```\n{user.link}\n```", parse_mode="MarkdownV2")

