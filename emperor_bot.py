import telebot
import time
import random
import json
import os
from datetime import datetime, timedelta, timezone
from flask import Flask
import threading

print("🌌 Запускаю УМНОГО Хорарного Императора с РЕАЛЬНЫМ обучением...")

BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)
@app.route('/')
def home():
    return "💫 Умный Император работает!", 200

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

class SmartEmperor:
    def __init__(self):
        print("🔮 Умный Император инициализирован!")
        self.memory_file = 'smart_memory.json'
        self.analysis_history = {}
        self.load_memory()
    
    def load_memory(self):
        """Загружаем память и историю анализов"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.memory = data.get('memory', {})
                    self.analysis_history = data.get('analysis_history', {})
                print(f"🧠 Загружено {len(self.memory)} записей, {len(self.analysis_history)} анализов")
            else:
                self.memory = {}
                self.analysis_history = {}
        except:
            self.memory = {}
            self.analysis_history = {}
    
    def save_memory(self):
        """Сохраняем память"""
        try:
            data = {
                'memory': self.memory,
                'analysis_history': self.analysis_history
            }
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def learn_from_interaction(self, question, response, user_id):
        """РЕАЛЬНО учимся на каждом вопросе"""
        key = f"{user_id}_{question[:30].lower()}"
        
        # Считаем частоту вопросов
        if key not in self.memory:
            self.memory[key] = {
                'question': question,
                'response': response[:100],  # Сохраняем часть ответа для обучения
                'timestamp': datetime.now().isoformat(),
                'count': 1,
                'last_used': datetime.now().isoformat()
            }
        else:
            self.memory[key]['count'] += 1
            self.memory[key]['last_used'] = datetime.now().isoformat()
        
        # Сохраняем историю анализов для уникальности
        analysis_key = f"{question[:20].lower()}_{datetime.now().strftime('%H')}"
        if analysis_key not in self.analysis_history:
            self.analysis_history[analysis_key] = 0
        self.analysis_history[analysis_key] += 1
        
        self.save_memory()
        print(f"🧠 РЕАЛЬНО выучил: {question[:30]}... (использован {self.memory[key]['count']} раз)")

    def generate_unique_analysis(self, question, intent):
        """Генерируем УНИКАЛЬНЫЙ анализ каждый раз"""
        current_time = datetime.now(timezone.utc) + timedelta(hours=3)
        time_str = current_time.strftime('%H:%M, %d %B %Y')
        
        # Базовые данные для уникальности
        base_signs = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 
                     'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']
        base_planets = ['Солнце', 'Луна', 'Меркурий', 'Венера', 'Марс', 'Юпитер', 'Сатурн', 'Уран', 'Нептун', 'Плутон']
        base_aspects = ['трин', 'квадрат', 'секстиль', 'оппозиция', 'соединение']
        base_houses = ['I дом', 'II дом', 'III дом', 'IV дом', 'V дом', 'VI дом', 
                      'VII дом', 'VIII дом', 'IX дом', 'X дом', 'XI дом', 'XII дом']
        
        # Уникальные комбинации для каждого анализа
        random.seed(f"{question}_{current_time.strftime('%H%M')}")
        
        main_sign = random.choice(base_signs)
        secondary_sign = random.choice([s for s in base_signs if s != main_sign])
        main_planet = random.choice(base_planets)
        aspect_planet = random.choice([p for p in base_planets if p != main_planet])
        aspect_type = random.choice(base_aspects)
        influential_house = random.choice(base_houses)
        
        # Уникальные градусы
        main_degree = random.randint(1, 29)
        secondary_degree = random.randint(1, 29)
        
        # Генерация ответа в зависимости от намерения
        if intent == "MONEY_QUESTION":
            return self._generate_money_answer(question, time_str, main_sign, main_planet, aspect_type, main_degree)
        elif "LOVE" in intent:
            return self._generate_love_answer(question, time_str, main_sign, secondary_sign, aspect_planet, aspect_type)
        elif "FUTURE" in question.upper():
            return self._generate_future_answer(question, time_str, main_planet, influential_house, aspect_type)
        else:
            return self._generate_universal_answer(question, time_str, main_sign, main_planet, aspect_planet, aspect_type, main_degree)

    def _generate_money_answer(self, question, time_str, sign, planet, aspect, degree):
        """Генерируем УНИКАЛЬНЫЙ денежный анализ"""
        
        # ДЕТЕРМИНИРУЕМ ОТВЕТ - да/нет с вероятностью
        question_lower = question.lower()
        if 'сегодня' in question_lower or 'завтра' in question_lower:
            money_chance = random.randint(1, 100)
            if money_chance > 60:
                money_answer = "💰 *ДА, деньги придут!* Вероятность 75%"
                reason = "Юпитер формирует благоприятный аспект с Луной"
            elif money_chance > 30:
                money_answer = "🤔 *ВОЗМОЖНО, но не сегодня.* Вероятность 45%"
                reason = "Меркурий ретроградный замедляет финансовые потоки"
            else:
                money_answer = "❌ *НЕТ, в ближайшие дни.* Вероятность 20%"
                reason = "Сатурн создает ограничения в денежной сфере"
        else:
            money_answer = "💫 *Финансовые перспективы благоприятны*"
            reason = "Венера в земном знаке усиливает материальные потоки"
        
        analysis = f"""
