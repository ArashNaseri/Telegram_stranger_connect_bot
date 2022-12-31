import telebot
import os
from loguru import logger


class Telebot(object):
    def __init__(self):
        self.bot = telebot.TeleBot(
            os.environ['TELEGRAM_ANANYMOUS_BOT_TOKEN'],
            parse_mode=None
            ) # You can set parse_mode by default. HTML or MARKDOWN
            self.send_welcome_message=self.bot.message_handler(commands=['start','help'])

    def send_welcome_message(message):
        bot.reply_to(message, "Hey you!"))
    def run(self):
        logger.info("Lunching bot...")
        self.bot.polling()
    def __str__(self):
        pass
    def __repr__(self):
        pass

if __name__ == '__main__':
    bot = Telebot()
    bot.run()

