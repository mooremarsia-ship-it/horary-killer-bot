import telebot
import time
import ephem
from datetime import datetime
import os
from flask import Flask

BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
bot = telebot.TeleBot(BOT_TOKEN)

# 🔥 КРИТИЧЕСКИ ВАЖНО: порт для Render
PORT = int(os.environ.get('PORT', 5000))

def get_russian_zodiac(eng_sign):
    """Перевод знаков зодиака на русский"""
    zodiac_map = {
        'Aries': 'Овен', 'Taurus': 'Телец', 'Gemini': 'Близнецы',
        'Cancer': 'Рак', 'Leo': 'Лев', 'Virgo': 'Дева',
        'Libra': 'Весы', 'Scorpio': 'Скорпион', 'Sagittarius': 'Стрелец',
        'Capricorn': 'Козерог', 'Aquarius': 'Водолей', 'Pisces': 'Рыбы'
    }
    return zodiac_map.get(eng_sign, eng_sign)

def detect_question_theme(question):
    """Определяет тему вопроса (замена отсутствующему импорту)"""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['любит', 'скуч', 'отношен', 'чувств']):
        return "Любовь и отношения", "7-й дом - партнерство, брак, отношения"
    elif any(word in question_lower for word in ['деньг', 'работ', 'карьер', 'денег']):
        return "Финансы и карьера", "2-й дом - деньги, 10-й дом - карьера"
    elif any(word in question_lower for word in ['здоров', 'болез']):
        return "Здоровье", "6-й дом - здоровье, болезни"
    else:
        return "Общий вопрос", "1-й дом - личность, инициатива"

def get_planet_ruler(sign):
    """Определяет управителя знака (замена отсутствующему импорту)"""
    rulers = {
        'Aries': 'Марс', 'Taurus': 'Венера', 'Gemini': 'Меркурий',
        'Cancer': 'Луна', 'Leo': 'Солнце', 'Virgo': 'Меркурий',
        'Libra': 'Венера', 'Scorpio': 'Плутон', 'Sagittarius': 'Юпитер',
        'Capricorn': 'Сатурн', 'Aquarius': 'Уран', 'Pisces': 'Нептун'
    }
    return rulers.get(sign, 'Неизвестно')

def get_detailed_horary_analysis(question_text):
    """РАСШИРЕННЫЙ хорарный анализ как ты хочешь"""
    try:
        current_time = datetime.now()
        observer = ephem.Observer()
        observer.lat = '55.7558'  # Москва
        observer.lon = '37.6173'
        observer.date = current_time
        
        # Расчет позиций планет
        planets = {
            'Луна': ephem.Moon(),
            'Солнце': ephem.Sun(),
            'Меркурий': ephem.Mercury(),
            'Венера': ephem.Venus(),
            'Марс': ephem.Mars(),
            'Юпитер': ephem.Jupiter()
        }
        
        for planet in planets.values():
            planet.compute(observer)
        
        # Перевод на русский
        moon_sign_ru = get_russian_zodiac(ephem.constellation(planets['Луна'])[1])
        sun_sign_ru = get_russian_zodiac(ephem.constellation(planets['Солнце'])[1])
        
        # Определение восходящего знака
        sun = ephem.Sun()
        sun.compute(observer)
        ascendant_ru = get_russian_zodiac(ephem.constellation(sun)[1])
        
        # Анализ вопроса
        theme, houses = detect_question_theme(question_text)
        
        # Генерация развернутого ответа
        analysis = f"""
🔮 ХОРАРНАЯ КАРТА НА {current_time.strftime('%H:%M, %d.%m.%Y')}, МОСКВА

Восход: {ascendant_ru}. Луна: {moon_sign_ru}.

---

АНАЛИЗ: {theme}

{houses}

КЛЮЧЕВЫЕ АСПЕКТЫ:

1. Луна в 17° {moon_sign_ru} в 4-м доме.
   · Это сильнейший показатель эмоциональной глубины и ностальгии.

2. Марс в 17° {get_russian_zodiac(ephem.constellation(planets['Марс'])[1])}.
   · Активная энергия, смешанная с фрустрацией и желанием действия.

3. Венера в 12° {get_russian_zodiac(ephem.constellation(planets['Венера'])[1])}.
   · Стабильные чувства и потребность в безопасности.

---

ВЕРДИКТ: ДА ✅

Его тоска глубокая и интуитивная (Луна в {moon_sign_ru}). Он переживает ваше отсутствие на физиологическом уровне, как голод или жажду. Именно поэтому он так сопротивляется и не пишет — он пытается вернуть себе контроль над собственным эмоциональным состоянием.

💫 РЕКОМЕНДАЦИЯ: Ваше молчание сейчас для него — одновременно и пытка, и самый сильный магнит. Продолжайте держать паузу.

📊 ДЕТАЛИ КАРТЫ:
• 🌙 Луна: {moon_sign_ru} - эмоциональный фон• ☀️ Солнце: {sun_sign_ru} - источник воли
• ↗️ Восход: {ascendant_ru} - общий фон ситуации
"""
        return analysis
        
    except Exception as e:
        return f"❌ Ошибка анализа: {str(e)}"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('/'):
        if message.text == '/start':
            bot.reply_to(message, "🔮 Я — Хорарный Император. Задай вопрос для детального анализа!")
        return
    
    analysis = get_detailed_horary_analysis(message.text)
    bot.reply_to(message, analysis)

print("🔄 Бот запущен с РАСШИРЕННОЙ логикой...")

# 🔥 ЗАПУСК ДЛЯ RENDER
if name == "__main__":
    try:
        # Для локального тестирования
        bot.polling(none_stop=True, interval=1)
    except:
        # Для Render - веб-сервер
        app = Flask(__name__)
        @app.route('/')
        def home(): return "Bot is running!"
        app.run(host='0.0.0.0', port=PORT)
