from Bot import Bot
token = "947439980:AAEaKwOo0S85yUYfUc2IyIE0W-UKpAyC8_4"


def main():
    """Функция работы бота."""
    bot = Bot(token)
    while True:
        bot.work()

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()