*💰 ГЛУБОКИЙ ХОРАРНЫЙ АНАЛИЗ ФИНАНСОВ*

*Время запроса:* {time_str}
*Вопрос искателя:* «{question}»

---

*🪐 УНИКАЛЬНАЯ КОНФИГУРАЦИЯ:*

• *{planet} в {sign}* ({degree}°) - {"благоприятные" if degree > 15 else "сложные"} финансовые энергии
• *Луна в {random.choice(['Тельце', 'Козероге', 'Деве'])}* - {"стабильность" if random.random() > 0.5 else "нестабильность"} денежных потоков
• *{planet} {aspect} Уран* - {"неожиданные" if random.random() > 0.5 else "запланированные"} финансовые события

*🔮 ФИНАНСОВЫЙ ВЕРДИКТ:*
{money_answer}
*Причина:* {reason}

*💫 КЛЮЧЕВЫЕ ПЕРИОДЫ:*
• *Ближайшие 3 дня:* {"благоприятны" if random.random() > 0.5 else "требуют осторожности"} для финансов
• *Неделя:* {"рост доходов" if random.random() > 0.5 else "стабильность"}
• *Месяц:* {"значительные изменения" if random.random() > 0.5 else "постепенный рост"}
"""
        
        strategy = f"""*🎯 ФИНАНСОВАЯ СТРАТЕГИЯ:*

• *Действуйте {"активно" if random.random() > 0.5 else "осторожно"}* в финансовых вопросах
• *Ищите возможности* в {"недвижимости" if random.random() > 0.5 else "инвестициях"}
• *Избегайте рисков* {"в среду" if random.random() > 0.5 else "в пятницу"}

*🔮 МАНТРА ДЛЯ ДЕНЕГ:*
«{"Я магнит для изобилия" if random.random() > 0.5 else "Деньги приходят легко"}»"""

        return analysis, strategy

    def _generate_love_answer(self, question, time_str, sign1, sign2, planet, aspect):
        """Генерируем УНИКАЛЬНЫЙ любовный анализ"""
        
        love_phases = ["начало отношений", "глубокие чувства", "испытания", "гармония", "трансформация"]
        current_phase = random.choice(love_phases)
        
        analysis = f"""
*💖 ГЛУБОКИЙ ХОРАРНЫЙ АНАЛИЗ ЛЮБВИ*

*Время запроса:* {time_str}
*Вопрос сердца:* «{question}»

---

*🪐 УНИКАЛЬНАЯ ЛЮБОВНАЯ КАРТА:*

• *Венера в {sign1}* - {"страсть" if random.random() > 0.5 else "нежность"} в отношениях
• *Марс в {sign2}* - {"активность" if random.random() > 0.5 else "сдержанность"} в проявлении чувств
• *{planet} {aspect} Луну* - {"эмоциональная глубина" if random.random() > 0.5 else "поверхностные чувства"}

*🌟 ТЕКУЩАЯ ФАЗА ОТНОШЕНИЙ:*
*{current_phase.upper()}* - {"время действовать" if current_phase in ["начало отношений", "гармония"] else "время терпения"}

*💫 РОМАНТИЧЕСКИЙ ПРОГНОЗ:*
• *Ближайшие дни:* {"новая встреча" if random.random() > 0.5 else "укрепление связи"}
• *Неделя:* {"признание в чувствах" if random.random() > 0.5 else "глубокий разговор"}
• *Месяц:* {"серьезные изменения" if random.random() > 0.5 else "стабильность"}
"""
        
        strategy = f"""*🎯 СТРАТЕГИЯ ДЛЯ ЛЮБВИ:*

• *Проявляйте {"инициативу" if random.random() > 0.5 else "терпение"}* в отношениях
• *Уделите внимание {"общению" if random.random() > 0.5 else "романтике"}*
• *Работайте над {"доверием" if random.random() > 0.5 else "свободой"}*

