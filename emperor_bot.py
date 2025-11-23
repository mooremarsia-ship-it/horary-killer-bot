import telebot
import time
import ephem
from datetime import datetime, timedelta

BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
bot = telebot.TeleBot(BOT_TOKEN)

class HoraryBrain:
    def __init__(self):
        self.experience = 0
        
    def analyze_question_type(self, question):
        question_lower = question.lower()
        if any(word in question_lower for word in ['деньг', 'финанс', 'денег']):
            return "ФИНАНСЫ", "💰"
        elif any(word in question_lower for word in ['любит', 'скуч', 'отношен']):
            return "ОТНОШЕНИЯ", "💖" 
        elif any(word in question_lower for word in ['работ', 'карьер']):
            return "КАРЬЕРА", "🚀"
        else:
            return "ОБЩИЙ", "🔮"
    
    def make_decision(self, moon_sign):
        good_signs = ['Телец', 'Рак', 'Весы', 'Стрелец']
        if moon_sign in good_signs:
            return "ДА ✅", "Звезды благоволят вашим намерениям!"
        else:
            return "НЕТ ❌", "Сейчас не лучшее время для активных действий"

bot_brain = HoraryBrain()

def get_moscow_time():
    utc_time = datetime.utcnow()
    moscow_time = utc_time + timedelta(hours=3)
    return moscow_time.strftime('%H:%M, %d.%m.%Y')

def get_russian_zodiac(eng_sign):
    zodiac_map = {
        'Aries': 'Овен', 'Taurus': 'Телец', 'Gemini': 'Близнецы',
        'Cancer': 'Рак', 'Leo': 'Лев', 'Virgo': 'Дева',
        'Libra': 'Весы', 'Scorpio': 'Скорпион', 'Sagittarius': 'Стрелец',
        'Capricorn': 'Козерог', 'Aquarius': 'Водолей', 'Pisces': 'Рыбы'
    }
    return zodiac_map.get(eng_sign, eng_sign)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('/'):
        if message.text == '/start':
            bot.reply_to(message, "🔮 Я — УМНЫЙ Хорарный Император! Задай вопрос для анализа!")
        return
    
    try:
        display_time = get_moscow_time()
        
        observer = ephem.Observer()
        observer.lat = '55.7558'
        observer.lon = '37.6173'
        
        moon = ephem.Moon()
        sun = ephem.Sun()
        moon.compute(observer)
        sun.compute(observer)
        
        moon_sign = get_russian_zodiac(ephem.constellation(moon)[1])
        sun_sign = get_russian_zodiac(ephem.constellation(sun)[1])
        
        question_type, emoji = bot_brain.analyze_question_type(message.text)
        verdict, reasoning = bot_brain.make_decision(moon_sign)
        
        response = f"""
🔮 УМНЫЙ ХОРАРНЫЙ АНАЛИЗ
⏰ {display_time}, МОСКВА

❓ ВОПРОС: {message.text}
🎯 ТИП: {question_type} {emoji}

📊 КАРТА:
• 🌙 Луна: {moon_sign}
• ☀️ Солнце: {sun_sign}

⚡ ВЕРДИКТ: {verdict}
💡 ОБОСНОВАНИЕ: {reasoning}

💫 СТРАТЕГИЯ: {"Действуйте уверенно - звёзды на вашей стороне!" if "ДА" in verdict else "Проявите терпение - лучшее время впереди!"}

🤖 Уровень анализа: {bot_brain.experience + 1}
"""
        bot.reply_to(message, response)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

print("🔄 УМНЫЙ бот с мозгами запущен...")
while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
