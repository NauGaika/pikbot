from .TelegramRequestsMethod import TelegramRequestsMethod
from .TelegramRequestsProperty import TelegramRequestsProperty

class TelegramRequests(TelegramRequestsMethod, TelegramRequestsProperty):
    """Класс по работе с запросами на телегу."""
    token = None

    def __init__(self, update):
        self.obj = update