from flask import Flask, request
import requests
import telebot
import os

app = Flask(__name__)

# ЦИФРОВАЯ ДНК ТВОЕГО ИМПЕРАТОРА
BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
ASTRO_SERVER = "https://horary-killer-bot.onrender.com"

bot = telebot.TeleBot(BOT_TOKEN)

def get_astrological_verdict():
    """Получает вердикт от астрологического ядра"""
    try:
        response = requests.get(ASTRO_SERVER)
        if "Вердикт: ДА" in response.text:
            return "ДА ✅"
        elif "Вердикт: НЕТ" in response.text:
            return "НЕТ ❌"
        return "НЕОПРЕДЕЛЕНО ⚡"
    except:
        return "ОШИБКА СИСТЕМЫ"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обрабатывает все сообщения"""
    verdict = get_astrological_verdict()
    response = f"""🔮 ХОРАРНЫЙ ИМПЕРАТОР

Вопрос: {message.text}
Вердикт: {verdict}

Сила звёзд с тобой, Владычица."""
    
    bot.reply_to(message, response)

# Вебхук для Render
@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        json_str = request.get_data().decode("UTF-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
    return "БОТ-ИМПЕРАТОР АКТИВЕН"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
