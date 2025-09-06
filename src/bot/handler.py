"""
Функции обработки для телеграм бота
"""

import os

from services.message_transcription_service import message_transcription
from services.qa_service import QA_Service


def get_question():
    """
    Получить случайный вопрос из базы
    """
    qa_service = QA_Service()
    question = qa_service.get_random_question()
    return question


def get_text_from_voice(bot, message):
    """
    Парсинг голосового сообщения и получение текста из него
    """
    voice_file = "voice.ogg"

    # Получаем информацию о голосовом сообщении
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Сохраняем файл локально
    with open(voice_file, "wb") as f:
        f.write(downloaded_file)

    # Получение текста из голосового
    result = message_transcription(voice_file)

    # Удаляем файл
    os.remove(voice_file)

    return result


def answer_analyze(user_answer: str) -> str:
    """
    Обработка ответа пользователя
    Сейчас функция-заглушка
    """
    return "Вы абсолютно правы"
