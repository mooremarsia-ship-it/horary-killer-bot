import telebot
import time
import random
from datetime import datetime, timedelta, timezone
from flask import Flask
import threading

# Создаем Flask приложение для здоровья
app = Flask(__name__)

@app.route('/')
def health_check():
    return "🔄 Хорарный Император работает!", 200

# Запускаем Flask в отдельном потоке
def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

# Запускаем HTTP-сервер в фоне
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

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
        """БОЛЕЕ МЯГКАЯ проверка вопроса"""
        question_lower = question.lower()
        
        # 1. ПРОВЕРКА НА АБСУРД
        if self._is_absurd(question_lower):
            return False, "❌ Этот вопрос не для хорарного анализа. Задай вопрос о своей жизни!"
        
        # 2. ПРОВЕРКА НА ПОГОДУ/ВРЕМЯ
        if self._is_weather_time(question_lower):
            return False, "🌤️ Я анализирую жизненные ситуации, а не погоду или время!"
        
        return True, "Вопрос принят"
    
    def _is_absurd(self, question):
        """Проверяет совсем абсурдные вопросы"""
        absurd = [
            'подарят квартиру', 'получу миллион', 'стану знаменитым',
            'встречу принца', 'найду клад', 'упадет с неба'
        ]
        return any(word in question for word in absurd)
    
    def _is_weather_time(self, question):
        """Проверяет вопросы о погоде/времени"""
        weather_time = [
            'погода', 'дождь', 'солнце', 'градус', 'температур',
            'сколько времени', 'который час', 'когда сейчас'
        ]
        return any(word in question for word in weather_time)

