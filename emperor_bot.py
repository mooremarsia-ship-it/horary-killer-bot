import telebot
import time
import random
import json
import os
from datetime import datetime, timedelta, timezone
from flask import Flask
import threading
import requests
import subprocess
import sys

print("🌌 Запускаю РАДИКАЛЬНОГО Хорарного Императора...")

# СИЛЬНОЕ ОЧИЩЕНИЕ ПЕРЕД ЗАПУСКОМ
def kill_previous_instances():
    """Убиваем все предыдущие процессы бота"""
    try:
        # Получаем список процессов Python
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        # Ищем процессы нашего бота
        for line in lines:
            if 'python' in line and 'horary' in line.lower():
                parts = line.split()
                if len(parts) > 1:
                    pid = parts[1]
                    print(f"🔫 Убиваем процесс {pid}")
                    subprocess.run(['kill', '-9', pid])
        
        time.sleep(3)
        print("✅ Все предыдущие процессы уничтожены")
    except Exception as e:
        print(f"⚠️ Ошибка очистки процессов: {e}")

# ВЫПОЛНЯЕМ ОЧИСТКУ
kill_previous_instances()

# ЖЕСТКОЕ удаление вебхуков
def hard_webhook_cleanup():
    """Жесткое удаление всех вебхуков"""
    BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
    
    for _ in range(3):  # Пробуем несколько раз
        try:
            response = requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook",
                timeout=10
            )
            if response.status_code == 200:
                print("✅ Вебхуки полностью удалены")
                break
        except Exception as e:
            print(f"⚠️ Ошибка удаления вебхуков: {e}")
        time.sleep(2)

hard_webhook_cleanup()

# ТОЛЬКО ПОСЛЕ ОЧИСТКИ создаем бота
BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
bot = telebot.TeleBot(BOT_TOKEN)

# Простой Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "🔄 Радикальный Император работает!", 200

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

class RadicalHoraryEmperor:
    def __init__(self):
        print("🔮 Инициализирую радикального Императора...")
    
    def get_greeting(self):
        return "🌌 *Я - Радикальный Хорарный Император!* Задай вопрос!"
    
    def generate_analysis(self, question):
        """Быстрый и умный анализ"""
        current_time = datetime.now(timezone.utc) + timedelta(hours=3)
        time_str = current_time.strftime('%H:%M, %d %B %Y')
        
        analysis = f"""
*🔮 ХОРАРНЫЙ АНАЛИЗ*

*Время:* {time_str}
*Вопрос:* «{question}»

*💫 ЗВЕЗДНЫЙ ВЕРДИКТ:*
Звезды благоволят твоим начинаниям! Текущий период благоприятен для реализации планов.

*🌟 КЛЮЧЕВЫЕ АСПЕКТЫ:*
• Луна растущая - время начинаний
• Венера в гармонии - успех в отношениях  
• Юпитер расширяет возможности
"""
        
        strategy = """*🎯 СТРАТЕГИЯ:*
• Доверяй интуиции
• Действуй смело
• Будь открыт новому"""
        
        return analysis, strategy

emperor = RadicalHoraryEmperor()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    response = f"""{emperor.get_greeting()}

*Выбери способ:*
💬 Задай вопрос здесь
🔒 Напиши «Личное [вопрос]» для ЛС
👤 Или в личные сообщения

*Пример:* «Что меня ждет в любви?»"""
    
    bot.reply_to(message, response, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user_id = message.from_user.id
        text = message.text.strip()
        chat_type = "private" if message.chat.type == "private" else "group"
        
        print(f"📨 Сообщение: {text}")

        # Обработка личных запросов
        if chat_type in ['group', 'supergroup'] and text.lower().startswith('личное'):
            parts = text.split(' ', 1)
            if len(parts) > 1 and len(parts[1]) > 2:
                try:
                    analysis, strategy = emperor.generate_analysis(parts[1])
                    private_response = f"🔒 *КОНФИДЕНЦИАЛЬНЫЙ АНАЛИЗ*\n\n{analysis}\n\n*🎯 СТРАТЕГИЯ:*\n{strategy}"
                    
                    bot.send_message(user_id, private_response, parse_mode='Markdown')
                    bot.reply_to(message, "✅ *Анализ отправлен в ЛС!*", parse_mode='Markdown')
                    return
                except Exception as e:
                    bot.reply_to(message, "💌 *Напиши мне в ЛС:* @HoraryEmperorBot", parse_mode='Markdown')
                    return

        # Обычные вопросы
        if text.lower() in ['привет', 'начать']:
            bot.reply_to(message, f"{emperor.get_greeting()}\n\nЗадай вопрос!", parse_mode='Markdown')
            return

        analysis, strategy = emperor.generate_analysis(text)
        
        if chat_type == "private":
            full_response = f"{analysis}\n\n*🎯 СТРАТЕГИЯ:*\n{strategy}"
        else:
            full_response = f"{analysis}\n\n*🎯 СТРАТЕГИЯ:*\n{strategy}\n\n💌 *Для конфиденциальности: «Личное [вопрос]»*"
        
        bot.reply_to(message, full_response, parse_mode='Markdown')
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        bot.reply_to(message, "🔮 *Попробуй еще раз...*", parse_mode='Markdown')

print("✅ Радикальный Император готов!")
print("🌐 Flask работает на порту 5000")

# СУПЕР-УСТОЙЧИВЫЙ ЗАПУСК
def super_stable_launch():
    max_attempts = 5
    attempt = 0
    
    while attempt < max_attempts:
        try:
            attempt += 1
            print(f"🚀 Попытка запуска {attempt}/{max_attempts}...")
            
            # ОЧИСТКА перед каждой попыткой
            hard_webhook_cleanup()
            
            # ЗАПУСК с коротким таймаутом
            bot.polling(
                none_stop=False,  # НЕ none_stop!
                interval=3,
                timeout=30,
                long_polling_timeout=20
            )
            
        except telebot.apihelper.ApiTelegramException as e:
            if "Conflict" in str(e):
                print(f"⚡ Конфликт обнаружен! Убиваем процессы...")
                kill_previous_instances()
                time.sleep(5)
            else:
                print(f"❌ API ошибка: {e}")
                
        except Exception as e:
            print(f"❌ Общая ошибка: {e}")
            
        # Увеличиваем паузу между попытками
        wait_time = attempt * 10
        print(f"💤 Ожидание {wait_time} секунд перед перезапуском...")
        time.sleep(wait_time)
    
    print("💀 Все попытки исчерпаны! Завершаем работу.")
    sys.exit(1)

if __name__ == "__main__":
    super_stable_launch()
