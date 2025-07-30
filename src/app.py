import types

import telebot
from telebot.custom_filters import StateFilter
from telebot.handler_backends import State, StatesGroup
from telebot.types import Message

from bot.handler import answer_analyze, get_question, get_text_from_voice
from config import Config
from logger import logger

cfg = Config()


# TODO: вынести состояния
class UserStates(StatesGroup):
    ANSWERING = State()  # Пользователь отвечает на вопрос
    WAITING_FEEADBACK = State()  # Пользоавтель ждет обратную связь


logger.info("Инициализация бота")

bot = telebot.TeleBot(cfg.TG_TOKEN)


@bot.message_handler(state=UserStates.ANSWERING, content_types=["voice"])
def handle_answer(message: Message):
    logger.info("Получен ответ от пользователя")

    text_answer = get_text_from_voice(bot, message)
    logger.info(f"Ответ пользователя расшифрован {text_answer}")

    feedback = answer_analyze(text_answer)
    logger.info("Ответ проанализирован")

    bot.send_message(message.chat.id, feedback)

    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(commands=["next"])
def send_question(message):
    logger.debug("Пользователь запросил вопрос")
    response = get_question()

    bot.set_state(message.from_user.id, UserStates.ANSWERING, message.chat.id)
    logger.debug(f"Состояние пользователя измененно на {bot.get_state(message.from_user.id, message.chat.id)}")

    bot.send_message(message.chat.id, response)
    logger.debug(f"Пользователю отправлен вопрос {response}")


bot.add_custom_filter(StateFilter(bot))
bot.polling(none_stop=True)
