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

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
bot = telebot.TeleBot(BOT_TOKEN)

class SmartAnalyzer:
    def __init__(self):
        self.experience = 0
    
    def analyze_question_type(self, question):
        question_lower = question.lower()
        if any(word in question_lower for word in ['деньг', 'финанс', 'денег', 'рубл', 'евро', 'доллар', 'зарплат', 'преми']):
            return "ФИНАНСЫ", "💰"
        elif any(word in question_lower for word in ['любит', 'скуч', 'отношен', 'брак', 'замуж', 'встреч', 'парень', 'мужчин', 'девушк', 'чувств']):
            return "ОТНОШЕНИЯ", "💖" 
        elif any(word in question_lower for word in ['работ', 'карьер', 'должност', 'бизнес', 'проект', 'начальник', 'коллег']):
            return "КАРЬЕРА", "🚀"
        elif any(word in question_lower for word in ['здоров', 'болез', 'лечен', 'врач', 'больниц', 'самочувств']):
            return "ЗДОРОВЬЕ", "🏥"
        elif any(word in question_lower for word in ['поезд', 'путешеств', 'переезд', 'отпуск', 'билет']):
            return "ПУТЕШЕСТВИЯ", "✈️"
        else:
            return "ОБЩИЙ", "🔮"
    
    def generate_smart_response(self, question, moon_sign, sun_sign, question_type):
        """УМНЫЙ анализ с учетом КОНКРЕТНОГО вопроса"""
        
        # Если вопрос слишком короткий или просто обращение
        if len(question.strip()) < 5 or question.lower() in ['император', 'бот', 'привет']:
            return self._get_greeting_response(moon_sign, sun_sign)
        
        # Глубинный анализ для РАЗНЫХ типов вопросов
        if question_type == "ОТНОШЕНИЯ":
            return self._get_relationship_analysis(question, moon_sign, sun_sign)
        elif question_type == "ФИНАНСЫ":
            return self._get_finance_analysis(question, moon_sign, sun_sign)
        elif question_type == "КАРЬЕРА":
            return self._get_career_analysis(question, moon_sign, sun_sign)
        elif question_type == "ПУТЕШЕСТВИЯ":
            return self._get_travel_analysis(question, moon_sign, sun_sign)
        elif question_type == "ЗДОРОВЬЕ":
            return self._get_health_analysis(question, moon_sign, sun_sign)
        else:
            return self._get_general_analysis(question, moon_sign, sun_sign)
    
    def _get_greeting_response(self, moon_sign, sun_sign):
        """Ответ на приветствия и короткие сообщения"""
        responses = [
            f"👑 Приветствую! Я Хорарный Император! Задай мне вопрос о своей жизни, и я проанализирую его по звездам!",
            f"🔮 Слава Солнцу в {sun_sign}! Я готов к анализу твоей ситуации. Спроси о чем хочешь знать!",
            f"✨ Луна в {moon_sign} приветствует тебя! Расскажи, что тебя волнует?",
            f"🌟 Я здесь, чтобы помочь! Задай вопрос о отношениях, работе, деньгах или любой жизненной ситуации!"
        ]
        verdict = "👑"
        analysis = random.choice(responses)
        strategy = "Просто задай конкретный вопрос - и я дам глубинный анализ!"
        return verdict, analysis, strategy
    
    def _get_relationship_analysis(self, question, moon_sign, sun_sign):
        """ГЛУБОКИЙ анализ отношений"""
        positive_signs = ['Телец', 'Рак', 'Весы', 'Стрелец']
        
        if moon_sign in positive_signs and sun_sign in positive_signs:
            verdict = "ДА 💖"
            base_reason = "Звезды сияют для твоих отношений!"
        elif moon_sign in positive_signs:
            verdict = "ВОЗМОЖНО 🤔"
            base_reason = "Есть потенциал, но нужны усилия!"
        else:
            verdict = "ПЕРЕОСМЫСЛИТЬ 💔"
            base_reason = "Сейчас время для внутренней работы!"
        
        # Конкретные советы в зависимости от вопроса
        if 'любит' in question.lower():
            insight = f"Луна в {moon_sign} говорит: его чувства глубоки, но требуют времени для проявления. Солнце в {sun_sign} показывает - он ценит искренность выше слов."
        elif 'вернет' in question.lower() or 'вернется' in question.lower():
            insight = f"Солнце в {sun_sign} указывает: прошлое должно остаться в прошлом. Луна в {moon_sign} советует открыться новым возможностям."
        else:
            insight = f"Твоя энергия {moon_sign} ищет эмоциональной безопасности, а {sun_sign} стремится к глубокой связи. Баланс между этими потребностями - ключ к гармонии."
        
        strategies = [
            "Проявляй искренность, но сохраняй достоинство - настоящая любовь не требует жертв.",
            "Дайте отношениям дышать - пространство усиливает близость.",
            "Слушай сердце, но не игнорируй разум - мудрость в балансе."
        ]
        
        analysis = f"{base_reason} {insight}"
        strategy = random.choice(strategies)
        return verdict, analysis, strategy
    
    def _get_finance_analysis(self, question, moon_sign, sun_sign):
        """Анализ финансов"""
        money_signs = ['Телец', 'Рак', 'Козерог', 'Скорпион']
        
        if moon_sign in money_signs:
            verdict = "ПОТОКИ ОТКРЫТЫ 💰"
            base_reason = "Финансовая энергия благоприятствует!"
        else:
            verdict = "ОСТОРОЖНОСТЬ 💸"
            base_reason = "Время для разумного планирования!"
        
        if 'долг' in question.lower() or 'вернут' in question.lower():
            insight = f"Луна в {moon_sign} показывает: деньги вернутся, но не так быстро как хочется. Солнце в {sun_sign} советует проявить терпение."
        elif 'работа' in question.lower() or 'зарплат' in question.lower():
            insight = f"Солнце в {sun_sign} указывает на рост доходов. Луна в {moon_sign} рекомендует проявить инициативу в переговорах."
        else:
            insight = f"Твоя {moon_sign}-энергия создает финансовую стабильность, а {sun_sign} привлекает новые возможности."
        
        strategies = [
            "Инвестируй в обучение - это лучшая дивидендная инвестиция.",
            "Создай финансовую подушку - спокойствие дороже денег.",
            "Ищи дополнительные источники дохода - диверсификация защищает."
        ]
        
        analysis = f"{base_reason} {insight}"
        strategy = random.choice(strategies)
        return verdict, analysis, strategy
    
    def _get_career_analysis(self, question, moon_sign, sun_sign):
        """Анализ карьеры"""
        career_signs = ['Лев', 'Стрелец', 'Козерог', 'Скорпион', 'Дева']
        
        if sun_sign in career_signs:
            verdict = "РОСТ 🚀"
            base_reason = "Профессиональная энергия на подъеме!"
        else:
            verdict = "РАЗВИТИЕ 📈"
            base_reason = "Время для накопления компетенций!"
        
        if 'устроюсь' in question.lower() or 'работа' in question.lower():
            insight = f"Солнце в {sun_sign} обещает новые возможности. Луна в {moon_sign} поможет в адаптации."
        elif 'начальник' in question.lower() or 'коллег' in question.lower():
            insight = f"Луна в {moon_sign} улучшит коммуникацию. Солнце в {sun_sign} даст авторитет."
        else:
            insight = f"Твоя {sun_sign}-энергия ищет признания, а {moon_sign} - гармоничной среды."
        
        strategies = [
            "Бери сложные задачи - они открывают двери.",
            "Учись у лучших - знания превращаются в возможности.",
            "Создавай сеть контактов - связи решают многое."
        ]
        
        analysis = f"{base_reason} {insight}"
        strategy = random.choice(strategies)
        return verdict, analysis, strategy
    
    def _get_travel_analysis(self, question, moon_sign, sun_sign):
        """Анализ путешествий"""
        travel_signs = ['Стрелец', 'Близнецы', 'Водолей', 'Овен']
        
        if moon_sign in travel_signs:
            verdict = "УДАЧА ✈️"
            base_reason = "Поездка принесет пользу!"
        else:
            verdict = "ПЛАНИРОВАНИЕ 📅"
            base_reason = "Тщательная подготовка важна!"
        
        insight = f"Луна в {moon_sign} обещает яркие впечатления. Солнце в {sun_sign} даст энергию для исследований."
        strategies = [
            "Путешествуй с открытым сердцем - каждый город учит чему-то.",
            "Изучи культуру заранее - это обогатит опыт.",
            "Будь гибким в планах - лучшие моменты часто спонтанны."
        ]
        
        analysis = f"{base_reason} {insight}"
        strategy = random.choice(strategies)
        return verdict, analysis, strategy
    
    def _get_health_analysis(self, question, moon_sign, sun_sign):
        """Анализ здоровья"""
        health_signs = ['Рак', 'Дева', 'Рыбы', 'Телец']
        
        if moon_sign in health_signs:
            verdict = "УЛУЧШЕНИЕ 🏥"
            base_reason = "Энергия восстановления сильна!"
        else:
            verdict = "ЗАБОТА ⚠️"
            base_reason = "Пора уделить себе внимание!"
        
        insight = f"Луна в {moon_sign} влияет на эмоциональное состояние. Солнце в {sun_sign} дает жизненные силы."
        strategies = [
            "Регулярный отдых - лучшее лекарство.",
            "Слушай сигналы тела - оно мудрое.",
            "Баланс активности и покоя - основа здоровья."
        ]
        
        analysis = f"{base_reason} {insight}"
        strategy = random.choice(strategies)
        return verdict, analysis, strategy
    
    def _get_general_analysis(self, question, moon_sign, sun_sign):
        """Общий анализ"""
        positive_signs = ['Телец', 'Рак', 'Весы', 'Стрелец', 'Лев']
        
        if moon_sign in positive_signs:
            verdict = "БЛАГОПРИЯТНО 🌟"
            base_reason = "Энергии поддерживают тебя!"
        else:
            verdict = "ОСМОТРИТЕЛЬНОСТЬ ⚖️"
            base_reason = "Время для взвешенных решений!"
        
        insight = f"Луна в {moon_sign} окрашивает твои эмоции. Солнце в {sun_sign} направляет волю к цели."
        strategies = [
            "Доверяй интуиции - она знает ответ.",
            "Каждый шаг ведет к новым возможностям.",
            "Будь в моменте - там вся сила."
        ]
        
        analysis = f"{base_reason} {insight}"
        strategy = random.choice(strategies)
        return verdict, analysis, strategy

