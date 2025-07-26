import types

import telebot

from bot.handler import get_question
from config import Config
from logger import logger

cfg = Config()

logger.info("Инициализация бота")

bot = telebot.TeleBot(cfg.TG_TOKEN)


@bot.message_handler(commands=["next"])
def handle_next(message):  # TODO: переименовать
    response = get_question()
    bot.reply_to(message, response)


bot.polling(none_stop=True, interval=0)  # обязательная для работы бота часть
