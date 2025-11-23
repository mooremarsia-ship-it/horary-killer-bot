import telebot
import time
import ephem
from datetime import datetime, timedelta

BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
bot = telebot.TeleBot(BOT_TOKEN)

class RealityChecker:
    def __init__(self):
        self.absurd_patterns = {
            'время': ['сколько времени', 'который час', 'когда сейчас'],
            'погода': ['выйдет солнце', 'будет дождь', 'какая погода'],
            'магия': ['получу миллион', 'подарят квартиру', 'выиграю в лотерею'],
            'невозможное': ['сегодня замуж', 'завтра рожу', 'стану богатым за день']
        }
    
    def check_reality(self, question):
        """Проверяем вопрос на реалистичность"""
        question_lower = question.lower()
        
        # 1. ПРОВЕРКА НА РЕАЛИЗМ
        if self._check_timeframe(question_lower):
            return False, "⏰ Вопрос нарушает временные рамки. Хорар анализирует обозримое будущее, а не мгновенные чудеса."
        
        # 2. ПРОВЕРКА НА КОНКРЕТИКУ
        if not self._has_specifics(question_lower):
            return False, "🎯 Уточните вопрос: кто, что, когда, какие сроки? Без конкретики анализ невозможен."
        
        # 3. ПРОВЕРКА НА ПАССИВНОСТЬ  
        if self._is_too_passive(question_lower):
            return False, "🚫 Вопрос исходит из позиции 'мне должны'. Переформулируйте в контексте ваших действий."
        
        # 4. ПРОВЕРКА НА МАСШТАБ
        if self._violates_scale(question_lower):
            return False, "💫 Вопрос противоречит базовым жизненным процессам. Хорар - не волшебная палочка."
        
        return True, "Вопрос легитимен"
    
    def _check_timeframe(self, question):
        """Проверяет нарушение временных рамок"""
        urgent_indicators = ['сегодня', 'завтра', 'сейчас', 'немедленно', 'срочно']
        big_changes = ['замуж', 'разведусь', 'рожу', 'умру', 'стану богатым', 'получу миллион']
        
        has_urgency = any(word in question for word in urgent_indicators)
        has_big_change = any(word in question for word in big_changes)
        
        return has_urgency and has_big_change
    
    def _has_specifics(self, question):
        """Проверяет наличие конкретики"""
        specifics = ['кто', 'что', 'когда', 'какой', 'какая', 'сколько', 'где']
        has_some_specifics = any(word in question for word in specifics)
        
        # Если есть глаголы действия - тоже ок
        action_verbs = ['вернут', 'получу', 'встречу', 'устроюсь', 'куплю', 'продам']
        has_actions = any(verb in question for verb in action_verbs)
        
        return has_some_specifics or has_actions
    
    def _is_too_passive(self, question):
        """Проверяет пассивную позицию"""
        passive_patterns = [
            'подарят мне', 'достанется мне', 'упадет с неба', 
            'выиграю без', 'получу просто так', 'мне должны'
        ]
        return any(pattern in question for pattern in passive_patterns)
    
    def _violates_scale(self, question):
        """Проверяет нарушение масштаба реальности"""
        unrealistic = [
            'подарят квартиру', 'получу миллион', 'стану знаменитым',
            'встречу принца', 'найду клад', 'перееду в другую страну'
        ]
        urgent = ['сегодня', 'завтра', 'на неделе']
        
        has_unrealistic = any(word in question for word in unrealistic)
        has_urgent = any(word in question for word in urgent)
        
        return has_unrealistic and has_urgent
    
    def suggest_better_question(self, original_question):
        """Предлагает улучшенную формулировку"""
        question_lower = original_question.lower()
        
        if 'замуж' in question_lower and 'сегодня' in question_lower:
            return "Есть ли у меня потенциал выйти замуж в ближайшие 6 месяцев?"
        
        elif 'миллион' in question_lower or 'деньги' in question_lower:
            return "Вернут ли мне долг до пятницы? Или: Получу ли я премию в этом месяце?"
        
        elif 'квартир' in question_lower and 'подарят' in question_lower:
            return "Стоит ли мне ожидать помощи с жильем от семьи в этом году?"
        
        else:
            return "Сформулируйте вопрос конкретнее: с указанием людей, сроков и ваших действий."

