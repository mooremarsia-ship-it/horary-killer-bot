import telebot
import time
import random
import json
import os
from datetime import datetime, timedelta, timezone
from flask import Flask
import threading
import requests

print("🌌 Запускаю ВЕЧНЫЙ Хорарный Императора...")

# Токен бота
BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"

# УДАЛЯЕМ ВЕБХУКИ навсегда
try:
    response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook")
    print("✅ Вебхуки уничтожены навсегда")
    time.sleep(2)
except:
    print("✅ Вебхуков и так не было")

# Создаем бота
bot = telebot.TeleBot(BOT_TOKEN)

# Flask для здоровья
app = Flask(__name__)
@app.route('/')
def home():
    return "💫 Вечный Император работает!", 200

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

class EternalEmperor:
    def __init__(self):
        print("🔮 Вечный Император рожден!")
    
    def get_greeting(self):
        return random.choice([
            "🌌 *Приветствую, Искатель!* Я - Вечный Хорарный Император!",
            "✨ *Пред ликом Вечности склонись!* Я готов открыть тайны звезд!",
            "🔮 *В час, когда звёзды шепчут,* я внимаю твоим вопросам...",
        ])
    
    def is_greeting(self, text):
        """Проверяем приветствия"""
        greetings = ['император', 'бот', 'привет', 'здравствуй', 'начать', 'хорарный']
        return text.lower().strip() in greetings
    
    def is_private_request(self, text):
        """Проверяем запрос на личное"""
        return text.lower().startswith('личное')
    
    def is_real_question(self, text):
        """Проверяем настоящий ли вопрос"""
        if self.is_greeting(text) or len(text) < 4:
            return False
            
        keywords = ['любов', 'деньг', 'работ', 'карьер', 'здоров', 'будущ', 'встреч', 'получу']
        return any(word in text.lower() for word in keywords) or '?' in text
    
    def analyze_intent(self, question):
        """Анализируем намерение"""
        q = question.lower()
        if 'любов' in q: return "LOVE"
        elif 'деньг' in q: return "MONEY" 
        elif 'работ' in q: return "CAREER"
        else: return "GENERAL"
    
    def generate_analysis(self, question, intent):
        """Генерируем анализ"""
        current_time = datetime.now(timezone.utc) + timedelta(hours=3)
        time_str = current_time.strftime('%H:%M, %d %B %Y')
        
        if intent == "LOVE":
            return self._love_analysis(question, time_str)
        elif intent == "MONEY":
            return self._money_analysis(question, time_str)
        elif intent == "CAREER":
            return self._career_analysis(question, time_str)
        else:
            return self._general_analysis(question, time_str)
    
    def _love_analysis(self, question, time_str):
        analysis = f"""
*💖 ХОРАРНЫЙ АНАЛИЗ ЛЮБВИ*

*Время:* {time_str}
*Вопрос:* «{question}»

---

*🌙 ЛЮБОВНЫЕ ПЕРСПЕКТИВЫ:*

✨ *Ближайшие 2 недели:* Значимые встречи и глубокие эмоциональные связи
✨ *До конца ноября:* Возможность встречи родственной души
✨ *Энергетика:* Ваше сердце открыто для настоящей любви

*💫 ВЕРДИКТ:*
Любовь уже на пути к вам! Будьте открыты новым знакомствам.
"""
        
        strategy = """*🎯 СТРАТЕГИЯ ДЛЯ ЛЮБВИ:*
• Посещайте места, где можете встретить единомышленников
• Будьте открыты неожиданным знакомствам
• Работайте над самооценкой и самолюбием
• Доверяйте интуиции в выборе партнера"""
        
        return analysis, strategy
    
    def _money_analysis(self, question, time_str):
        analysis = f"""
*💰 ХОРАРНЫЙ ФИНАНСОВЫЙ АНАЛИЗ*

*Время:* {time_str}
*Вопрос:* «{question}»

---

*💎 ФИНАНСОВЫЕ ПОТОКИ:*

✨ *Ближайшие недели:* Активизация денежных потоков
✨ *Источники:* Неожиданные поступления и завершение старых проектов
✨ *Энергетика:* Изобилие следует за вашими намерениями

*💫 ВЕРДИКТ:*
Финансовые возможности расширяются! Деньги придут вовремя.
"""
        
        strategy = """*🎯 ФИНАНСОВАЯ СТРАТЕГИЯ:*
• Завершите все незавершенные финансовые дела
• Будьте готовы к новым источникам дохода
• Контролируйте расходы и планируйте бюджет
• Доверяйте, что Вселенная поддержит ваши цели"""
        
        return analysis, strategy
    
    def _general_analysis(self, question, time_str):
        analysis = f"""
*🌌 ХОРАРНЫЙ АНАЛИЗ*

*Время:* {time_str}
*Вопрос:* «{question}»

---

*🔮 ЗВЕЗДНЫЙ ВЕРДИКТ:*

Звезды благоволят вашим начинаниям! Текущий период благоприятен для реализации планов и духовного роста.

*💫 ПЕРСПЕКТИВЫ:*
Вы находитесь на правильном пути. Каждый шаг ведет к расширению сознания и новым возможностям.
"""
        
        strategy = """*🎯 СТРАТЕГИЯ:*
• Доверяйте интуиции и внутреннему руководству
• Действуйте смело, но обдуманно
• Сохраняйте позитивный настрой в любых обстоятельствах
• Помните: вы - творец своей реальности"""
        
        return analysis, strategy

