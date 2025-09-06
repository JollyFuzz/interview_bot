"""
Функции обработки для телеграм бота
"""

import os

import numpy as np
import torch
from pydub import AudioSegment
from transformers import WhisperForConditionalGeneration, WhisperProcessor

from db.mongo_repository import QA_Repository

device = "cuda" if torch.cuda.is_available() else "cpu"


def get_question():
    """
    Получить случайный вопрос из базы
    """
    client = QA_Repository()
    qa = client.get_random_qa()
    return qa["question"]


def get_text_from_voice(downloaded_file: bytes) -> str:
    """
    Парсинг голосового сообщения и получение текста из него
    """
    voice_file = "voice.ogg"

    # Сохраняем файл локально
    with open(voice_file, "wb") as f:
        f.write(downloaded_file)

    # Получение текста из голосового

    # Загрузка модели и токенизатора
    processor = WhisperProcessor.from_pretrained("openai/whisper-medium")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium").to(device)
    model.config.forced_decoder_ids = None

    # Загружаем аудио с помощью pydub
    audio = AudioSegment.from_file(voice_file)

    # Whisper работает с частотой дискретизации 16000 Гц
    audio = audio.set_frame_rate(16000)
    audio = audio.set_channels(1)  # моно
    audio = audio.set_sample_width(2)  # 16-bit PCM

    # Преобразуем в numpy массив
    samples = np.array(audio.get_array_of_samples())
    audio_array = samples.astype(np.float32) / 32768.0  # нормализация

    # 4. Обработка аудио и преобразование в тензор
    input_features = processor(audio_array, sampling_rate=16000, return_tensors="pt").input_features
    input_features = input_features.to(device)

    # 5. Расшифровка
    predicted_ids = model.generate(input_features)

    # 6. Декодирование в текст
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

    # Удаляем файл
    os.remove(voice_file)

    return transcription


def answer_analyze(user_answer: str) -> str:
    """
    Обработка ответа пользователя
    Сейчас функция-заглушка
    """
    return "Вы абсолютно правы"
