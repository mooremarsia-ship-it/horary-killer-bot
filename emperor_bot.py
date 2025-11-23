import telebot
import time
import random
from datetime import datetime, timedelta, timezone
from flask import Flask
import threading
import requests

print("🌌 Запускаю Хорарного Императора с защитой от конфликтов...")

# Простой Flask для здоровья
app = Flask(__name__)
@app.route('/')
def home():
    return "🔄 Хорарный Император работает!", 200

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

# Запускаем Flask в отдельном потоке
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

# Токен бота
BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"

# ВАЖНО: Сначала удаляем все вебхуки
try:
    response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook")
    print("✅ Вебхуки удалены")
    time.sleep(2)
except Exception as e:
    print(f"ℹ️ Ошибка удаления вебхуков: {e}")

# Теперь создаем бота
bot = telebot.TeleBot(BOT_TOKEN)

class HoraryEmperor:
    def __init__(self):
        print("🔮 Император инициализирован...")
    
    def get_greeting(self):
        return random.choice([
            "🌌 *Приветствую, Искатель!* Задай свой вопрос...",
            "✨ *Пред ликом Вечности склонись!* Что желаешь узнать?",
        ])
    
    def analyze_question(self, question):
        """Анализируем тип вопроса"""
        q = question.lower()
        if any(word in q for word in ['любов', 'отношен', 'чувств', 'парн']):
            return "love"
        elif any(word in q for word in ['деньг', 'финанс', 'денег']):
            return "money" 
        elif any(word in q for word in ['работ', 'карьер']):
            return "career"
        else:
            return "general"
    
    def generate_answer(self, question, question_type):
        """Генерируем умный ответ"""
        current_time = datetime.now(timezone.utc) + timedelta(hours=3)
        time_str = current_time.strftime('%H:%M, %d %B %Y')
        
        if question_type == "love":
            return self._love_analysis(question, time_str)
        elif question_type == "money":
            return self._money_analysis(question, time_str)
        elif question_type == "career":
            return self._career_analysis(question, time_str)
        else:
            return self._general_analysis(question, time_str)
    
    def _love_analysis(self, question, time_str):
        analysis = f"""
*💖 ХОРАРНЫЙ АНАЛИЗ ЛЮБВИ*

*Время:* {time_str}
*Вопрос:* «{question}»

---

*🔮 АНАЛИЗ СИГНИФИКАТОРОВ:*

• *Луна в Тельце* - стабильность в чувствах
• *Венера в Весах* - гармония в отношениях  
• *Гармоничный аспект* между сигнификаторами

---

*💫 ВЕРДИКТ:*
*Любовные перспективы благоприятны!* 

В ближайшие 2 недели вероятны значимые встречи и развитие отношений.
"""
        
        strategy = """*🎯 СТРАТЕГИЯ:*
• Будьте открыты новым знакомствам
• Проявляйте инициативу в общении
• Работайте над доверием в отношениях"""
        
        return analysis, strategy
    
    def _money_analysis(self, question, time_str):
        analysis = f"""
*💰 ХОРАРНЫЙ ФИНАНСОВЫЙ АНАЛИЗ*

*Время:* {time_str}
*Вопрос:* «{question}»

---

*🔮 АНАЛИЗ СИГНИФИКАТОРОВ:*

• *Юпитер в Близнецах* - множественные источники дохода
• *Управитель 2-го дома* в сильном положении
• *Отсутствие напряженных аспектов*

---

*💫 ВЕРДИКТ:*
*Финансовые потоки активизируются!*

Деньги придут в течение 10-14 дней из неожиданных источников.
"""
        
        strategy = """*🎯 СТРАТЕГИЯ:*
• Будьте готовы к новым возможностям
• Диверсифицируйте доходы
• Контролируйте расходы"""
        
        return analysis, strategy
    
    def _career_analysis(self, question, time_str):
        analysis = f"""
*💼 ХОРАРНЫЙ КАРЬЕРНЫЙ АНАЛИЗ*

*Время:* {time_str}
*Вопрос:* «{question}»

---

*🔮 АНАЛИЗ СИГНИФИКАТОРОВ:*

• *Солнце в 10-м доме* - карьерный рост
• *Меркурий директный* - успех в переговорах
• *Марс в Козероге* - амбиции и решительность

---

*💫 ВЕРДИКТ:*
*Профессиональные перспективы отличные!*

Повышение или новые возможности в течение месяца.
"""
        
        strategy = """*🎯 СТРАТЕГИЯ:*
• Проявляйте инициативу на работе
• Участвуйте в важных проектах
• Сетевой с коллегами и начальством"""
        
        return analysis, strategy
    
    def _general_analysis(self, question, time_str):
        analysis = f"""
*🌌 ХОРАРНЫЙ АНАЛИЗ*

*Время:* {time_str}
*Вопрос:* «{question}»

---

*🔮 АНАЛИЗ КАРТЫ:*

• *Луна растущая* - благоприятный период для начинаний
• *Отсутствие ретроградных планет* - минимальные препятствия
• *Гармоничные аспекты* преобладают

---

*💫 ВЕРДИКТ:*
*Звезды благоволят твоим начинаниям!*

Текущий период благоприятен для реализации планов.
"""
        
        strategy = """*🎯 СТРАТЕГИЯ:*
• Доверяйте интуиции
• Действуйте смело
• Сохраняйте позитивный настрой"""
        
        return analysis, strategy

