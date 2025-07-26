import numpy as np
import torch
from pydub import AudioSegment
from transformers import WhisperForConditionalGeneration, WhisperProcessor

device = "cuda" if torch.cuda.is_available() else "cpu"


def load_audio_file(file_path):
    # Загружаем аудио с помощью pydub
    audio = AudioSegment.from_file(file_path)

    # Whisper работает с частотой дискретизации 16000 Гц
    audio = audio.set_frame_rate(16000)
    audio = audio.set_channels(1)  # моно
    audio = audio.set_sample_width(2)  # 16-bit PCM

    # Преобразуем в numpy массив
    samples = np.array(audio.get_array_of_samples())
    return samples.astype(np.float32) / 32768.0  # нормализация


def message_transcription(voice_path):
    # Загрузка модели и токенизатора
    processor = WhisperProcessor.from_pretrained("openai/whisper-medium")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium").to(device)
    model.config.forced_decoder_ids = None

    audio_array = load_audio_file(voice_path)

    # 4. Обработка аудио и преобразование в тензор
    input_features = processor(audio_array, sampling_rate=16000, return_tensors="pt").input_features
    input_features = input_features.to(device)

    # 5. Расшифровка
    predicted_ids = model.generate(input_features)

    # 6. Декодирование в текст
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

    return transcription[0]
