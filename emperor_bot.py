import telebot
import time
import ephem
from datetime import datetime, timedelta

BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
bot = telebot.TeleBot(BOT_TOKEN)

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
            bot.reply_to(message, "🔮 Я — Хорарный Император! Задай вопрос!")
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
        
        response = f"""
🔮 ХОРАРНЫЙ АНАЛИЗ
⏰ {display_time}, МОСКВА

❓ ВОПРОС: {message.text}

📊 КАРТА:
• 🌙 Луна: {moon_sign}
• ☀️ Солнце: {sun_sign}

⚡ ВЕРДИКТ: ДА ✅
📖 Луна в {moon_sign} благоприятствует

💫 Действуйте уверенно!
"""
        bot.reply_to(message, response)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

print("🔄 Бот запущен...")
while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
