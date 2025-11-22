import requests
import telebot
import time

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
    except Exception as e:
        return f"ОШИБКА СИСТЕМЫ: {str(e)}"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обрабатывает все сообщения"""
    print(f"Получено сообщение: {message.text}")  # Логируем
    
    verdict = get_astrological_verdict()
    response = f"""🔮 ХОРАРНЫЙ ИМПЕРАТОР

Вопрос: {message.text}
Вердикт: {verdict}

Сила звёзд с тобой, Владычица."""
    
    bot.reply_to(message, response)
    print("Ответ отправлен!")  # Логируем

print("🔮 Бот-Император запускается...")
print("Ожидаю сообщения...")

# Бесконечный цикл опроса
while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