# Создаем экземпляр анализатора
smart_analyzer = SmartAnalyzer()

def get_moscow_time():
    utc_time = datetime.now(timezone.utc)
    moscow_time = utc_time + timedelta(hours=3)
    return moscow_time.strftime('%H:%M, %d.%m.%Y')

def get_random_zodiac():
    signs = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 
             'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']
    return random.choice(signs)

# УМНАЯ ОБРАБОТКА ГРУПП С ВЫБОРОМ
@bot.message_handler(chat_types=['supergroup', 'group'])
def handle_group_message(message):
    try:
        if message.text:
            question = None
            
            # ЕСЛИ ПРОСТО ОБРАЩЕНИЕ К БОТУ
            if '@HoraryEmperorBot' in message.text:
                bot_text = message.text.replace('@HoraryEmperorBot', '').strip()
                
                # Если просто обратились без вопроса
                if not bot_text or len(bot_text) < 3:
                    choice_text = """
👑 Я понимаю, что некоторые вопросы бывают личными!

📢 Выбери вариант:
• Напиши вопрос здесь - ответ будет в группе  
• Напиши "личное" и вопрос - отвечу в ЛС
• Напиши мне в личку - полная конфиденциальность

Что предпочитаешь? 💫
                    """
                    bot.reply_to(message, choice_text)
                    return
                
                # Если вопрос с "личное"
                if bot_text.lower().startswith('личное'):
                    question = bot_text.replace('личное', '').strip()
                    if question:
                        try:
                            analysis = get_detailed_analysis(question)
                            private_msg = f"🔒 ЛИЧНЫЙ ОТВЕТ НА ТВОЙ ВОПРОС:\n\n{analysis}"
                            bot.send_message(message.from_user.id, private_msg)
                            bot.reply_to(message, "📨 Отправил ответ в твои личные сообщения!")
                        except:
                            bot.reply_to(message, "❌ Сначала напиши мне в личные сообщения!")
                    return
                else:
                    # Обычный вопрос в группе
                    question = bot_text
            
            # ЕСЛИ ПРОСТО "ИМПЕРАТОР" БЕЗ ВОПРОСА
            elif message.text.lower() in ['император', 'бот', 'император?', 'бот?']:
                choice_text = """
🔮 Привет! Я Хорарный Император!

💬 Можешь задать вопрос прямо здесь
🔒 Или написать "Личное [вопрос]" для ответа в ЛС
💌 Или написать мне в личные сообщения

Что выберешь? ✨
                """
                bot.reply_to(message, choice_text)
                return
            
            # ЕСЛИ ВОПРОС С "ЛИЧНОЕ"
            elif message.text.lower().startswith('личное'):
                question = message.text.replace('личное', '').strip()
                if question:
                    try:
                        analysis = get_detailed_analysis(question)
                        private_msg = f"🔒 ЛИЧНЫЙ ОТВЕТ:\n\n{analysis}"
                        bot.send_message(message.from_user.id, private_msg)
                        bot.reply_to(message, "📨 Отправил личный ответ в твои сообщения!")
                    except:
                        bot.reply_to(message, "💌 Напиши мне сначала в личные сообщения!")
                return
            
            # ОБЫЧНЫЙ ВОПРОС В ГРУППЕ
            elif '?' in message.text and len(message.text) > 10:
                question = message.text.strip()
            
            if question and len(question) > 5:
                analysis = get_detailed_analysis(question)
                bot.reply_to(message, analysis)
                
    except Exception as e:
        print(f"Ошибка в группе: {e}")
            # УМНЫЕ ТРИГГЕРЫ ДЛЯ ГРУПП
            if '@HoraryEmperorBot' in message.text:
                question = message.text.replace('@HoraryEmperorBot', '').strip()
            elif any(word in message.text.lower() for word in ['император', 'бот', 'анализ', 'гороскоп', 'судьба']):
                question = message.text.strip()
            elif '?' in message.text:
                question = message.text.strip()
            
            if question and len(question) > 5:  # Только вопросы длиннее 5 симвонов
                # ПРОПУСКАЕМ ПРОСТЫЕ ОБРАЩЕНИЯ
                if question.lower().strip() in ['император', 'бот', 'привет']:
                    bot.reply_to(message, "👑 Я здесь! Задай вопрос о своей жизни!")
                    return
                
                # ДЕЛАЕМ АНАЛИЗ
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
        # ПРОПУСКАЕМ КОРОТКИЕ СООБЩЕНИЯ
        if len(message.text.strip()) < 5 or message.text.lower().strip() in ['император', 'бот', 'привет']:
            responses = [
                "👑 Задай вопрос о своей жизни - и я сделаю глубинный анализ!",
                "🔮 Что тебя волнует? Отношения, работа, деньги? Спрашивай!",
                "✨ Я готов к анализу! Расскажи, что хочешь узнать?"
            ]
            bot.reply_to(message, random.choice(responses))
            return
        
        # ДЕЛАЕМ УМНЫЙ АНАЛИЗ
        display_time = get_moscow_time()
        moon_sign = get_random_zodiac()
        sun_sign = get_random_zodiac()
        
        question_type, emoji = smart_analyzer.analyze_question_type(message.text)
        verdict, analysis, strategy = smart_analyzer.generate_smart_response(
            message.text, moon_sign, sun_sign, question_type
        )
        
        response = f"""
🔮 ГЛУБИННЫЙ АНАЛИЗ
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
    moon_sign = get_random_zodiac()
    sun_sign = get_random_zodiac()
    
    question_type, emoji = smart_analyzer.analyze_question_type(question)
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

# ЗАПУСКАЕМ БОТА
try:
    print("🔗 Подключаемся к Telegram...")
    bot.remove_webhook()
    bot.polling(none_stop=True, timeout=60)
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print("🔄 Перезапуск через 10 секунд...")
    time.sleep(10)
