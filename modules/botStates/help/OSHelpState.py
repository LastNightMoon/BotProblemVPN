import telebot
from telebot.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from modules.botStates.BaseState import BaseState


class OSHelpState(BaseState):
    main_button = {
        "Windows": ["Установите приложение V2rayN, вот ссылка",
                    "Выберите раздел Сервера и там нажмите на Импорт массива URL из буфера обмена (CtrI+V)",
                    "Внизу есть настройки, их нужно немного поменять:",
                    "1. Маршрутизация - уровень Global",
                    "2. Настройки системного прокси: Очистить системный прокси - VPN не работает, Установить системный прокси - Vpn включён"
                    "3. Режим VPN - выключен: перехват только браузеров, включён: перехват всего трафика компютера"],
        "Linux": [""],
        "Android": ["Установите приложение V2rayNG, вот ссылка",
                    "Откройте его, в верхнем меню нажмите на + потом импорт из буфера обмена.",
                    "Для включения vpn на всём устройстве нажмите на пуск (оранжевый треугольник снизу)"],
        "Product Apple": ["В офицальном магазине приложений для вашего устройства скачайте приложение , вот ссылка.",
                          ""]
    }

    def init_internal(self):
        self.send("VPN можно подключить на любые девайсы, инструкции как "
                  "подключать для разных ОС представлены здесь. Перед каждым шагом из всех описанных ниже скопируйте vless ссылку из раздела про информацию.",
                  reply_markup=self.generate_reply_keyboard(list(self.main_button.keys())))

    def receive_message(self, message: Message, user_data: dict):
        if message.text in self.main_button.keys():
            for message in self.main_button[message.text]:
                self.send(message, )
        return self

    def receive_callback(self, call: CallbackQuery, user_data: dict):
        return self