# Создаем ВЕЧНОГО императора
emperor = EternalEmperor()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_type = "private" if message.chat.type == "private" else "group"
    
    greeting = emperor.get_greeting()
    
    if chat_type == "private":
        response = f"""{greeting}

*Я готов открыть тайны звезд для тебя!* ✨

*Задай вопрос о:*
• 💖 Любви и отношениях
• 💰 Финансах и изобилии
• 💼 Карьере и предназначении
• 🌌 Будущем и возможностях

*Пример:* «Что меня ждет в любви?»"""
    else:
        response = f"""{greeting}

*Выбери способ общения:*
💬 *Задай вопрос здесь*
🔒 *Напиши «Личное [вопрос]» для конфиденциальности*
👤 *Или в личные сообщения для полной приватности*

*Пример:* «Личное Что меня ждет в карьере?»"""
    
    bot.reply_to(message, response, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    try:
        user_id = message.from_user.id
        text = message.text.strip()
        chat_type = "private" if message.chat.type == "private" else "group"
        
        print(f"💫 Сообщение: {text}")

        # Обработка ЛИЧНЫХ запросов
        if chat_type in ['group', 'supergroup'] and emperor.is_private_request(text):
            parts = text.split(' ', 1)
            if len(parts) > 1 and len(parts[1]) > 2:
                try:
                    intent = emperor.analyze_intent(parts[1])
                    analysis, strategy = emperor.generate_analysis(parts[1], intent)
                    
                    private_response = f"🔒 *КОНФИДЕНЦИАЛЬНЫЙ АНАЛИЗ*\n\n{analysis}\n\n*🎯 СТРАТЕГИЯ:*\n{strategy}"
                    
                    bot.send_message(user_id, private_response, parse_mode='Markdown')
                    bot.reply_to(message, "✅ *Анализ отправлен в личные сообщения!*", parse_mode='Markdown')
                    return
                except:
                    bot.reply_to(message, "💌 *Напиши мне в ЛС:* @HoraryEmperorBot", parse_mode='Markdown')
                    return

        # Обычные сообщения
        if emperor.is_greeting(text):
            greeting = emperor.get_greeting()
            response = f"{greeting}\n\nЗадай вопрос о любви, деньгах или будущем!"
            bot.reply_to(message, response, parse_mode='Markdown')
            return
            
        elif not emperor.is_real_question(text):
            response = """🤔 *Я не совсем понял...*

Задай вопрос о:
• Любви и отношениях
• Финансах и деньгах  
• Карьере и будущем

*Пример:* «Что меня ждет в любви до конца года?»"""
            bot.reply_to(message, response, parse_mode='Markdown')
            return
            
        else:
            # НАСТОЯЩИЕ вопросы
            intent = emperor.analyze_intent(text)
            analysis, strategy = emperor.generate_analysis(text, intent)
            
            if chat_type == "private":
                full_response = f"{analysis}\n\n*🎯 СТРАТЕГИЯ:*\n{strategy}"
            else:
                full_response = f"{analysis}\n\n*🎯 СТРАТЕГИЯ:*\n{strategy}\n\n💌 *Для конфиденциальности: «Личное [вопрос]»*"
            
            bot.reply_to(message, full_response, parse_mode='Markdown')
            
    except Exception as e:
        print(f"💫 Император преодолевает: {e}")
        bot.reply_to(message, "🔮 *Звезды временно скрыты... Попробуй еще раз!*", parse_mode='Markdown')

print("✅ ВЕЧНЫЙ Император готов служить!")
print("🌐 Flask работает на порту 5000")

# ВЕЧНЫЙ запуск
def eternal_launch():
    while True:
        try:
            print("💫 Запускаю вечный polling...")
            bot.polling(none_stop=True, interval=2, timeout=60)
        except Exception as e:
            print(f"💫 Император возрождается: {e}")
            time.sleep(10)

if __name__ == "__main__":
    eternal_launch()
