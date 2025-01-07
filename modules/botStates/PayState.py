from modules.botStates.BaseState import BaseState


class PayState(BaseState):
    def init_internal(self):
        self.send("В настоящее время ИП и подобное не открыто, поэтому приём через онлайн кассу невозможен")

