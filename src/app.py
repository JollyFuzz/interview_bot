import types

import telebot
from telebot.custom_filters import StateFilter
from telebot.handler_backends import State, StatesGroup
from telebot.types import Message

from bot.handler import answer_analyze, get_question, get_text_from_voice
from config import cfg
from logger import logger


# TODO: вынести состояния
class UserStates(StatesGroup):
    ANSWERING = State()  # Пользователь отвечает на вопрос
    WAITING_FEEADBACK = State()  # Пользоавтель ждет обратную связь


logger.info("Инициализация бота")

bot = telebot.TeleBot(cfg.TG_TOKEN)


@bot.message_handler(commands=["start_session"])
def start_session(message):
    """
    Начинаем сессию вопрос-ответ.
    Отправляем пользователю вопрос и меняем состояние пользователя на ANSWERING
    """
    logger.debug("Пользователь запросил вопрос")
    try:
        response = get_question()

        bot.set_state(message.from_user.id, UserStates.ANSWERING, message.chat.id)
        logger.debug(f"Состояние пользователя измененно на {bot.get_state(message.from_user.id, message.chat.id)}")

        bot.send_message(message.chat.id, response)
        logger.debug(f"Пользователю отправлен вопрос {response}")
    except Exception as e:
        logger.error(f"Неудалось получить вопрос {e}")
        bot.send_message(message.chat.id, "Не удалось получить вопрос. Попробуйте позже")


@bot.message_handler(state=UserStates.ANSWERING, content_types=["voice"])
def handle_answer(message: Message):
    """
    Обрабатываем ответ пользователя.
    Ответ ожидается в виде голосового сообщения.
    """
    logger.info("Получен ответ от пользователя")

    text_answer = get_text_from_voice(bot, message)
    logger.info(f"Ответ пользователя расшифрован {text_answer}")

    feedback = answer_analyze(text_answer)
    logger.info("Ответ проанализирован")

    bot.send_message(message.chat.id, feedback)

    bot.delete_state(message.from_user.id, message.chat.id)


bot.add_custom_filter(StateFilter(bot))
bot.polling(none_stop=True)