class SmartAnalyzer:
    def __init__(self):
        self.experience = 0
    
    def analyze_question_type(self, question):
        question_lower = question.lower()
        if any(word in question_lower for word in ['деньг', 'финанс', 'денег', 'рубл', 'евро', 'доллар']):
            return "ФИНАНСЫ", "💰"
        elif any(word in question_lower for word in ['любит', 'скуч', 'отношен', 'брак', 'замуж', 'встреч', 'парень', 'мужчин', 'девушк']):
            return "ОТНОШЕНИЯ", "💖" 
        elif any(word in question_lower for word in ['работ', 'карьер', 'должност', 'бизнес', 'проект']):
            return "КАРЬЕРА", "🚀"
        elif any(word in question_lower for word in ['здоров', 'болез', 'лечен', 'врач', 'больниц']):
            return "ЗДОРОВЬЕ", "🏥"
        elif any(word in question_lower for word in ['поезд', 'путешеств', 'переезд', 'отпуск']):
            return "ПУТЕШЕСТВИЯ", "✈️"
        else:
            return "ОБЩИЙ", "🔮"
    
    def generate_smart_response(self, question, moon_sign, sun_sign, question_type):
        """УМНЫЙ анализ в зависимости от типа вопроса"""
        
        question_lower = question.lower()
        
        # ОСОБЫЕ СЛУЧАИ
        if any(word in question_lower for word in ['привет', 'здравствуй', 'hello', 'hi', 'начать']):
            return self._get_greeting_response(moon_sign, sun_sign)
        
        # РАЗНЫЕ ТИПЫ ВОПРОСОВ - РАЗНЫЕ ОТВЕТЫ
        if question_type == "ОТНОШЕНИЯ":
            return self._get_relationship_analysis(moon_sign, sun_sign, question)
        elif question_type == "ФИНАНСЫ":
            return self._get_finance_analysis(moon_sign, sun_sign, question)
        elif question_type == "КАРЬЕРА":
            return self._get_career_analysis(moon_sign, sun_sign, question)
        elif question_type == "ПУТЕШЕСТВИЯ":
            return self._get_travel_analysis(moon_sign, sun_sign, question)
        elif question_type == "ЗДОРОВЬЕ":
            return self._get_health_analysis(moon_sign, sun_sign, question)
        else:
            return self._get_general_analysis(moon_sign, sun_sign, question)
    
    def _get_greeting_response(self, moon_sign, sun_sign):
        """Ответ на приветствия"""
        responses = [
            f"👑 Приветствую! Император с Луной в {moon_sign} к твоим услугам!",
            f"🔮 Слава Солнцу в {sun_sign}! Хорарный Император готов к анализу!",
            f"✨ Привет! Луна в {moon_sign} благоволит нашей беседе!",
            f"🌟 Солнце в {sun_sign} приветствует тебя! Задай свой вопрос!"
        ]
        verdict = "👑"
        analysis = random.choice(responses)
        strategy = "Задай вопрос о своей ситуации - и получи глубинный астрологический анализ!"
        return verdict, analysis, strategy
    
    def _get_relationship_analysis(self, moon_sign, sun_sign, question):
        """АНАЛИЗ ОТНОШЕНИЙ"""
        if moon_sign in ['Телец', 'Рак', 'Весы', 'Стрелец']:
            verdict = "ДА 💖"
            base_reason = "Звезды благоволят твоим отношениям!"
        else:
            verdict = "НЕТ, НО... 💔"
            base_reason = "Сейчас время для работы над собой!"
        
        insights = [
            f"""Твоя Луна в {moon_sign} создает уникальный эмоциональный магнетизм.
Солнце в {sun_sign} дает тебе ту энергию, которая привлекает нужных людей.""",

            f"""Отношения - это танец двух вселенных. 
Твоя {moon_sign}-энергия ищет гармонии, а {sun_sign}-энергия стремится к глубине.""",

            f"""Луна в {moon_sign} говорит о эмоциональной щедрости.
Солнце в {sun_sign} - о страсти к трансформации партнера."""
        ]
        
        strategies = [
            "Будь искренней в своих чувствах - настоящая близость рождается из честности.",
            "Дайте отношениям время развиваться - как цветок, который раскрывается постепенно.",
            "Слушай не только слова, но и энергию между словами - там живет истина."
        ]
        
        analysis = f"{base_reason} {random.choice(insights)}"
        strategy = random.choice(strategies)
        return verdict, analysis, strategy
    
    def _get_finance_analysis(self, moon_sign, sun_sign, question):
        """АНАЛИЗ ФИНАНСОВ"""
        if moon_sign in ['Телец', 'Рак', 'Козерог']:
            verdict = "ХОРОШО 💰"
            base_reason = "Финансовые потоки благоприятны!"
        else:
            verdict = "ОСТОРОЖНО 💸"
            base_reason = "Время для разумной экономии!"
        
        insights = [
            f"""Луна в {moon_sign} влияет на твое отношение к деньгам.
Солнце в {sun_sign} указывает на потенциал заработка.""",

            f"""Деньги приходят к тем, кто создает ценность.
Твоя {sun_sign}-энергия может стать источником дохода.""",

            f"""Финансовая стабильность начинается с внутренней.
Луна в {moon_sign} помогает найти баланс."""
        ]
        
        strategies = [
            "Инвестируй в знания - это самая надежная валюта.",
            "Создавай несколько источников дохода - диверсификация защищает.",
            "Деньги любят счет и уважительное отношение."
        ]
        
        analysis = f"{base_reason} {random.choice(insights)}"
        strategy = random.choice(strategies)
        return verdict, analysis, strategy
    
    def _get_career_analysis(self, moon_sign, sun_sign, question):
        """АНАЛИЗ КАРЬЕРЫ"""
        if sun_sign in ['Лев', 'Стрелец', 'Козерог', 'Скорпион']:
            verdict = "УСПЕХ 🚀"
            base_reason = "Карьерный рост вероятен!"
        else:
            verdict = "РАЗВИТИЕ 📈"
            base_reason = "Время для накопления опыта!"
        
        insights = [
            f"""Солнце в {sun_sign} указывает на твое профессиональное призвание.
Луна в {moon_sign} помогает в коммуникации с коллегами.""",

            f"""Твоя {sun_sign}-энергия ищет самовыражения в работе.
Найди дело, которое резонирует с твоей сущностью.""",

            f"""Карьера - это не только должность, но и реализация талантов.
Луна в {moon_sign} раскрывает твои скрытые способности."""
        ]
        
        strategies = [
            "Не бойся брать на себя ответственность - это путь к росту.",
            "Учись у лучших в твоей сфере - знания открывают двери.",
            "Создавай проекты, а не просто выполняй задачи."
        ]
        
        analysis = f"{base_reason} {random.choice(insights)}"
        strategy = random.choice(strategies)
        return verdict, analysis, strategy
    
    def _get_travel_analysis(self, moon_sign, sun_sign, question):
        """АНАЛИЗ ПУТЕШЕСТВИЙ"""
        if moon_sign in ['Стрелец', 'Близнецы', 'Водолей']:
            verdict = "БЛАГОПРИЯТНО ✈️"
            base_reason = "Поездка будет успешной!"
        else:
            verdict = "ПЛАНИРУЙТЕ 📅"
            base_reason = "Тщательная подготовка важна!"
        
        insights = [
            f"""Луна в {moon_sign} благоприятствует новым впечатлениям.
Солнце в {sun_sign} дает энергию для исследований.""",

            f"""Путешествие расширяет сознание.
Твоя {moon_sign}-энергия жаждет новых горизонтов.""",

            f"""Дорога учит большему, чем цель.
Наслаждайся процессом, а не только результатом."""
        ]
        
        strategies = [
            "Путешествуй с открытым сердцем - каждая поездка меняет тебя.",
            "Изучи культуру места заранее - это обогатит опыт.",
            "Будь гибким в планах - лучшие приключения часто спонтанны."
        ]
        
        analysis = f"{base_reason} {random.choice(insights)}"
        strategy = random.choice(strategies)
        return verdict, analysis, strategy
    
    def _get_health_analysis(self, moon_sign, sun_sign, question):
        """АНАЛИЗ ЗДОРОВЬЯ"""
        if moon_sign in ['Рак', 'Дева', 'Рыбы']:
            verdict = "УЛУЧШЕНИЕ 🏥"
            base_reason = "Энергия восстановления сильна!"
        else:
            verdict = "ВНИМАНИЕ ⚠️"
            base_reason = "Позаботься о себе!"
        
        insights = [
            f"""Луна в {moon_sign} влияет на твое эмоциональное состояние.
Солнце в {sun_sign} дает жизненные силы.""",

            f"""Здоровье - это гармония души и тела.
Твоя {moon_sign}-энергия ищет баланса.""",

            f"""Тело говорит языком симптомов.
Услышь, что пытается сказать твое {sun_sign}-Солнце."""
        ]
        
        strategies = [
            "Регулярные прогулки на природе - лучшая терапия.",
            "Слушай сигналы тела - оно мудрее любого врача.",
            "Баланс работы и отдыха - основа здоровья."
        ]
        
        analysis = f"{base_reason} {random.choice(insights)}"
        strategy = random.choice(strategies)
        return verdict, analysis, strategy
    
    def _get_general_analysis(self, moon_sign, sun_sign, question):
        """ОБЩИЙ АНАЛИЗ"""
        if moon_sign in ['Телец', 'Рак', 'Весы', 'Стрелец']:
            verdict = "ПОЗИТИВНО 🌟"
            base_reason = "Энергии благоприятствуют!"
        else:
            verdict = "ОСМОТРИТЕЛЬНО ⚖️"
            base_reason = "Время для взвешенных решений!"
        
        insights = [
            f"""Луна в {moon_sign} окрашивает твои эмоции.
Солнце в {sun_sign} направляет волю.""",

            f"""Каждая ситуация - урок.
Твоя {moon_sign}-Луна помогает усвоить его.""",

            f"""Жизнь - это поток.
Твое {sun_sign}-Солнце учится управлять им."""
        ]
        
        strategies = [
            "Доверяй интуиции - она знает дорогу.",
            "Каждое решение ведет к новым возможностям.",
            "Будь present в моменте - там вся сила."
        ]
        
        analysis = f"{base_reason} {random.choice(insights)}"
        strategy = random.choice(strategies)
        return verdict, analysis, strategy

