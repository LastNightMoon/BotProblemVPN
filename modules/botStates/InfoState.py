from modules.botStates.BaseState import BaseState
from vpn.request import Request


class InfoState(BaseState):

    def init_internal(self):
        req = Request()
        user = req.get_user_info(self.user_name)
        self.send(f"{user.tag}")