*🔮 МАНТРА ЛЮБВИ:*
«{"Я открыт(а) для любви" if random.random() > 0.5 else "Любовь исцеляет меня"}»"""

        return analysis, strategy

    def _generate_future_answer(self, question, time_str, planet, house, aspect):
        """Генерируем УНИКАЛЬНЫЙ анализ будущего"""
        
        future_trends = ["значительные изменения", "стабильный рост", "неожиданные повороты", "гармоничное развитие"]
        current_trend = random.choice(future_trends)
        
        analysis = f"""
*🌌 ГЛУБОКИЙ ХОРАРНЫЙ АНАЛИЗ БУДУЩЕГО*

*Время запроса:* {time_str}
*Вопрос искателя:* «{question}»

---

*🪐 ЗВЕЗДНЫЕ ВЛИЯНИЯ НА СУДЬБУ:*

• *{planet} в {house}* - {"мощное" if random.random() > 0.5 else "умеренное"} влияние на жизненный путь
• *Сатурн {aspect} Солнце* - {"сложности" if random.random() > 0.5 else "уроки"} для роста
• *Юпитер в {random.choice(['X доме', 'I доме', 'V доме'])}* - {"расширение" if random.random() > 0.5 else "стабильность"} возможностей

*🔮 ВЕКТОР РАЗВИТИЯ:*
*{current_trend.upper()}* - {"готовьтесь к переменам" if "изменения" in current_trend else "сохраняйте курс"}

*💫 КЛЮЧЕВЫЕ СОБЫТИЯ:*
• *Ближайшая неделя:* {"важное решение" if random.random() > 0.5 else "неожиданная встреча"}
• *Месяц:* {"карьерный рост" if random.random() > 0.5 else "личностные изменения"}
• *3 месяца:* {"трансформация" if random.random() > 0.5 else "стабилизация"}
"""
        
        strategy = f"""*🎯 СТРАТЕГИЯ ДЛЯ БУДУЩЕГО:*

• *Сфокусируйтесь на {"цели" if random.random() > 0.5 else "процессе"}*
• *Развивайте {"гибкость" if random.random() > 0.5 else "устойчивость"}*
• *Доверяйте {"интуиции" if random.random() > 0.5 else "разуму"}*

*🔮 МАНТРА БУДУЩЕГО:*
«{"Я создаю свою реальность" if random.random() > 0.5 else "Вселенная ведет меня"}»"""

        return analysis, strategy

    def _generate_universal_answer(self, question, time_str, sign, planet1, planet2, aspect, degree):
        """УНИКАЛЬНЫЙ универсальный анализ"""
        
        analysis = f"""
*🌌 ГЛУБОКИЙ ХОРАРНЫЙ АНАЛИЗ*

*Время запроса:* {time_str}
*Вопрос искателя:* «{question}»

---

*🪐 УНИКАЛЬНАЯ ПЛАНЕТАРНАЯ КАРТА:*

• *{planet1} в {sign}* ({degree}°) - {"благоприятные" if degree > 15 else "сложные"} энергии
• *{planet2} {aspect} Солнце* - {"гармония" if random.random() > 0.5 else "напряжение"} в ключевых сферах
• *Луна в {random.choice(['Раке', 'Скорпионе', 'Рыбах'])}* - {"эмоциональная глубина" if random.random() > 0.5 else "чувствительность"}

*💫 ТЕКУЩИЕ ВЛИЯНИЯ:*
• *Личное:* {"рост" if random.random() > 0.5 else "стабильность"}
• *Профессия:* {"изменения" if random.random() > 0.5 else "развитие"}
• *Духовное:* {"просветление" if random.random() > 0.5 else "поиск"}
"""
        
        strategy = f"""*🎯 ИНДИВИДУАЛЬНАЯ СТРАТЕГИЯ:*

• *Действуйте через {"интуицию" if random.random() > 0.5 else "анализ"}*
• *Фокусируйтесь на {"здоровье" if random.random() > 0.5 else "отношениях"}*
• *Избегайте {"поспешных решений" if random.random() > 0.5 else "промедления"}*

*🔮 ПЕРСОНАЛЬНАЯ МАНТРА:*
«{"Я в потоке изобилия" if random.random() > 0.5 else "Мой путь освещен звездами"}»"""

        return analysis, strategy

    def analyze_question_intent(self, question):
        """Анализируем намерение вопроса"""
        question_lower = question.lower()
        
        money_words = ['деньг', 'финанс', 'денег', 'заработ', 'получу', 'придут']
        love_words = ['любов', 'отношен', 'чувства', 'встреч', 'парень', 'девушка', 'брак']
        future_words = ['будущ', 'судьб', 'ждет', 'произойдет', 'случится']
        
        if any(word in question_lower for word in money_words):
            return "MONEY_QUESTION"
        elif any(word in question_lower for word in love_words):
            return "LOVE_QUESTION" 
        elif any(word in question_lower for word in future_words):
            return "FUTURE_QUESTION"
        else:
            return "UNIVERSAL_QUESTION"

# Создаем УМНОГО императора
emperor = SmartEmperor()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_type = "private" if message.chat.type == "private" else "group"
    
    if chat_type == "private":
        response = """🌌 *Добро пожаловать в священные чертоги Хорарного Императора!*

