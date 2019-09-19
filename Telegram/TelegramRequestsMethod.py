import time
import requests

class TelegramRequestsMethod:
    @classmethod
    def send_message(cls, chat_id, text, token=None, deley=0):
        if cls.token:
            token = cls.token
        params = {'chat_id': chat_id, 'text': text}
        api_url = "https://api.telegram.org/bot{}/".format(token)
        method = 'sendMessage'
        resp = requests.post(api_url + method, params)
        resp = resp.json()['result']
        if deley:
            cls.delete_message(chat_id, resp['message_id'], deley=deley, token=token)
            return
        return resp

    @classmethod
    def delete_message(cls, chat_id, message_id, token = None, deley=0):
        if cls.token:
            token = cls.token
        params = {'chat_id': chat_id, 'message_id': message_id}
        api_url = "https://api.telegram.org/bot{}/".format(token)
        method = 'deleteMessage'
        if deley:
            time.sleep(deley)
        requests.post(api_url + method, params)

    @classmethod
    def get_admins_ids(cls, chat_id, token=None):
        if cls.token:
            token = cls.token
        params = {'chat_id': chat_id}
        api_url = "https://api.telegram.org/bot{}/".format(token)
        method = 'getChatAdministrators'
        resp = requests.post(api_url + method, params)
        if resp:
            return [i['user']['id'] for i in resp.json()['result']]
        return []

    @classmethod
    def resend_message(cls, chat_id, chat_id_from, message_id, token=None):
        if cls.token:
            token = cls.token
        params = {'chat_id': chat_id, 'from_chat_id': chat_id_from, 'message_id': message_id}
        api_url = "https://api.telegram.org/bot{}/".format(token)
        method = 'forwardMessage'
        resp = requests.post(api_url + method, params)

    @classmethod
    def send_stiker(cls, chat_id, sticker, token=None, deley=0):
        if cls.token:
            token = cls.token
        params = {'chat_id': chat_id, 'sticker': sticker}
        api_url = "https://api.telegram.org/bot{}/".format(token)
        method = 'sendSticker'
        resp = requests.post(api_url + method, params)
        resp = resp.json()['result']
        cls.delete_message(resp['chat']['id'], resp['message_id'], deley=deley)
        return resp

    @classmethod
    def get_stiker_set(cls, name, token=None):
        if cls.token:
            token = cls.token
        params = {'name': name}
        api_url = "https://api.telegram.org/bot{}/".format(token)
        method ='getStickerSet'
        resp = requests.post(api_url + method, params)
        resp = resp.json()['result']
        tt = []
        for i in resp['stickers']:
            tt.append(i['file_id'])
        return tt

    @classmethod
    def get_file(cls, file_id, token=None):
        if cls.token:
            token = cls.token
        params = {'file_id': file_id}
        api_url = "https://api.telegram.org/bot{}/".format(token)
        method ='getFile' 
        resp = requests.post(api_url + method, params)
        resp = resp.json()['result']
        return resp['file_path']