class HoraryBrain:
    def __init__(self):
        self.experience = 0
        self.reality_checker = RealityChecker()
    
    def analyze_question_legitimacy(self, question):
        """Проверяет легитимность вопроса перед анализом"""
        is_valid, message = self.reality_checker.check_reality(question)
        
        if not is_valid:
            suggestion = self.reality_checker.suggest_better_question(question)
            full_message = f"🛡️ ДЕТЕКТОР РЕАЛЬНОСТИ\n\n{message}\n\n💡 Попробуйте так: «{suggestion}»"
            return False, full_message
        
        return True, "Вопрос принят к анализу"
    
    def analyze_question_type(self, question):
        question_lower = question.lower()
        if any(word in question_lower for word in ['деньг', 'финанс', 'денег']):
            return "ФИНАНСЫ", "💰"
        elif any(word in question_lower for word in ['любит', 'скуч', 'отношен']):
            return "ОТНОШЕНИЯ", "💖" 
        elif any(word in question_lower for word in ['работ', 'карьер']):
            return "КАРЬЕРА", "🚀"
        else:
            return "ОБЩИЙ", "🔮"
    
    def make_decision(self, moon_sign, sun_sign, question_type):
        good_signs = ['Телец', 'Рак', 'Весы', 'Стрелец']
        if moon_sign in good_signs:
            return "ДА ✅", "Звезды благоволят вашим намерениям!"
        else:
            return "НЕТ ❌", "Сейчас не лучшее время для активных действий"
    
    def generate_strategy(self, verdict, moon_sign, question_type):
        if "ДА" in verdict:
            return "Действуйте уверенно - звёзды на вашей стороне!"
        else:
            return "Проявите терпение - лучшее время впереди!"

bot_brain = HoraryBrain()

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

# ОБРАБОТКА ГРУПП ← НОВЫЙ КОД
@bot.message_handler(chat_types=['group', 'supergroup'])
def handle_group_message(message):
    if message.text and ('@HoraryEmperorBot' in message.text):
        question = message.text.replace('@HoraryEmperorBot', '').strip()
        if question:
            # ПРОВЕРЯЕМ ЛЕГИТИМНОСТЬ
            is_legitimate, legitimacy_message = bot_brain.analyze_question_legitimacy(question)
            
            if not is_legitimate:
                bot.reply_to(message, legitimacy_message)
                return
            
            # ЕСЛИ ВОПРОС ЛЕГИТИМЕН - АНАЛИЗ
            analysis = get_detailed_analysis(question)
            bot.reply_to(message, analysis)

# ЛИЧНЫЕ СООБЩЕНИЯ ← ОБНОВЛЕННЫЙ КОД
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('/'):
        if message.text == '/start':
            start_text = """
🔮 Я — УМНЫЙ Хорарный Император!

Я анализирую РЕАЛЬНЫЕ жизненные ситуации:
• 💰 Финансы и карьера
• 💖 Отношения и брак  
• 🏥 Здоровье и решения
• 🚀 Планы и проекты

❗ Я НЕ отвечаю на:
• Метеорологические вопросы
• Вопросы с нарушением логики времени
• Запросы на "чудеса без усилий"

Задайте ОСМЫСЛЕННЫЙ вопрос о вашей жизни!
"""
            bot.reply_to(message, start_text)
        return
    
    try:
        # ПРОВЕРЯЕМ ЛЕГИТИМНОСТЬ ВОПРОСА
        is_legitimate, legitimacy_message = bot_brain.analyze_question_legitimacy(message.text)
        
        if not is_legitimate:
            bot.reply_to(message, legitimacy_message)
            return
        
        # ЕСЛИ ВОПРОС ЛЕГИТИМЕН - ДЕЛАЕМ АНАЛИЗ
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

✅ Вопрос прошел проверку на реалистичность
🤖 Уровень анализа: {bot_brain.experience + 1}
"""
        bot.reply_to(message, response)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

def get_detailed_analysis(question):
    """Функция для анализа в группах"""
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
    
    question_type, emoji = bot_brain.analyze_question_type(question)
    verdict, reasoning = bot_brain.make_decision(moon_sign, sun_sign, question_type)
    strategy = bot_brain.generate_strategy(verdict, moon_sign, question_type)
    
    return f"""
🔮 ГРУППОВОЙ АНАЛИЗ
⏰ {display_time}

❓ ВОПРОС: {question}
🎯 ТИП: {question_type} {emoji}

📊 КАРТА:
• 🌙 Луна: {moon_sign}
• ☀️ Солнце: {sun_sign}

⚡ ВЕРДИКТ: {verdict}
💡 ОБОСНОВАНИЕ: {reasoning}

💫 СТРАТЕГИЯ: {strategy}
"""

print("🔄 УМНЫЙ бот с ДЕТЕКТОРОМ РЕАЛЬНОСТИ запущен...")
while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