# Создаем экземпляры классов
reality_checker = RealityChecker()
smart_analyzer = SmartAnalyzer()

def get_moscow_time():
    utc_time = datetime.now(timezone.utc)
    moscow_time = utc_time + timedelta(hours=3)
    return moscow_time.strftime('%H:%M, %d.%m.%Y')

def get_random_zodiac():
    signs = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 
             'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']
    return random.choice(signs)

# ОБРАБОТКА ГРУПП
@bot.message_handler(chat_types=['supergroup', 'group'])
def handle_group_message(message):
    try:
        if message.text:
            question = None
            
            # РАЗНЫЕ ВАРИАНТЫ ОБРАЩЕНИЙ
            if '@HoraryEmperorBot' in message.text:
                question = message.text.replace('@HoraryEmperorBot', '').strip()
            elif 'Император' in message.text:
                question = message.text.replace('Император', '').strip()
            elif 'император' in message.text.lower():
                question = message.text.lower().replace('император', '').strip()
            elif '?' in message.text and len(message.text) > 10:
                question = message.text.strip()
            
            if question and len(question) > 2:
                # ПРОВЕРЯЕМ ЛЕГИТИМНОСТЬ
                is_legitimate, legitimacy_message = reality_checker.check_reality(question)
                
                if not is_legitimate:
                    bot.reply_to(message, legitimacy_message)
                    return
                
                # ЕСЛИ ВОПРОС ЛЕГИТИМЕН - АНАЛИЗ
                analysis = get_detailed_analysis(question)
                bot.reply_to(message, analysis)
    except Exception as e:
        print(f"Ошибка в группе: {e}")

