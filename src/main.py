import telebot
import os
from loguru import logger
from utils import create_keyboard
from constants import keyboards
from constants import state
from constants import keys
import emoji


class Telebot(object):
    def __init__(self):
        self.bot = telebot.TeleBot(
            os.environ['TELEGRAM_ANANYMOUS_BOT_TOKEN'],
            parse_mode='HTML'
            ) # You can set parse_mode by default. HTML or MARKDOWN

        self.respond_welcome = self.bot.message_handler(commands=['start','help'])(self.respond_welcome)
        self.respond_text = self.bot.message_handler(func=lambda message: True)(self.respond_text)

        #keep user state
        self.users = dict()

    def run(self):
        logger.info("Lunching bot...")
        self.bot.polling()

    def respond_welcome(self, message):
        self.set(message)
        self.bot.send_message(message.chat.id, f'Hey <b> {self.name}</b>!',
        reply_markup=keyboards.main
        )

    def respond_text(self, message):

        logger.info(emoji.demojize(message.text))
        self.set(message)
        message.text = emoji.demojize(message.text)
        print(message.text)
        # taking to strangers
        if self.get_state() == state.talking:
            self.send_message(message.text,self.users[self.chat_id]['random_connection'])
        #start looking for strangers to connect
        elif message.text == keys.random_connect:
            self.send_message(
                ':hourglass_not_done: Waiting for someone to connect...',
                reply_markup=keyboards.back
            )
            self.set_state(state.random_connect)
        # Setting state
        elif message.text == keys.settings:
            self.send_message(
                keys.settings,
                reply_markup=keyboards.back
            )
            self.set_state(state.settings)
        #Back
        elif message.text == keys.back:
            self.send_message(
                keys.back,
                reply_markup=keyboards.main
            )
            self.set_state(state.init)
        # connect to stranger
        if self.get_state() == state.random_connect:
            self.connect()

    def connect(self):
        print('self.users')
        #find someone in random connect state
        for chat_id, info in self.users.items():
            if chat_id == self.chat_id:
                continue
            if info['state'] != state.random_connect:
                continue

            self.send_message(
                f':check_mark_botton: Congragulation!!!, connected to {chat_id}! Start talking...!',
                chat_id=self.chat_id, reply_markup=keyboards.talking,
            )
            self.send_message(
                f':check_mark_botton: Congragulation!!!, connected to {self.chat_id}! Start talking...!',
                chat_id=chat_id, reply_markup=keyboards.talking,
            )
            self.users[self.chat_id]['random_conection']=chat_id
            self.users[chat_id]['random_conection']=self.chat_id

            self.set_state(state.talking, self.chat_id)
            self.set_state(state.talking, chat_id)

    def set(self, message):
        self.message = message
        self.name = message.chat.first_name
        if message.chat.last_name:
            self.name = f'{self.name} {self.message.chat.last_name}'

        self.chat_id = message.chat.id
        logger.info(f'chat id: {self.chat_id}')

        if not self.users.get(self.chat_id):
            self.users[self.chat_id] = dict(
                username=message.chat.username,
            )

    def set_state(self, state, chat_id=None):
        if chat_id is None:
            chat_id = self.chat_id

        self.users[chat_id]['state']=state
        logger.info(f'Set state to --> "{state}"')

    def get_state(self):
        return self.users[self.chat_id].get('state')

    def send_message(self, bot_response, chat_id=None, reply_markup=None, emojize=True):
        if emojize:
            bot_response = emoji.emojize(bot_response)
        if not chat_id:
            chat_id = self.message.chat.id
        self.bot.send_message(chat_id, bot_response, reply_markup=reply_markup)


if __name__ == '__main__':
    bot = Telebot()
    bot.run()
