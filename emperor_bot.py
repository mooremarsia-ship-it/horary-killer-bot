import telebot
import time
import ephem
from datetime import datetime, timedelta

BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
bot = telebot.TeleBot(BOT_TOKEN)

class HoraryBrain:
    def __init__(self):
        self.experience = 0
        
    def filter_absurd_questions(self, question):
        """Фильтруем абсурдные и метеорологические вопросы"""
        question_lower = question.lower()
        
        absurd_patterns = [
            'выйдет солнце', 'выйдет ли солнце', 'будет ли солнце',
            'будет дождь', 'пойдет дождь', 'будет ли дождь',
            'будет снег', 'пойдет снег', 'какая погода',
            'сколько времени', 'который час', 'какой день'
        ]
        
        for pattern in absurd_patterns:
            if pattern in question_lower:
                return "❌ Это метеорологический или бытовой вопрос! Задайте астрологический вопрос о вашей жизни, отношениях, финансах или карьере."
        
        return None
    
    def analyze_question_type(self, question):
        """Определяем тип астрологического вопроса"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['деньг', 'финанс', 'денег', 'придут', 'получу', 'заработ']):
            return "ФИНАНСЫ", "💰"
        elif any(word in question_lower for word in ['выйду замуж', 'замужество', 'брак', 'свадьб']):
            return "БРАК И ОТНОШЕНИЯ", "💍"
        elif any(word in question_lower for word in ['любит', 'скуч', 'отношен', 'чувств', 'любов', 'встреч']):
            return "ОТНОШЕНИЯ", "💖" 
        elif any(word in question_lower for word in ['работ', 'карьер', 'бизнес', 'проект', 'должност']):
            return "КАРЬЕРА", "🚀"
        elif any(word in question_lower for word in ['здоров', 'болез', 'самочувств']):
            return "ЗДОРОВЬЕ", "🏥"
        else:
            return "ОБЩИЙ", "🔮"
    
    def make_decision(self, moon_sign, venus_sign, question_type):
        """Умная система принятия решений"""
        good_signs = ['Телец', 'Рак', 'Весы', 'Стрелец']
        
        score = 0
        if moon_sign in good_signs: score += 50
        if venus_sign in good_signs: score += 30
        if question_type in ["ФИНАНСЫ", "БРАК И ОТНОШЕНИЯ"]: score += 20
        
        if score > 70:
            return "ДА ✅", "Высокие шансы на успех! Звезды благоволят вашим намерениям."
        elif score > 40:
            return "ВОЗМОЖНО 🤔", "Шансы есть, но потребуются ваши усилия и терпение."
        else:
            return "НЕТ ❌", "Сейчас не лучшее время для активных действий. Проявите терпение."
    
    def generate_strategy(self, verdict, moon_sign, question_type):
        """Генерируем умные стратегии"""
        strategies = {
            "БРАК И ОТНОШЕНИЯ": {
                "ДА ✅": f"💖 Луна в {moon_sign} благоприятствует серьезным отношениям! Это хорошее время для обсуждения брачных планов.",
                "ВОЗМОЖНО 🤔": f"💕 При Луне в {moon_sign} отношения развиваются медленно. Проявите терпение в сердечных делах.",
                "НЕТ ❌": f"💔 Сейчас не лучшее время для решения о браке. Луна в {moon_sign} советует подождать."
            },
            "ФИНАНСЫ": {
                "ДА ✅": f"💰 При Луне в {moon_sign} - отличное время для финансовых операций!",
                "ВОЗМОЖНО 🤔": f"💸 При Луне в {moon_sign} - действуйте осторожно в денежных вопросах.",
                "НЕТ ❌": f"🚫 При Луне в {moon_sign} - лучше отложить финансовые решения."
            }
        }
        return strategies.get(question_type, {}).get(verdict, "🌟 Доверьтесь своей интуиции!")

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

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('/'):
        if message.text == '/start':
            bot.reply_to(message, "🔮 Я — УМНЫЙ Хорарный Император! Задай АСТРОЛОГИЧЕСКИЙ вопрос о жизни, отношениях, финансах или карьере!")
        return
    
    try:
        # ПРОВЕРЯЕМ НА АБСУРДНЫЕ ВОПРОСЫ
        absurd_response = bot_brain.filter_absurd_questions(message.text)
        if absurd_response:
            bot.reply_to(message, absurd_response)
            return
        
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
        
        # ИСПОЛЬЗУЕМ УМНЫЙ АНАЛИЗ
        question_type, emoji = bot_brain.analyze_question_type(message.text)
        verdict, reasoning = bot_brain.make_decision(moon_sign, sun_sign, question_type)
        strategy = bot_brain.generate_strategy(verdict, moon_sign, question_type)
        
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

💫 СТРАТЕГИЯ: {strategy}

🤖 Уровень анализа: {bot_brain.experience + 1}
"""
        bot.reply_to(message, response)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

print("🔄 УМНЫЙ бот с защитой от абсурда запущен...")
while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
