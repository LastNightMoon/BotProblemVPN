from modules.botStates.BaseState import BaseState
from vpn.request import Request


class InfoState(BaseState):

    def init_internal(self):
        req = Request()
        user = req.get_user_info(self.user_name)
        self.send(f"Информация о вашем подключении:\n" +\
                  f"Скачано {user.down / 8} GB\n" +\
                  f"Загружено {user.up / 1024} GB\n" +\
                  f"Осталось {user.time / 60} дней"
                  f"Ссылка для подключения:")
        self.send(f"```{user.link}```")

