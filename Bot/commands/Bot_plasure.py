import re
from Telegram import TelegramRequests

class Bot_plasure:
    plasure_templates = ['спасибо', 'благодарю', 'спс', 'от души']

    def is_plasure(self, upd):
        templ = self.make_template(self.plasure_templates)
        templ_2 = self.make_template(self.plasure_templates, start_str="^@[\w\d_]+\s+")
        usernames = upd.message_usernames
        if (templ.search(upd.text) and usernames) or (upd.resend_id and templ.search(upd.text)):
            user_id = upd.sender_id
            if upd.resend_id:
                user_to_plasure_id = upd.resend_id
            elif usernames:
                user_to_plasure_id = self.db.get_user_id(usernames[0])
            if user_to_plasure_id:
                if user_to_plasure_id == user_id:
                    TelegramRequests.send_message(upd.chat_id, 'Себя благодарить не хорошо', deley=10)
                else:
                    if upd.resend_id:
                        TelegramRequests.resend_message(self.general_chat_id, upd.resend_chat_id, upd.resend_message_id)
                    self.db.make_plasure(user_to_plasure_id, user_id)
                    print("Поблагодарили пользователя {}".format(self.db.get_user_name(user_to_plasure_id)))
                    TelegramRequests.send_message(upd.chat_id, 'Вы поблагодарили @{} пикули  ☄️ пользователя равны {}'.format(self.db.get_user_name(user_to_plasure_id), self.db.get_user_likes(user_to_plasure_id)), deley=10)
        elif templ.search(upd.text):
            TelegramRequests.send_message(upd.chat_id, 'Если вы хотите поблагодарить кого-нибудь - отправьте которое начинается с "@username Спасибо" или ответом на сообщение помощника.', deley=10)

    def make_template(self, arr, start_str=""):
        """Делает из массива регулярное выражение на содержит."""
        templ = start_str
        pos = 1
        for i in arr:
            templ += "({})".format(i)
            if pos != len(arr):
                templ += '|'
            pos += 1
        return re.compile(templ, re.IGNORECASE)

    def resend_pleasure(self, upd):
        if upd.resend_from:
            upd.resend_from
        return False