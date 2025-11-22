import requests
import telebot
import time
import ephem
from datetime import datetime
from horary_knowledge import detect_question_theme, get_planet_ruler

# ЦИФРОВАЯ ДНК ТВОЕГО ИМПЕРАТОРА
BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
ASTRO_SERVER = "https://horary-killer-bot.onrender.com"

bot = telebot.TeleBot(BOT_TOKEN)

def get_horary_analysis(question_text):
    """Проводит хорарный анализ вопроса"""
    try:
        # Фиксируем время вопроса
        question_time = datetime.now()
        
        # Определяем тему вопроса
        question_house, house_meaning = detect_question_theme(question_text)
        
        # Строим карту
        observer = ephem.Observer()
        observer.lat = '55.7558'
        observer.lon = '37.6173'  
        observer.date = question_time
        
        # Расчет ключевых планет
        moon = ephem.Moon()
        sun = ephem.Sun()
        
        moon.compute(observer)
        sun.compute(observer)
        
        moon_sign = ephem.constellation(moon)[1]
        sun_sign = ephem.constellation(sun)[1]
        
        moon_ruler = get_planet_ruler(moon_sign)
        sun_ruler = get_planet_ruler(sun_sign)
        
        # Простой анализ аспектов (заглушка)
        aspect_found = moon_sign in ['Taurus', 'Cancer', 'Libra', 'Sagittarius']
        
        # Формируем ответ
        if aspect_found:
            verdict = "ДА ✅"
            reason = f"Обнаружены гармоничные аспекты. Луна в {moon_sign} способствует успеху"
        else:
            verdict = "НЕТ ❌" 
            reason = f"Аспекты отсутствуют. Луна в {moon_sign} указывает на препятствия"
        
        # Детальный отчет
        analysis = f"""
🔮 ХОРАРНЫЙ АНАЛИЗ

❓ ВОПРОС: {question_text}
⏰ ВРЕМЯ: {question_time.strftime('%d.%m.%Y %H:%M:%S')}

📊 КАРТА:
• 🏠 Тема: {house_meaning} 
• 🌙 Луна: {moon_sign} (упр. {moon_ruler})
• ☀️ Солнце: {sun_sign} (упр. {sun_ruler})

⚡ ВЕРДИКТ: {verdict}
📖 ОБОСНОВАНИЕ: {reason}

💡 СОВЕТ: {"Действуй уверенно - звёзды благоволят" if verdict == "ДА ✅" else "Выжди время - сейчас не лучший момент"}
"""
        return analysis
        
    except Exception as e:
        return f"❌ Ошибка расчета: {str(e)}"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обрабатывает все сообщения"""
    print(f"Получен вопрос: {message.text}")
    
    # Игнорируем команды
    if message.text.startswith('/'):
        bot.reply_to(message, "🔮 Задай свой вопрос Вселенной...")
        return
    
    # Проводим хорарный анализ
    analysis = get_horary_analysis(message.text)
    bot.reply_to(message, analysis)
    print("Анализ отправлен!")

print("🔮 Хорарный Император запущен...")
while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
