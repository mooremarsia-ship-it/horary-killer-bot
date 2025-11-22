import telebot
import time
import ephem
from datetime import datetime
import math

BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
bot = telebot.TeleBot(BOT_TOKEN)

def get_russian_zodiac(eng_sign):
    zodiac_map = {
        'Aries': 'Овен', 'Taurus': 'Телец', 'Gemini': 'Близнецы',
        'Cancer': 'Рак', 'Leo': 'Лев', 'Virgo': 'Дева',
        'Libra': 'Весы', 'Scorpio': 'Скорпион', 'Sagittarius': 'Стрелец',
        'Capricorn': 'Козерог', 'Aquarius': 'Водолей', 'Pisces': 'Рыбы'
    }
    return zodiac_map.get(eng_sign, eng_sign)

def get_planet_ruler(sign):
    rulers = {
        'Aries': 'Марс', 'Taurus': 'Венера', 'Gemini': 'Меркурий',
        'Cancer': 'Луна', 'Leo': 'Солнце', 'Virgo': 'Меркурий',
        'Libra': 'Венера', 'Scorpio': 'Плутон', 'Sagittarius': 'Юпитер',
        'Capricorn': 'Сатурн', 'Aquarius': 'Уран', 'Pisces': 'Нептун'
    }
    return rulers.get(sign, sign)  # Если знак не найден, возвращаем сам знак

def get_horary_analysis(question_text):
    """Чистый и простой хорарный анализ"""
    try:
        current_time = datetime.now()
        
        observer = ephem.Observer()
        observer.lat = '55.7558'
        observer.lon = '37.6173'
        observer.date = current_time
        
        # Только основные планеты
        planets = {
            'Луна': ephem.Moon(),
            'Солнце': ephem.Sun(),
            'Меркурий': ephem.Mercury(),
            'Венера': ephem.Venus(),
            'Марс': ephem.Mars()
        }
        
        # Вычисляем позиции
        for planet in planets.values():
            planet.compute(observer)
        
        # Получаем знаки на русском
        moon_sign = get_russian_zodiac(ephem.constellation(planets['Луна'])[1])
        sun_sign = get_russian_zodiac(ephem.constellation(planets['Солнце'])[1])
        mars_sign = get_russian_zodiac(ephem.constellation(planets['Марс'])[1])
        venus_sign = get_russian_zodiac(ephem.constellation(planets['Венера'])[1])
        
        # Управители
        moon_ruler = get_planet_ruler(moon_sign)
        sun_ruler = get_planet_ruler(sun_sign)
        
        # Простой вердикт
        if moon_sign in ['Телец', 'Рак', 'Весы', 'Стрелец']:
            verdict = "ДА ✅"
            reason = f"Луна в {moon_sign} создает благоприятные условия"
        else:
            verdict = "НЕТ ❌"
            reason = f"Луна в {moon_sign} указывает на препятствия"
        
        analysis = f"""
🔮 ХОРАРНЫЙ АНАЛИЗ
⏰ {current_time.strftime('%H:%M, %d.%m.%Y')}, МОСКВА

❓ ВОПРОС: {question_text}

📊 КАРТА:
• 🌙 Луна: {moon_sign} (упр. {moon_ruler})
• ☀️ Солнце: {sun_sign} (упр. {sun_ruler}) 
• ♂️ Марс: {mars_sign}
• ♀️ Венера: {venus_sign}

⚡ ВЕРДИКТ: {verdict}
📖 ОБОСНОВАНИЕ: {reason}

💫 РЕКОМЕНДАЦИЯ: {"Действуй уверенно - звезды благоволят" if "ДА" in verdict else "Прояви терпение - сейчас не лучшее время"}
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
    
    analysis = get_horary_analysis(message.text)
    bot.reply_to(message, analysis)

print("🔄 Чистый бот запущен...")
while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
