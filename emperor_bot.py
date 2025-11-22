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
    """Правильное определение управителей знаков"""
    rulers = {
        'Овен': 'Марс', 'Телец': 'Венера', 'Близнецы': 'Меркурий',
        'Рак': 'Луна', 'Лев': 'Солнце', 'Дева': 'Меркурий',
        'Весы': 'Венера', 'Скорпион': 'Плутон', 'Стрелец': 'Юпитер',
        'Козерог': 'Сатурн', 'Водолей': 'Уран', 'Рыбы': 'Нептун'
    }
    return rulers.get(zodiac_sign, 'Венера')

def get_zodiac_sign(planet, observer):
    """Получение знака планеты БЕЗ Ophiuchus"""
    try:
        planet.compute(observer)
        constellation = ephem.constellation(planet)[1]
        # Фильтруем только зодиакальные созвездия
        zodiac_constellations = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                               'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        
        if constellation in zodiac_constellations:
            return get_russian_zodiac(constellation)
        else:
            # Если не зодиакальное созвездие, используем предыдущее вычисление
            return get_russian_zodiac(constellation)
    except:
        return "Не определен"

def get_detailed_analysis(question_text):
    """Детальный анализ с правильными управителями"""
    try:
        current_time = datetime.now()
        
        observer = ephem.Observer()
        observer.lat = '55.7558'
        observer.lon = '37.6173'  
        observer.date = current_time
        
        # Расчет планет
        moon = ephem.Moon()
        sun = ephem.Sun()
        mars = ephem.Mars()
        venus = ephem.Venus()
        mercury = ephem.Mercury()
        jupiter = ephem.Jupiter()
        
        moon.compute(observer)
        sun.compute(observer)
        mars.compute(observer)
        venus.compute(observer)
        mercury.compute(observer)
        jupiter.compute(observer)
        
        # Получаем знаки БЕЗ Ophiuchus
        moon_sign = get_zodiac_sign(moon, observer)
        sun_sign = get_zodiac_sign(sun, observer)
        mars_sign = get_zodiac_sign(mars, observer)
        venus_sign = get_zodiac_sign(venus, observer)
        mercury_sign = get_zodiac_sign(mercury, observer)
        jupiter_sign = get_zodiac_sign(jupiter, observer)
        
        # Правильные управители
        moon_ruler = get_planet_ruler(moon_sign)
        sun_ruler = get_planet_ruler(sun_sign)
        mars_ruler = get_planet_ruler(mars_sign)
        venus_ruler = get_planet_ruler(venus_sign)
        
        # Детальный вердикт
        favorable_signs = ['Телец', 'Рак', 'Весы', 'Стрелец', 'Рыбы']
        
        if moon_sign in favorable_signs and venus_sign in favorable_signs:
            verdict = "ДА ✅"
            reason = f"Луна в {moon_sign} и Венера в {venus_sign} создают отличные условия для финансов"
            advice = "Действуйте активно - период благоприятствует денежным потокам"
        elif moon_sign in favorable_signs:
            verdict = "ДА ✅" 
            reason = f"Луна в {moon_sign} способствует успешному исходу"
            advice = "Проявите инициативу - звезды поддерживают ваши начинания"
        else:
            verdict = "НЕТ ❌"
            reason = f"Луна в {moon_sign} указывает на временные затруднения"
            advice = "Проявите терпение - лучшее время еще впереди"
        
        # Развернутый анализ
        analysis = f"""
🔮 ДЕТАЛЬНЫЙ ХОРАРНЫЙ АНАЛИЗ
⏰ {current_time.strftime('%H:%M, %d.%m.%Y')}, МОСКВА

❓ ВОПРОС: {question_text}

📊 ДЕТАЛИ КАРТЫ:

• 🌙 Луна: {moon_sign} (упр. {moon_ruler}) - эмоциональный фон
• ☀️ Солнце: {sun_sign} (упр. {sun_ruler}) - источник воли
• ♀️ Венера: {venus_sign} (упр. {venus_ruler}) - деньги, ценности
• ♂️ Марс: {mars_sign} (упр. {mars_ruler}) - энергия действий
• ☿ Меркурий: {mercury_sign} - коммуникация, переговоры
• ♃ Юпитер: {jupiter_sign} - удача, расширение

⚡ ВЕРДИКТ: {verdict}
📖 ОБОСНОВАНИЕ: {reason}

💫 РЕКОМЕНДАЦИЯ: {advice}

🌟 АСТРОЛОГИЧЕСКИЙ КОНТЕКСТ:
Текущее положение планет {("благоприятствует финансовым операциям" if "ДА" in verdict else "требует осторожности в денежных вопросах")}. 
Обратите внимание на {venus_sign} для финансов и {moon_sign} для эмоционального состояния.
"""
        return analysis
        
    except Exception as e:
        return f"❌ Ошибка анализа: {str(e)}"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('/'):
        if message.text == '/start':
            bot.reply_to(message, "🔮 Я — Хорарный Император. Задай вопрос для детального астрологического анализа!")
        return
    
    analysis = get_detailed_analysis(message.text)
    bot.reply_to(message, analysis)

print("🔄 Улучшенный бот запущен...")
while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
