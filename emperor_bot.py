import telebot
import time
import ephem
from datetime import datetime, timedelta

BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
bot = telebot.TeleBot(BOT_TOKEN)

# МОЗГ БОТА 🧠
class HoraryBrain:
    def __init__(self):
        self.experience = 0
        
    def analyze_question_type(self, question):
        question_lower = question.lower()
        if any(word in question_lower for word in ['деньг', 'финанс', 'денег']):
            return "ФИНАНСЫ", 2, "Венера"
        elif any(word in question_lower for word in ['любит', 'скуч', 'отношен']):
            return "ОТНОШЕНИЯ", 7, "Венера" 
        elif any(word in question_lower for word in ['работ', 'карьер']):
            return "КАРЬЕРА", 10, "Сатурн"
        else:
            return "ОБЩИЙ", 1, "Солнце"
    
    def make_decision(self, moon_sign, venus_sign, question_type):
        # Умная логика принятия решений
        good_signs = ['Телец', 'Рак', 'Весы', 'Стрелец']
        
        score = 0
        if moon_sign in good_signs: score += 50
        if venus_sign in good_signs: score += 30
        if question_type == "ФИНАНСЫ": score += 20
        
        if score > 70:
            return "ДА ✅", "Высокие шансы на успех! Звезды благоволят"
        elif score > 40:
            return "ВОЗМОЖНО 🤔", "Шансы есть, но нужны ваши усилия"
        else:
            return "НЕТ ❌", "Сейчас не лучшее время - проявите терпение"
    
    def generate_strategy(self, verdict, moon_sign, question_type):
        strategies = {
            "ФИНАНСЫ": {
                "ДА ✅": f"💰 При Луне в {moon_sign} - идеальное время для инвестиций и переговоров!",
                "ВОЗМОЖНО 🤔": f"💸 При Луне в {moon_sign} - действуйте осторожно, но настойчиво",
                "НЕТ ❌": f"🚫 При Луне в {moon_sign} - отложите финансовые вопросы на потом"
            },
            "ОТНОШЕНИЯ": {
                "ДА ✅": f"💖 Луна в {moon_sign} создает магию притяжения! Проявляйте чувства",
                "ВОЗМОЖНО 🤔": f"💕 При Луне в {moon_sign} - будьте терпеливы, но открыты", 
                "НЕТ ❌": f"💔 Луна в {moon_sign} - время для работы над собой"
            },
            "КАРЬЕРА": {
                "ДА ✅": f"🚀 Луна в {moon_sign} - прорыв в карьере! Смело действуйте",
                "ВОЗМОЖНО 🤔": f"📈 При Луне в {moon_sign} - постепенный рост, не торопитесь",
                "НЕТ ❌": f"📉 Луна в {moon_sign} - сосредоточьтесь на планировании"
            }
        }
        
        return strategies.get(question_type, {}).get(verdict, "🌟 Доверьтесь своей интуиции!")

# СОЗДАЕМ МОЗГ
bot_brain = HoraryBrain()

def get_moscow_time():
    """ПРАВИЛЬНОЕ московское время"""
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

def get_planet_ruler(zodiac_sign):
    rulers = {
        'Овен': 'Марс', 'Телец': 'Венера', 'Близнецы': 'Меркурий',
        'Рак': 'Луна', 'Лев': 'Солнце', 'Дева': 'Меркурий',
        'Весы': 'Венера', 'Скорпион': 'Плутон', 'Стрелец': 'Юпитер',
        'Козерог': 'Сатурн', 'Водолей': 'Уран', 'Рыбы': 'Нептун'
    }
    return rulers.get(zodiac_sign, 'Венера')

def get_zodiac_sign(planet):
    """Исправляем Ophiuchus"""
    try:
        constellation = ephem.constellation(planet)[1]
        if constellation == 'Ophiuchus':
            return 'Скорпион'  # временная замена
        return get_russian_zodiac(constellation)
    except:
        return "Не определен"

def get_detailed_analysis(question_text):
    try:
        # ПРАВИЛЬНОЕ время!
        display_time = get_moscow_time()
        
        observer = ephem.Observer()
        observer.lat = '55.7558'
        observer.lon = '37.6173'
        
        # Расчет планет
        planets = {
            'Луна': ephem.Moon(),
            'Солнце': ephem.Sun(),
            'Венера': ephem.Venus(),
            'Марс': ephem.Mars(),
            'Меркурий': ephem.Mercury(),
            'Юпитер': ephem.Jupiter()
        }
        
        for name, planet in planets.items():
            planet.compute(observer)
        
        # Знаки с исправлением Ophiuchus
        moon_sign = get_zodiac_sign(planets['Луна'])
        sun_sign = get_zodiac_sign(planets['Солнце'])
        venus_sign = get_zodiac_sign(planets['Венера'])
        mars_sign = get_zodiac_sign(planets['Марс'])
        mercury_sign = get_zodiac_sign(planets['Меркурий'])
        jupiter_sign = get_zodiac_sign(planets['Юпитер'])
        
        # Управители
        moon_ruler = get_planet_ruler(moon_sign)
        sun_ruler = get_planet_ruler(sun_sign)
        venus_ruler = get_planet_ruler(venus_sign)
        mars_ruler = get_planet_ruler(mars_sign)
        
        # ИСПОЛЬЗУЕМ МОЗГ БОТА! 🧠
        question_type, house, significator = bot_brain.analyze_question_type(question_text)
        verdict, reasoning = bot_brain.make_decision(moon_sign, venus_sign, question_type)
        strategy = bot_brain.generate_strategy(verdict, moon_sign, question_type)
        
        analysis = f"""
🔮 УМНЫЙ ХОРАРНЫЙ АНАЛИЗ
⏰ {display_time}, МОСКВА

❓ ВОПРОС: {question_text}
🎯 ТИП: {question_type} ({house}-й дом)

📊 КАРТА:
• 🌙 Луна: {moon_sign} (упр. {moon_ruler})
• ☀️ Солнце: {sun_sign} (упр. {sun_ruler}) 
• ♀️ Венера: {venus_sign} (упр. {venus_ruler})
• ♂️ Марс: {mars_sign} (упр. {mars_ruler})
• ☿ Меркурий: {mercury_sign}
• ♃ Юпитер: {jupiter_sign}

⚡ ВЕРДИКТ: {verdict}
💡 ОБОСНОВАНИЕ: {reasoning}

🎪 СТРАТЕГИЯ: {strategy}

🤖 Уровень анализа: {bot_brain.experience + 1}
"""
        return analysis
        
    except Exception as e:
        return f"❌ Ошибка анализа: {str(e)}"
# [все твои функции здесь...]

# ОБРАБОТКА ГРУПП ← НОВЫЙ КОД
@bot.message_handler(chat_types=['group', 'supergroup'])
def handle_group_message(message):
    if message.text and ('@HoraryEmperorBot' in message.text):
        question = message.text.replace('@HoraryEmperorBot', '').strip()
        if question:
            analysis = get_detailed_analysis(question)
            bot.reply_to(message, analysis)

# ЛИЧНЫЕ СООБЩЕНИЯ ← СТАРЫЙ КОД (оставить как есть)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('/'):
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('/'):
        if message.text == '/start':
            bot.reply_to(message, "🔮 Я — УМНЫЙ Хорарный Император! Задай вопрос для глубокого анализа!")
        return
    
    analysis = get_detailed_analysis(message.text)
    bot.reply_to(message, analysis)

print("🔄 УМНЫЙ бот с ПРАВИЛЬНЫМ временем запущен...")
while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
