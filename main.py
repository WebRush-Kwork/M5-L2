import telebot
from config import *
from logic import *
bot = telebot.TeleBot(token)


@bot.message_handler(func=lambda message: True)
def start(message):
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


bot.infinity_polling()
