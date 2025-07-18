from pathlib import Path

from check import Auth
import telebot, types

from message_transcription import message_transcription
from qadatabse import QADatabase

qa_db = QADatabase()
auth = Auth()

def get_token():
    dir = Path(__file__).parent
    filepath = dir / "token"

    token = filepath.read_text()

    return token

token = get_token()
bot = telebot.TeleBot(token)

# Обработчик голосовых сообщений
# @bot.message_handler(content_types=['voice'])
def handle_voice(message):
    voice_file = "voice.ogg"

    # Получаем информацию о голосовом сообщении
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Сохраняем файл локально
    with open(voice_file, 'wb') as f:
        f.write(downloaded_file)

    result = message_transcription(voice_file)
    bot.reply_to(message, f"Вы ответили {result}")
    bot.reply_to(message, result)

@bot.message_handler(commands=['start'])
def send_question(message):
    
    username = message.json["from"]["username"]
    print(username)
    
    if not auth.is_user_authorized(username):
        return 

    question, reference_answer = qa_db.get_random_answer()
    bot.reply_to(message, question)
    bot.register_next_step_handler(message, handle_voice)


bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
