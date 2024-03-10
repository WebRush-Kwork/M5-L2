import telebot
import os
from config import *
from logic import *
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def info(message):
    bot.send_message(
        message.chat.id, 'Привет! Я бот для генерации изображений! Напиши свой запрос в чат и ожидай фото! 🥰')


def delete_message(chat_id, message_id, delay):
    time.sleep(delay)
    bot.delete_message(chat_id, message_id)


@bot.message_handler(func=lambda message: True)
def start(message):
    greeting_message = bot.reply_to(message, 'Генерирую картинку...')
    greeting_message_id = greeting_message.message_id
    delete_message(message.chat.id, greeting_message_id, 30)
    bot.send_chat_action(message.chat.id, 'typing')
    prompt = message.text
    user_id = message.from_user.id
    path = f'images/{user_id}.png'

    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    images = api.check_generation(uuid)[0]
    api.converter_base64(images, path)

    with open(path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

    if os.path.isfile(path):
        os.remove(path)


bot.infinity_polling()
