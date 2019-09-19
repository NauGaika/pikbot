import re
import sys
from Telegram import TelegramRequests

class Bot_commands:
    def command_checker(self, upd):
        """Проверяет какая команда была выполнена."""
        commands = upd.command_names
        if upd.message_usernames:
            username = upd.message_usernames[0]
        if 'idea' in commands:
            TelegramRequests.resend_message(self.general_chat_id, upd.chat_id, upd.message_id)
        # elif 'add' in commands:
        #     self.add_carma(upd, username)
        # elif 'substract' in commands:
        #     self.substract_carma(upd, username)
        # elif 'nulify' in commands:
        #     self.nulify_carma(username)
        elif 'pikuli' in commands:
            self.my_pikuli(upd)
        elif 'top' in commands:
            self.show_top(upd)
        elif 'help' in commands:
            self.show_help(upd)

    def command_text(self, upd):
        if 'Сергей лучший координатор' in upd.text:
            stikers = TelegramRequests.get_stiker_set('BimBroStikers')
            TelegramRequests.send_message(upd.chat_id, "Абсолютно верно!", deley=1)

    def my_pikuli(self, upd):
        """Моя карма."""
        pikuli = self.db.get_user_likes(upd.sender_id)
        TelegramRequests.send_message(upd.chat_id, "@{}, У вас {} пикуль.".format(self.db.get_user_name(upd.sender_id), pikuli), deley=10)

    def show_top(self, upd, deley=10):
        """Показывает текущий топ пользователей."""
        new_str = 'Топ BIM помощников \n\r\n\r'
        iterator = 1
        smiles = ['🥉', '🥈', '🥇']
        for i in self.db.get_top():
            if smiles:
                new_str += smiles.pop()
            new_str += "{}. {} - {} ☄️\n\r".format(iterator, i[0], i[1])
            iterator += 1
        TelegramRequests.send_message(upd.chat_id, new_str, deley=deley)

    def show_help(self, upd):
        new_str = 'Справка бота \n\r\n\r'
        new_str += '"/help" - справка\n\r'
        new_str += '"/top" - текущий рейтинг бим помощников\n\r'
        new_str += '"/pikuli" - ваши текущие пикули {}\n\r'.format(self.pikuli_symbol)
        new_str += '"/idea идея которая будет отправлена в бим отдел" - с помощью этой команды можно отправить идею в бим отдел \n\r'
        TelegramRequests.send_message(upd.chat_id, new_str, deley=10)

    def add_carma(self, upd, username):
        """Добавить карму. /add @user 100"""
        text = upd.text
        if self.is_admin:
            num = re.search('\d+', text.replace('/add', '').replace(username, ''))
            if num:
                num = num.group(0).strip()
                if num.isdigit:
                    num = int(num)
                    self.db.add_carma(username, num)
                    self.send_message("Вы добавили пользователю {} {} пикуль {}".format(username, num, self.pikuli_symbol))
        else:
            self.send_message("Добавлять пикули {} могут только администраторы".format(self.pikuli_symbol))

    def substract_carma(self, upd, username):
        """Забрать карму. /add @user 100"""
        text = upd.text
        if self.is_admin:
            num = re.search('\d+', text.replace('/substract', '').replace(username, ''))
            if num:
                num = num.group(0).strip()
                if num.isdigit:
                    num = int(num)
                    self.db.substract_carma(username, num)
                    self.send_message("Вы забрали у пользователя {} {} пикуль {}".format(username, num, self.pikuli_symbol))
        else:
            self.send_message("Забирать пикули {} могут только администраторы".format(self.pikuli_symbol))

    def nulify_carma(self, username):
        """Обнулить карму."""
        if self.is_admin:
            self.db.nulify_carma(username)
            self.send_message("Вы обнулили пикули {} пользователя {}".format(self.pikuli_symbol, username))
        else:
            self.send_message("Обнулять пикули могут только администраторы")

    def send_stiker(self, obj, stiker):
        TelegramRequests.send_stiker(self.token, obj.chat_id, stiker)