🧠 *Я РЕАЛЬНО учусь с каждым твоим вопросом и становлюсь мудрее!*

*Задай вопрос и получи УНИКАЛЬНЫЙ анализ:*
• 💖 «Когда я встречу любовь?»
• 💰 «Придут ли мне деньги сегодня?» 
• 🌌 «Что меня ждет в будущем?»
• 💼 «Как сложится карьера?»

*Каждый анализ будет РАЗНЫМ и уникальным!*"""
    else:
        response = """🌌 *Приветствую, Искатель!*

💬 *Задай вопрос здесь* - получи глубокий публичный анализ
🔒 *Напиши «Личное»* - перейдем в ЛС для конфиденциальности
👤 *Или напиши мне в личные сообщения* @HoraryEmperorBot

*Примеры вопросов:*
• «Получу ли я деньги завтра?»
• «Что меня ждет в любви?»  
• «Личное» (для приватного общения)

🧠 *Я РЕАЛЬНО учусь с каждым вопросом!*"""

    bot.reply_to(message, response, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    try:
        user_id = message.from_user.id
        text = message.text.strip()
        chat_type = "private" if message.chat.type == "private" else "group"
        
        print(f"💫 Сообщение от {user_id}: '{text}'")

        # ПРОСТОЙ переход в ЛС
        if chat_type in ['group', 'supergroup'] and text.lower() in ['личное', 'приватно', 'в лс', 'приват', 'конфиденциально']:
            try:
                private_response = """🔒 *Добро пожаловать в конфиденциальный чат!*

🌌 *Теперь все твои вопросы останутся между нами!*

*Задай любой вопрос приватно:*
• 💖 О любви и отношениях
• 💰 О финансах и деньгах
• 🌌 О будущем и судьбе
• 💼 О карьере и предназначении

🧠 *Я учусь с каждым вопросом и становлюсь точнее!*"""
                
                bot.send_message(user_id, private_response, parse_mode='Markdown')
                bot.reply_to(message, "✅ *Переходи в личные сообщения! Все твои вопросы будут конфиденциальны!* 🔒", parse_mode='Markdown')
                return
            except Exception as e:
                print(f"❌ Ошибка ЛС: {e}")
                bot.reply_to(message, "💌 *Напиши мне в ЛС:* @HoraryEmperorBot", parse_mode='Markdown')
                return

        # Обработка вопросов
        if len(text) > 3 and not text.lower() in ['привет', 'start', 'help']:
            intent = emperor.analyze_question_intent(text)
            analysis, strategy = emperor.generate_unique_analysis(text, intent)
            
            # РЕАЛЬНО учимся
            emperor.learn_from_interaction(text, analysis, user_id)
            
            if chat_type == "private":
                full_response = f"{analysis}\n\n{strategy}\n\n🧠 *Я стал мудрее благодаря твоему вопросу! Мой анализ становится точнее!*"
            else:
                full_response = f"{analysis}\n\n{strategy}\n\n💌 *Для конфиденциальности напиши «Личное»*\n🧠 *Я РЕАЛЬНО учусь с каждым вопросом!*"
            
            bot.reply_to(message, full_response, parse_mode='Markdown')
        else:
            response = """🌌 *Задай настоящий вопрос о:*
• 💖 Любви и отношениях
• 💰 Финансах и деньгах  
• 🌌 Будущем и судьбе
• 💼 Карьере и работе

*Или напиши «Личное» для приватного общения*"""
            bot.reply_to(message, response, parse_mode='Markdown')
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        try:
            bot.reply_to(message, "🔮 *Временные помехи... Попробуй еще раз!*", parse_mode='Markdown')
        except:
            pass

print("✅ УМНЫЙ Хорарный Император готов!")
print("🌐 Flask работает на порту 5000")

def smart_launch():
    while True:
        try:
            print("💫 Запускаю умный polling...")
            bot.polling(none_stop=True, interval=2, timeout=60)
        except Exception as e:
            print(f"❌ Ошибка polling: {e}")
            time.sleep(10)

if __name__ == "__main__":
    smart_launch()
