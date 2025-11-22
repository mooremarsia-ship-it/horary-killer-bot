import telebot
import time
import ephem
from datetime import datetime

BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
bot = telebot.TeleBot(BOT_TOKEN)

def get_russian_zodiac(eng_sign):
    """ПРОСТОЙ перевод знаков"""
    zodiac_map = {
        'Aries': 'Овен', 'Taurus': 'Телец', 'Gemini': 'Близнецы',
        'Cancer': 'Рак', 'Leo': 'Лев', 'Virgo': 'Дева',
        'Libra': 'Весы', 'Scorpio': 'Скорпион', 'Sagittarius': 'Стрелец',
        'Capricorn': 'Козерог', 'Aquarius': 'Водолей', 'Pisces': 'Рыбы'
    }
    return zodiac_map.get(eng_sign, eng_sign)

def get_detailed_analysis(question_text):
    """ЭФФЕКТИВНЫЙ анализ БЕЗ сложной логики"""
    try:
        current_time = datetime.now()
        observer = ephem.Observer()
        observer.lat = '55.7558'
        observer.lon = '37.6173'  
        observer.date = current_time
        
        # ТОЛЬКО ключевые планеты
        moon = ephem.Moon()
        sun = ephem.Sun()
        
        moon.compute(observer)
        sun.compute(observer)
        
        moon_sign = get_russian_zodiac(ephem.constellation(moon)[1])
        sun_sign = get_russian_zodiac(ephem.constellation(sun)[1])
        
        # ПРОСТАЯ логика вердикта
        good_signs = ['Телец', 'Рак', 'Весы', 'Стрелец']
        if moon_sign in good_signs:
            verdict = "ДА ✅"
            reason = f"Луна в {moon_sign} создает благоприятные условия"
            advice = "Действуй смело - звезды благоволят"
        else:
            verdict = "НЕТ ❌" 
            reason = f"Луна в {moon_sign} указывает на временные препятствия"
            advice = "Выжди время - сейчас не лучший момент"
        
        # ЧИСТЫЙ и понятный ответ
        analysis = f"""
🔮 ХОРАРНЫЙ АНАЛИЗ
⏰ {current_time.strftime('%H:%M, %d.%m.%Y')}, Москва

❓ ВОПРОС: {question_text}

📊 КАРТА:
• 🌙 Луна: {moon_sign} - эмоциональный фон
• ☀️ Солнце: {sun_sign} - источник воли

⚡ ВЕРДИКТ: {verdict}
📖 ОБОСНОВАНИЕ: {reason}

💫 РЕКОМЕНДАЦИЯ: {advice}
"""
        return analysis
        
    except Exception as e:
        # НЕ падаем, а возвращаем понятную ошибку
        return f"🔮 Император размышляет...\n(тех.ошибка: {str(e)})"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """ПРОСТАЯ обработка сообщений"""
    try:
        if message.text.startswith('/'):
            if message.text == '/start':
                bot.reply_to(message, "🔮 Я — Хорарный Император. Задай вопрос о любви, деньгах, работе...")
            return
        
        analysis = get_detailed_analysis(message.text)
        bot.reply_to(message, analysis)
        
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.reply_to(message, "🔮 Император временно недоступен...")

print("🔄 ЭФФЕКТИВНЫЙ бот запущен...")
while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        time.sleep(10)
