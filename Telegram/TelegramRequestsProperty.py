class TelegramRequestsProperty:

    @property
    def message_id(self):
        """Id сообщения."""
        return self.obj['message']['message_id']

    @property
    def sender_id(self):
        """Отправитель сообщения."""
        return self.obj['message']['from']['id']

    @property
    def chat_id(self):
        """ID чата отправителя."""
        return self.obj['message']['chat']['id']

    @property
    def username(self):
        """username сообщения."""
        if "username" in self.obj['message']['from'].keys():
            return self.obj['message']['from']['username']

    @property
    def first_name(self):
        """first_name сообщения."""
        if "first_name" in self.obj['message']['from'].keys():
            return self.obj['message']['from']['first_name']

    @property
    def last_name(self):
        """last_name сообщения."""
        if "last_name" in self.obj['message']['from'].keys():
            return self.obj['message']['from']['last_name']

    @property
    def text(self):
        return self.obj['message']['text']

    @property
    def update_id(self):
        return self.obj['update_id'] + 1

    @property
    def resend_chat_id(self):
        """Id чата отправителя."""
        if 'reply_to_message' in self.obj['message'].keys():
            return self.obj['message']['reply_to_message']['chat']['id']

    @property
    def resend_username(self, cur_chat=False):
        """От кого отправлено сообщение."""
        if 'reply_to_message' in self.obj['message'].keys():
            if 'username' in self.obj['message']['reply_to_message']['from'].keys():
                return self.obj['message']['reply_to_message']['from']['username']
    @property
    def resend_id(self, cur_chat=False):
        """От кого отправлено сообщение."""
        if 'reply_to_message' in self.obj['message'].keys():
            if 'username' in self.obj['message']['reply_to_message']['from'].keys():
                return self.obj['message']['reply_to_message']['from']['id']

    @property
    def resend_message_id(self):
        """id пользователя перенаправленного сообщения."""
        if 'reply_to_message' in self.obj['message'].keys():
            return self.obj['message']['reply_to_message']['message_id']

    @property
    def is_message(self):
        """Является ли сообщением."""
        if 'message' in self.obj.keys():
            return 'text' in self.obj['message'].keys()

    @property
    def is_common_chat(self):
        """Является ли чат общим или индивидуальным."""
        if 'chat' in self.obj['message'].keys():
            if 'type' in self.obj['message']['chat'].keys():
                if self.obj['message']['chat']['type'] == 'group' or self.obj['message']['chat']['type'] == 'supergroup':
                    return True

    @property
    def command_names(self):
        """Наименование команд."""
        commands = []
        if 'entities' in self.obj['message'].keys():
            if 'type' in self.obj['message']['entities'][0].keys():
                for i in self.obj['message']['entities']:
                    if 'type' in i.keys():
                        if i['type'] == 'bot_command':
                            commands.append(self.text[i['offset']+1:i['offset'] + i['length']].split('@')[0])
        return commands

    @property
    def message_usernames(self):
        """Пользователи указанные в сообщении"""
        names =[]
        if 'entities' in self.obj['message'].keys():
            if 'type' in self.obj['message']['entities'][0].keys():
                for i in self.obj['message']['entities']:
                    if 'type' in i.keys():
                        if i['type'] == 'mention':
                            names.append(self.text[i['offset']+1 : i['offset'] + i['length']])
        return names