from modules.botStates.BaseState import BaseState


class NewUserState(BaseState):
    def init_internal(self):
        self.send("Здравствуй пользователь, здесь вы можете довольно дёшово получить быстрый vpn.")