# ЛИЧНЫЕ СООБЩЕНИЯ
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('/'):
        if message.text == '/start':
            start_text = """
🔮 Я — ХОРАРНЫЙ ИМПЕРАТОР!

Задай вопрос о:
• 💖 Отношениях и чувствах
• 💰 Финансах и деньгах  
• 🚀 Карьере и работе
• 🏥 Здоровье и самочувствии
• ✈️ Поездках и путешествиях
• 🌟 Любой жизненной ситуации

Я дам мудрый совет на основе звездных карт!"""
            bot.reply_to(message, start_text)
        return
    
    try:
        # ПРОВЕРЯЕМ ЛЕГИТИМНОСТЬ ВОПРОСА
        is_legitimate, legitimacy_message = reality_checker.check_reality(message.text)
        
        if not is_legitimate:
            bot.reply_to(message, legitimacy_message)
            return
        
        # ЕСЛИ ВОПРОС ЛЕГИТИМЕН - ДЕЛАЕМ УМНЫЙ АНАЛИЗ
        display_time = get_moscow_time()
        
        # ИСПОЛЬЗУЕМ СЛУЧАЙНЫЕ ЗНАКИ (без ephem)
        moon_sign = get_random_zodiac()
        sun_sign = get_random_zodiac()
        
        question_type, emoji = smart_analyzer.analyze_question_type(message.text)
        
        # УМНЫЙ АНАЛИЗ
        verdict, analysis, strategy = smart_analyzer.generate_smart_response(
            message.text, moon_sign, sun_sign, question_type
        )
        
        response = f"""
🔮 УМНЫЙ ХОРАРНЫЙ АНАЛИЗ
⏰ {display_time}, МОСКВА

❓ ВОПРОС: {message.text}
🎯 ТИП: {question_type} {emoji}

📊 КАРТА:
• 🌙 Луна: {moon_sign}
• ☀️ Солнце: {sun_sign}

⚡ ВЕРДИКТ: {verdict}

💫 АНАЛИЗ:
{analysis}

🎯 СТРАТЕГИЯ:
{strategy}

✨ Уровень анализа: {smart_analyzer.experience + 1}
"""
        bot.reply_to(message, response)
        smart_analyzer.experience += 1
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

def get_detailed_analysis(question):
    """Функция для анализа в группах"""
    display_time = get_moscow_time()
    
    # ИСПОЛЬЗУЕМ СЛУЧАЙНЫЕ ЗНАКИ (без ephem)
    moon_sign = get_random_zodiac()
    sun_sign = get_random_zodiac()
    
    question_type, emoji = smart_analyzer.analyze_question_type(question)
    
    # УМНЫЙ АНАЛИЗ ДЛЯ ГРУПП
    verdict, analysis, strategy = smart_analyzer.generate_smart_response(
        question, moon_sign, sun_sign, question_type
    )
    
    return f"""
🔮 АНАЛИЗ ОТ ИМПЕРАТОРА
⏰ {display_time}

❓ ВОПРОС: {question}
🎯 ТИП: {question_type} {emoji}

📊 КАРТА:
• 🌙 Луна: {moon_sign}
• ☀️ Солнце: {sun_sign}

⚡ ВЕРДИКТ: {verdict}

💫 АНАЛИЗ:
{analysis}

🎯 СТРАТЕГИЯ:
{strategy}

✨ @HoraryEmperorBot
"""

print("🔄 ХОРАРНЫЙ ИМПЕРАТОР запущен...")
print("🌐 HTTP-сервер здоровья работает на порту 5000")

# ЗАПУСКАЕМ БОТА БЕЗ Threaded polling (чтобы избежать ошибки 409)
try:
    print("🔗 Подключаемся к Telegram...")
    bot.remove_webhook()
    bot.polling(none_stop=True, timeout=60)
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print("🔄 Перезапуск через 10 секунд...")
    time.sleep(10)
