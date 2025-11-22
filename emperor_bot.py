import telebot
import time
import ephem
from datetime import datetime

BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
bot = telebot.TeleBot(BOT_TOKEN)

# МОДУЛЬ 1: БАЗОВЫЕ ФУНКЦИИ
def get_russian_zodiac(eng_sign):
    zodiac_map = {
        'Aries': 'Овен', 'Taurus': 'Телец', 'Gemini': 'Близнецы',
        'Cancer': 'Рак', 'Leo': 'Лев', 'Virgo': 'Дева',
        'Libra': 'Весы', 'Scorpio': 'Скорпион', 'Sagittarius': 'Стрелец',
        'Capricorn': 'Козерог', 'Aquarius': 'Водолей', 'Pisces': 'Рыбы'
    }
    return zodiac_map.get(eng_sign, eng_sign)

def get_planet_ruler(zodiac_sign):
    rulers = {
        'Овен': 'Марс', 'Телец': 'Венера', 'Близнецы': 'Меркурий',
        'Рак': 'Луна', 'Лев': 'Солнце', 'Дева': 'Меркурий',
        'Весы': 'Венера', 'Скорпион': 'Плутон', 'Стрелец': 'Юпитер',
        'Козерог': 'Сатурн', 'Водолей': 'Уран', 'Рыбы': 'Нептун'
    }
    return rulers.get(zodiac_sign, 'Венера')

# МОДУЛЬ 2: ОПРЕДЕЛЕНИЕ ТИПА ВОПРОСА
def detect_question_type(question):
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['деньг', 'финанс', 'денег']):
        return 'finance', 2, 'Венера'
    elif any(word in question_lower for word in ['любит', 'скуч', 'отношен']):
        return 'relationship', 7, 'Венера'
    elif any(word in question_lower for word in ['работ', 'карьер']):
        return 'career', 10, 'Сатурн'
    else:
        return 'general', 1, 'Солнце'

# МОДУЛЬ 3: ПРОСТОЙ АНАЛИЗ (пока без сложной логики)
def simple_analysis(question_text):
    try:
        real_time = datetime.now()
        display_time = real_time.strftime('%H:%M, %d.%m.%Y')
        
        observer = ephem.Observer()
        observer.lat = '55.7558'
        observer.lon = '37.6173'  
        observer.date = real_time
        
        # Расчет планет
        planets = {
            'Луна': ephem.Moon(),
            'Солнце': ephem.Sun(),
            'Меркурий': ephem.Mercury(),
            'Венера': ephem.Venus(),
            'Марс': ephem.Mars(),
            'Юпитер': ephem.Jupiter()
        }
        
        for name, planet in planets.items():
            planet.compute(observer)
        
        # Знаки и управители
        moon_sign = get_russian_zodiac(ephem.constellation(planets['Луна'])[1])
        sun_sign = get_russian_zodiac(ephem.constellation(planets['Солнце'])[1])
        venus_sign = get_russian_zodiac(ephem.constellation(planets['Венера'])[1])
        
        moon_ruler = get_planet_ruler(moon_sign)
        sun_ruler = get_planet_ruler(sun_sign)
        venus_ruler = get_planet_ruler(venus_sign)
        
        # Простой вердикт
        question_type, house, significator = detect_question_type(question_text)
        
        if moon_sign in ['Телец', 'Рак', 'Весы', 'Стрелец']:
            verdict = "ДА ✅"
            reason = f"Луна в {moon_sign} создает благоприятные условия"
        else:
            verdict = "НЕТ ❌"
            reason = f"Луна в {moon_sign} указывает на препятствия"
        
        analysis = f"""
🔮 ХОРАРНЫЙ АНАЛИЗ
⏰ {display_time}, МОСКВА

❓ ВОПРОС: {question_text}

📊 КАРТА:
• 🌙 Луна: {moon_sign} (упр. {moon_ruler})
• ☀️ Солнце: {sun_sign} (упр. {sun_ruler})
• ♀️ Венера: {venus_sign} (упр. {venus_ruler})

⚡ ВЕРДИКТ: {verdict}
📖 ОБОСНОВАНИЕ: {reason}

💫 СТРАТЕГИЯ: {"Действуйте уверенно" if "ДА" in verdict else "Проявите терпение"}
"""
        return analysis
        
    except Exception as e:
        return f"❌ Ошибка: {str(e)}"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('/'):
        if message.text == '/start':
            bot.reply_to(message, "🔮 Я — Хорарный Император. Задай вопрос!")
        return
    
    analysis = simple_analysis(message.text)
    bot.reply_to(message, analysis)

print("🔄 Базовый каркас запущен...")
while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
