import requests
import re
import os

from threading import Thread
from Telegram import TelegramRequests, BotSqlite
from .commands.Bot_commands import Bot_commands
from .commands.Bot_plasure import Bot_plasure


class Bot(Bot_commands, Bot_plasure):
    """Бот для работы с телегой."""

    general_chat_id = -350117727
    pikuli_symbol = '☄️'

    def __init__(self, token):
        self.db = BotSqlite('PikBimBot.db')
        self.last_update = None
        self.last_update_id = self.db.get_param('last_update_id')
        self.token = token
        TelegramRequests.token = token

    def is_admin(self, upd):
        """Является ли отправитель админом данного сообщества?."""
        if upd.sender_id in \
            TelegramRequests.get_admins_ids(upd.chat_id):
            return True
        return False

    def work(self):
        """Работа бота."""
        last_update = self.get_last_update()
        if last_update:
            for i in last_update:
                p = Thread(target=self.work_thread, args=[i])
                p.start()


    def work_thread(self, last_update):
        """Функции выполняемые в каждом потоке."""
        if last_update.is_message:
            self.db.save_user(last_update)
            if last_update.is_common_chat:
                self.is_plasure(last_update)
                self.command_text(last_update)
                if last_update.command_names:
                    self.command_checker(last_update)
            # else:
            #     self.send_message('Общайтесь в общих чатах.')

    def get_updates(self, offset=None, timeout=30):
        """Получает обновления."""
        params = {'timeout': timeout, 'offset': offset}
        api_url = "https://api.telegram.org/bot{}/getUpdates".format(self.token)
        resp = requests.get(api_url, params)
        result_json = resp.json()['result']
        return result_json

    def get_last_update(self):
        """Получает последнее обновление."""
        if not self.last_update_id:
            get_result = self.get_updates()
        else:
            get_result = self.get_updates(offset=self.last_update_id)
        if len(get_result):
            for i in get_result:
                print(i)
            req = [TelegramRequests(i) for i in get_result]
            self.last_update_id = req[-1].update_id
            self.db.set_param('last_update_id', req[-1].update_id)
            return req