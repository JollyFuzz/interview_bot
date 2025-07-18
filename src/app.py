import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from pydub import AudioSegment
from transformers import AutoModelForCausalLM, AutoTokenizer

import numpy as np

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

def voice_transcription(voice_path):
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

#TODO: переименовать
def inference(text):
    # Загрузка модели и токенизатора
    model_name = "Vikhrmodels/QVikhr-3-1.7B-Instruction-noreasoning"
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    inputs = tokenizer(text, return_tensors="pt").to(device)

    # Generate
    generate_ids = model.generate(inputs.input_ids, max_length=30)
    result = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

    return result


def run(voice_path):
    text = voice_transcription(voice_path)
    print(f"Вы наговорили: {text}")
    result = inference(text)
    print(f"Результат работы модели {result}")

    return result



run("sound.ogg")