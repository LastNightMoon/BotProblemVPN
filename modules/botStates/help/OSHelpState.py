import telebot
from telebot.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from modules.botStates.BaseState import BaseState


class OSHelpState(BaseState):
    main_button = {
        "Windows": [
            "1. Установите приложение V2rayN, [вот ссылка](https://github.com/2dust/v2rayN/releases).",
            "2. Выберите раздел 'Сервера' и нажмите на 'Импорт массива URL из буфера обмена (Ctrl+V)'.",
            "3. Измените настройки внизу экрана:",
            "   - Маршрутизация: уровень Global.",
            "   - Настройки системного прокси:",
            "     - Очистить системный прокси — VPN не работает.",
            "     - Установить системный прокси — VPN включён.",
            "   - Режим VPN:",
            "     - Выключен: перехватывается только трафик браузеров.",
            "     - Включён: перехватывается весь трафик компьютера."
        ],
        "Linux": [
            "1. Скачайте приложение nekoray с официального репозитория: [вот ссылка](https://github.com/MatsuriDayo/nekoray/releases). Выберите версию для вашей ОС.",
            "2. Установите приложение (например, для Debian используйте .deb-файл).",
            "3. Запустите приложение, затем скопируйте вашу новую ссылку VLESS и вставьте её в nekoray.",
            "4. Настройте режим работы:",
            "   - Системный прокси для браузеров.",
            "   - Режим tun для всех приложений (примечание: tun может быть медленным на виртуалках)."
        ],
        "Android": [
            "1. Установите приложение V2rayNG, вот ссылка.",
            "2. Откройте приложение, нажмите на '+' в верхнем меню, затем выберите 'Импорт из буфера обмена'.",
            "3. Для включения VPN на всём устройстве нажмите на кнопку пуск (оранжевый треугольник внизу экрана)."
        ],
        "Product Apple": [
            "1. Скачайте приложение FoXray из официального магазина приложений: [вот ссылка](https://apps.apple.com/ru/app/foxray/id6448898396?ref=dtf.ru).",
            "2. Установите приложение, соответствующее вашей платформе.",
            "3. Запустите приложение, затем скопируйте вашу новую ссылку VLESS и вставьте её.",
            "4. Настройте режим работы:",
            "   - Системный прокси для браузеров.",
            "   - Режим tun для всех приложений (при необходимости)."
        ]
    }

    def init_internal(self):
        self.send(
            "VPN можно подключить на любые устройства. Инструкции для различных операционных систем представлены ниже.\n"
            "Перед началом скопируйте VLESS-ссылку из раздела 'Информация'.",
            reply_markup=self.generate_reply_keyboard(list(self.main_button.keys()))
        )

    def receive_message(self, message: Message, user_data: dict):
        if message.text in self.main_button.keys():
            for msg in self.main_button[message.text]:
                self.send(msg, parse_mode="Markdown")
        return self

    def receive_callback(self, call: CallbackQuery, user_data: dict):
        return self