# Создаем императора
emperor = HoraryEmperor()

# Обработчики сообщений
@bot.message_handler(commands=['start', 'help', 'император'])
def send_welcome(message):
    chat_type = "private" if message.chat.type == "private" else "group"
    
    greeting = emperor.get_greeting()
    
    if chat_type == "private":
        response = f"""{greeting}

*Выбери тему:*
💖 Любовь и отношения
💰 Финансы и деньги  
💼 Карьера и работа
🌌 Общий прогноз

*Пример:* «Что меня ждет в любви?»"""
    else:
        response = f"""{greeting}

*Варианты консультации:*
💬 Задай вопрос здесь
🔒 Напиши «Личное [вопрос]» для ЛС
👤 Или в личные сообщения

*Для ЛС:* Нажми на @HoraryEmperorBot → «Написать»"""
    
    try:
        bot.reply_to(message, response, parse_mode='Markdown')
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    try:
        user_id = message.from_user.id
        text = message.text.strip()
        chat_type = "private" if message.chat.type == "private" else "group"
        
        print(f"📨 Получен вопрос: {text}")

        # Обработка личных запросов в группе
        if chat_type in ['group', 'supergroup'] and text.lower().startswith('личное'):
            parts = text.split(' ', 1)
            if len(parts) > 1 and len(parts[1]) > 2:
                try:
                    # Отправляем в ЛС
                    question_type = emperor.analyze_question(parts[1])
                    analysis, strategy = emperor.generate_answer(parts[1], question_type)
                    
                    private_response = f"🔒 *КОНФИДЕНЦИАЛЬНЫЙ АНАЛИЗ*\n\n{analysis}\n\n*🎯 СТРАТЕГИЯ:*\n{strategy}"
                    
                    bot.send_message(user_id, private_response, parse_mode='Markdown')
                    bot.reply_to(message, "✅ *Анализ отправлен в личные сообщения!*", parse_mode='Markdown')
                    return
                except Exception as e:
                    print(f"❌ Ошибка ЛС: {e}")
                    bot.reply_to(message, "💌 *Напиши мне в ЛС:* @HoraryEmperorBot", parse_mode='Markdown')
                    return
            else:
                bot.reply_to(message, "🔒 *Напиши вопрос после 'Личное'*", parse_mode='Markdown')
                return

        # Приветствия
        if text.lower() in ['привет', 'начать', 'бот']:
            greeting = emperor.get_greeting()
            response = f"{greeting}\n\nЗадай вопрос о любви, деньгах или карьере!"
            bot.reply_to(message, response, parse_mode='Markdown')
            return

        # Обычные вопросы
        time.sleep(1)  # Имитация размышления
        
        question_type = emperor.analyze_question(text)
        analysis, strategy = emperor.generate_answer(text, question_type)
        
        if chat_type == "private":
            full_response = f"{analysis}\n\n*🎯 СТРАТЕГИЯ:*\n{strategy}"
        else:
            full_response = f"{analysis}\n\n*🎯 СТРАТЕГИЯ:*\n{strategy}\n\n💌 *Для конфиденциальности: «Личное [вопрос]»*"
        
        bot.reply_to(message, full_response, parse_mode='Markdown')
        
    except Exception as e:
        print(f"❌ Ошибка обработки: {e}")
        try:
            bot.reply_to(message, "🔮 *Временные помехи... Попробуй еще раз*", parse_mode='Markdown')
        except:
            pass

print("✅ Хорарный Император готов к работе!")
print("🌐 Flask работает на порту 5000")

# ПРОСТОЙ И НАДЕЖНЫЙ ЗАПУСК
def run_bot():
    while True:
        try:
            print("🔗 Подключаемся к Telegram...")
            bot.infinity_polling(timeout=60, long_polling_timeout=30)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            print("🔄 Перезапуск через 10 секунд...")
            time.sleep(10)

if __name__ == "__main__":
    run_bot()
