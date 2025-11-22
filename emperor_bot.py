import telebot
import time
import ephem
from datetime import datetime

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

def get_planet_ruler(zodiac_sign):
    rulers = {
        'Овен': 'Марс', 'Телец': 'Венера', 'Близнецы': 'Меркурий',
        'Рак': 'Луна', 'Лев': 'Солнце', 'Дева': 'Меркурий',
        'Весы': 'Венера', 'Скорпион': 'Плутон', 'Стрелец': 'Юпитер',
        'Козерог': 'Сатурн', 'Водолей': 'Уран', 'Рыбы': 'Нептун'
    }
    return rulers.get(zodiac_sign, 'Венера')

def detect_question_type(question):
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['деньг', 'финанс', 'денег', 'придут', 'получу']):
        return 'finance', 2, 'Венера'
    elif any(word in question_lower for word in ['любит', 'скуч', 'отношен', 'чувств', 'любов']):
        return 'relationship', 7, 'Венера'
    elif any(word in question_lower for word in ['работ', 'карьер', 'бизнес', 'проект']):
        return 'career', 10, 'Сатурн'
    elif any(word in question_lower for word in ['здоров', 'болез', 'самочувств']):
        return 'health', 6, 'Марс'
    else:
        return 'general', 1, 'Солнце'

def get_detailed_analysis(question_text):
    try:
        # РЕАЛЬНОЕ время для показа
        real_time = datetime.now()
        display_time = real_time.strftime('%H:%M, %d.%m.%Y')
        
        # Настройка наблюдателя БЕЗ указания времени - ephem сам возьмет текущее
        observer = ephem.Observer()
        observer.lat = '55.7558'
        observer.lon = '37.6173'
        # НЕ указываем observer.date - будет использовано текущее время системы
        
        # Расчет всех планет
        planets = {
            'Луна': ephem.Moon(),
            'Солнце': ephem.Sun(),
            'Меркурий': ephem.Mercury(),
            'Венера': ephem.Venus(),
            'Марс': ephem.Mars(),
            'Юпитер': ephem.Jupiter(),
            'Сатурн': ephem.Saturn()
        }
        
        for name, planet in planets.items():
            planet.compute(observer)
        
        # Получаем знаки на русском
        moon_sign = get_russian_zodiac(ephem.constellation(planets['Луна'])[1])
        sun_sign = get_russian_zodiac(ephem.constellation(planets['Солнце'])[1])
        venus_sign = get_russian_zodiac(ephem.constellation(planets['Венера'])[1])
        mars_sign = get_russian_zodiac(ephem.constellation(planets['Марс'])[1])
        mercury_sign = get_russian_zodiac(ephem.constellation(planets['Меркурий'])[1])
        jupiter_sign = get_russian_zodiac(ephem.constellation(planets['Юпитер'])[1])
        
        # Правильные управители
        moon_ruler = get_planet_ruler(moon_sign)
        sun_ruler = get_planet_ruler(sun_sign)
        venus_ruler = get_planet_ruler(venus_sign)
        mars_ruler = get_planet_ruler(mars_sign)
        
        # Определяем тип вопроса
        question_type, house, significator = detect_question_type(question_text)
        
        # Детальный вердикт на основе комбинаций
        favorable_signs = ['Телец', 'Рак', 'Весы', 'Стрелец', 'Рыбы']
        
        if moon_sign in favorable_signs and venus_sign in favorable_signs:
            verdict = "ДА ✅"
            reason = f"Луна в {moon_sign} и Венера в {venus_sign} создают отличные условия"
            advice = "Действуйте активно - период благоприятствует"
        elif moon_sign in favorable_signs:
            verdict = "ДА ✅" 
            reason = f"Луна в {moon_sign} способствует успешному исходу"
            advice = "Проявите инициативу - звезды поддерживают"
        else:
            verdict = "НЕТ ❌"
            reason = f"Луна в {moon_sign} указывает на временные затруднения"
            advice = "Проявите терпение - лучшее время впереди"
        
        # Генерация ответа
        analysis = f"""
🔮 ДЕТАЛЬНЫЙ ХОРАРНЫЙ АНАЛИЗ
⏰ {display_time}, МОСКВА

❓ ВОПРОС: {question_text}

📊 ДЕТАЛИ КАРТЫ:

• 🌙 Луна: {moon_sign} (упр. {moon_ruler}) - эмоциональный фон
• ☀️ Солнце: {sun_sign} (упр. {sun_ruler}) - источник воли
• ♀️ Венера: {venus_sign} (упр. {venus_ruler}) - деньги, гармония
• ♂️ Марс: {mars_sign} (упр. {mars_ruler}) - энергия действий
• ☿ Меркурий: {mercury_sign} - коммуникация
• ♃ Юпитер: {jupiter_sign} - удача, расширение

⚡ ВЕРДИКТ: {verdict}
📖 ОБОСНОВАНИЕ: {reason}

💫 РЕКОМЕНДАЦИЯ: {advice}

🌟 ТИП ВОПРОСА: {question_type} ({house}-й дом)
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
    
    analysis = get_detailed_analysis(message.text)
    bot.reply_to(message, analysis)

print("🔄 Бот с ПРАВИЛЬНЫМ временем запущен...")
while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
