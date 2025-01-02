from modules.botStates.BaseState import BaseState
from modules.botStates.MainMenu import MainMenu
from vpn.request import Request


class NewUserState(BaseState):
    def init_internal(self):
        request = Request()
        if request.check_user(self.user_name):
            self.send("У вас уже есть аккаунт в этом боте, используйте уже существующую ссылку")
        else:
            self.send("Здравствуй пользователь, здесь вы можете довольно дёшово получить быстрый vpn.")
            request.create_user(self.user_name)
            self.send(
                "Мы выдаём вам ссылку, у вас есть возможность использовать 500 МБ для тестов. Инструкции и остальное вы можете найти в доп разделах.")
            return MainMenu(self)
