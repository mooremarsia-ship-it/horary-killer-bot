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

class ProfessionalAstrologer:
    def __init__(self):
        self.experience = 0
        self.waiting_for_clarification = {}
    
    def analyze_question_type(self, question):
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['деньг', 'финанс', 'придут', 'зарплат', 'преми', 'долг', 'вернут', 'кредит']):
            return "ФИНАНСЫ", "💰"
        elif any(word in question_lower for word in ['любит', 'отношен', 'брак', 'замуж', 'встреч', 'парень', 'мужчин', 'девушк', 'чувств', 'влюблен']):
            return "ОТНОШЕНИЯ", "💖" 
        elif any(word in question_lower for word in ['здоров', 'болез', 'лечен', 'врач', 'больниц', 'самочувств', 'анализ', 'диагноз']):
            return "ЗДОРОВЬЕ", "🏥"
        elif any(word in question_lower for word in ['работ', 'карьер', 'должност', 'бизнес', 'проект', 'начальник', 'устроюсь']):
            return "КАРЬЕРА", "🚀"
        elif any(word in question_lower for word in ['поезд', 'путешеств', 'переезд', 'отпуск']):
            return "ПУТЕШЕСТВИЯ", "✈️"
        else:
            return "ОБЩИЙ", "🔮"
    
    def generate_professional_analysis(self, question, moon_sign, sun_sign, question_type, user_id=None):
        """ПРОФЕССИОНАЛЬНЫЙ астрологический анализ"""
        
        if len(question.strip()) < 5 or question.lower() in ['император', 'бот', 'привет']:
            return self._get_greeting_response(moon_sign, sun_sign)
        
        # Если вопрос слишком общий
        if self._is_too_general(question):
            if user_id:
                self.waiting_for_clarification[user_id] = question_type
            return self._ask_for_clarification(question_type, moon_sign, sun_sign)
        
        # ПРОФЕССИОНАЛЬНЫЙ АНАЛИЗ
        return self._get_professional_reading(question, moon_sign, sun_sign, question_type)
    
    def _is_too_general(self, question):
        """Проверяет общие вопросы"""
        question_lower = question.lower()
        too_general = [
            'вопрос про деньги', 'про финансы', 'про отношения', 
            'про работу', 'про здоровье', 'про карьеру', 'про это'
        ]
        return any(pattern in question_lower for pattern in too_general)
    
    def _ask_for_clarification(self, question_type, moon_sign, sun_sign):
        """Просит уточнить вопрос профессионально"""
        
        clarifications = {
            "ФИНАНСЫ": [
                f"💎 *Профессиональный хорарный анализ требует точности*\n\n"
                f"Луна в {moon_sign} готова к анализу, но нужны детали:\n\n"
                f"• *Конкретные суммы и сроки:* 'Придут ли 5000 руб до пятницы?'\n"
                f"• *Источник денег:* 'Получу ли зарплату/премию/возврат долга?'\n"  
                f"• *Финансовые решения:* 'Стоит ли инвестировать в этот проект?'",
            ],
            "ОТНОШЕНИЯ": [
                f"💖 *Глубинный анализ отношений требует фокуса*\n\n"
                f"Солнце в {sun_sign} готово раскрыть карты судьбы:\n\n"
                f"• *Конкретный человек:* 'Любит ли меня Дмитрий?'\n"
                f"• *Ситуация:* 'Вернется ли ко мне бывший парень?'\n"
                f"• *Будущее:* 'Будет ли у нас брак/будущее вместе?'"
            ],
            "ЗДОРОВЬЕ": [
                f"🏥 *Медицинская астрология требует конкретики*\n\n"
                f"Луна в {moon_sign} готова к диагностике:\n\n"
                f"• *Симптомы/состояние:* 'Поправлюсь ли от простуды за неделю?'\n"
                f"• *Лечение:* 'Поможет ли мне это лечение/врач?'\n"
                f"• *Профилактика:* 'Что укрепит мое здоровье?'"
            ]
        }
        
        default_msg = f"🔮 Луна в {moon_sign} и Солнце в {sun_sign} готовы к анализу! Задай конкретный вопрос для профессионального ответа."
        
        options = clarifications.get(question_type, [default_msg])
        verdict = "🎯"
        analysis = random.choice(options)
        strategy = "Уточни вопрос - и получи развернутый астрологический анализ!"
        
        return verdict, analysis, strategy
    
    def _get_professional_reading(self, question, moon_sign, sun_sign, question_type):
        """ПРОФЕССИОНАЛЬНЫЙ разбор вопроса"""
        
        if question_type == "ФИНАНСЫ":
            return self._financial_horary_analysis(question, moon_sign, sun_sign)
        elif question_type == "ОТНОШЕНИЯ":
            return self._relationship_horary_analysis(question, moon_sign, sun_sign)
        elif question_type == "ЗДОРОВЬЕ":
            return self._health_horary_analysis(question, moon_sign, sun_sign)
        elif question_type == "КАРЬЕРА":
            return self._career_horary_analysis(question, moon_sign, sun_sign)
        else:
            return self._general_horary_analysis(question, moon_sign, sun_sign)
    
    def _financial_horary_analysis(self, question, moon_sign, sun_sign):
        """ПРОФЕССИОНАЛЬНЫЙ финансовый анализ"""
        
        question_lower = question.lower()
        current_time = datetime.now(timezone.utc) + timedelta(hours=3)
        time_str = current_time.strftime('%H:%M, %d %B %Y')
        
        # АНАЛИЗ КАРТЫ
        analysis_text = f"""
*Астрологический анализ*

*Время:* {time_str}
*Вопрос:* «{question}»

---

*Карта вопроса:*

• *Ты (1-й дом):* в {self._get_rising_sign()} 
• *Управитель — {self._get_ruler()}* в {random.randint(1, 30)}° {self._get_sign()}

• *Твои деньги (2-й дом):* в {self._get_second_house()} 
• *Управитель — {self._get_money_ruler()}* в {random.randint(1, 30)}° {self._get_sign()}

• *Общий сигнификатор денег:* 
  · Луна в {moon_sign}
  · Солнце в {sun_sign}

---

*Ключевые аспекты:*
"""
        
        # ДИНАМИЧЕСКИЙ АНАЛИЗ ПО ТИПУ ВОПРОСА
        if any(word in question_lower for word in ['придут', 'получу', 'когда']):
            analysis_text += self._analyze_money_timing(moon_sign, sun_sign)
        elif any(word in question_lower for word in ['долг', 'вернут']):
            analysis_text += self._analyze_debt_return(moon_sign, sun_sign)
        elif any(word in question_lower for word in ['инвест', 'вложен']):
            analysis_text += self._analyze_investment(moon_sign, sun_sign)
        else:
            analysis_text += self._analyze_general_finance(moon_sign, sun_sign)
        
        analysis_text += f"\n---\n*Вердикт:*\n\n{self._get_finance_verdict(moon_sign, sun_sign, question_lower)}"
        
        verdict = self._get_finance_verdict_symbol(moon_sign, sun_sign)
        strategy = self._get_finance_strategy(moon_sign)
        
        return verdict, analysis_text, strategy
    
    def _relationship_horary_analysis(self, question, moon_sign, sun_sign):
        """ПРОФЕССИОНАЛЬНЫЙ анализ отношений"""
        
        current_time = datetime.now(timezone.utc) + timedelta(hours=3)
        time_str = current_time.strftime('%H:%M, %d %B %Y')
        
        analysis_text = f"""
*Астрологический анализ отношений*

*Время:* {time_str}  
*Вопрос:* «{question}»

---

*Карта отношений:*

• *Ты (1-й дом):* в {self._get_rising_sign()}
• *Управитель — {self._get_ruler()}* в {random.randint(1, 30)}° {self._get_sign()}

• *Партнер (7-й дом):* в {self._get_partner_house()}
• *Управитель — {self._get_partner_ruler()}* в {random.randint(1, 30)}° {self._get_sign()}

• *Эмоциональная связь:* 
  · Луна в {moon_sign}
  · Венера в {self._get_venus_sign()}

---

*Ключевые аспекты:*
"""
        
        question_lower = question.lower()
        if 'любит' in question_lower:
            analysis_text += self._analyze_love_feelings(moon_sign, sun_sign)
        elif 'вернет' in question_lower or 'вернется' in question_lower:
            analysis_text += self._analyze_ex_return(moon_sign, sun_sign)
        elif 'будущее' in question_lower or 'брак' in question_lower:
            analysis_text += self._analyze_relationship_future(moon_sign, sun_sign)
        else:
            analysis_text += self._analyze_general_relationship(moon_sign, sun_sign)
        
        analysis_text += f"\n---\n*Вердикт:*\n\n{self._get_relationship_verdict(moon_sign, sun_sign, question_lower)}"
        
        verdict = self._get_relationship_verdict_symbol(moon_sign, sun_sign)
        strategy = self._get_relationship_strategy(moon_sign)
        
        return verdict, analysis_text, strategy
    
    def _health_horary_analysis(self, question, moon_sign, sun_sign):
        """ПРОФЕССИОНАЛЬНЫЙ анализ здоровья"""
        
        current_time = datetime.now(timezone.utc) + timedelta(hours=3)
        time_str = current_time.strftime('%H:%M, %d %B %Y')
        
        analysis_text = f"""
*Медицинский астрологический анализ*

*Время:* {time_str}
*Вопрос:* «{question}»

---

*Карта здоровья:*

• *Ты (1-й дом):* в {self._get_rising_sign()}
• *Управитель — {self._get_ruler()}* в {random.randint(1, 30)}° {self._get_sign()}

• *Здоровье (6-й дом):* в {self._get_health_house()}
• *Управитель — {self._get_health_ruler()}* в {random.randint(1, 30)}° {self._get_sign()}

• *Общее состояние:* 
  · Луна в {moon_sign}
  · Солнце в {sun_sign}

---

*Ключевые аспекты:*
"""
        
        analysis_text += self._analyze_health_aspects(moon_sign, sun_sign)
        analysis_text += f"\n---\n*Вердикт:*\n\n{self._get_health_verdict(moon_sign, sun_sign)}"
        
        verdict = self._get_health_verdict_symbol(moon_sign, sun_sign)
        strategy = self._get_health_strategy(moon_sign)
        
        return verdict, analysis_text, strategy
    
    def _analyze_money_timing(self, moon_sign, sun_sign):
        """Анализ времени прихода денег"""
        aspects = []
        
        if moon_sign in ['Телец', 'Рак', 'Козерог']:
            aspects.append(f"· Луна в {moon_sign} — благоприятный знак для финансов. Деньги могут прийти в течение 3-7 дней.")
        else:
            aspects.append(f"· Луна в {moon_sign} — возможны небольшие задержки. Ожидайте поступления в течение 1-2 недель.")
        
        if sun_sign in ['Лев', 'Стрелец']:
            aspects.append(f"· Солнце в {sun_sign} — указывает на неожиданные источники дохода или дополнительные возможности.")
        else:
            aspects.append(f"· Солнце в {sun_sign} — стабильный, но не быстрый финансовый поток.")
        
        aspects.append("· Управитель 2-го дома ретроградный — возможны задержки из-за документов или согласований.")
        aspects.append("· Отсутствие аспектов между управителями — деньги в пути, но требуют терпения.")
        
        return "\n".join(aspects)
    
    def _analyze_love_feelings(self, moon_sign, sun_sign):
        """Анализ чувств партнера"""
        aspects = []
        
        if moon_sign in ['Рак', 'Телец', 'Рыбы']:
            aspects.append(f"· Луна в {moon_sign} — глубокие эмоциональные чувства присутствуют. Партнер испытывает привязанность.")
        else:
            aspects.append(f"· Луна в {moon_sign} — эмоции есть, но могут быть скрыты или не до конца осознаны.")
        
        if sun_sign in ['Лев', 'Скорпион']:
            aspects.append(f"· Солнце в {sun_sign} — сильная воля и интерес. Партнер видит в тебе значимую фигуру.")
        else:
            aspects.append(f"· Солнце в {sun_sign} — устойчивый, но не интенсивный интерес.")
        
        aspects.append("· Венера делает аспект к управителю 7-го дома — симпатия и влечение присутствуют.")
        aspects.append("· Марс в огненном знаке — активное проявление чувств возможно в ближайшее время.")
        
        return "\n".join(aspects)
    
    def _analyze_health_aspects(self, moon_sign, sun_sign):
        """Анализ аспектов здоровья"""
        aspects = []
        
        if moon_sign in ['Рак', 'Дева', 'Козерог']:
            aspects.append(f"· Луна в {moon_sign} — организм обладает хорошими восстановительными способностями.")
        else:
            aspects.append(f"· Луна в {moon_sign} — возможны колебания в самочувствии. Важен режим.")
        
        if sun_sign in ['Овен', 'Лев']:
            aspects.append(f"· Солнце в {sun_sign} — высокий жизненный тонус, но риск переутомления.")
        else:
            aspects.append(f"· Солнце в {sun_sign} — стабильная энергия, организм в норме.")
        
        aspects.append("· Управитель 6-го дома в сильном положении — иммунная система функционирует хорошо.")
        aspects.append("· Отсутствие напряженных аспектов к управителю 1-го дома — серьезных угроз здоровью нет.")
        
        return "\n".join(aspects)
    
    def _get_finance_verdict(self, moon_sign, sun_sign, question_lower):
        """Вердикт по финансам"""
        if 'сегодня' in question_lower:
            if moon_sign in ['Телец', 'Рак']:
                return "На основании карты, получение денег сегодня ВОЗМОЖНО. Луна в благоприятном положении указывает на движение финансовых потоков."
            else:
                return "На основании карты, получение денег сегодня МАЛОВЕРОЯТНО. Ретроградный управитель 2-го дома указывает на задержки."
        else:
            if moon_sign in ['Телец', 'Козерог', 'Скорпион']:
                return "Финансовые перспективы БЛАГОПРИЯТНЫ. Деньги придут в ожидаемые сроки."
            else:
                return "Финансовые потоки требуют ТЕРПЕНИЯ. Возможны небольшие задержки из-за внешних обстоятельств."
    
    def _get_relationship_verdict(self, moon_sign, sun_sign, question_lower):
        """Вердикт по отношениям"""
        if 'любит' in question_lower:
            if moon_sign in ['Рак', 'Рыбы', 'Телец']:
                return "Чувства ПРИСУТСТВУЮТ и имеют глубокую эмоциональную основу. Луна в водном/земном знаке указывает на искреннюю привязанность."
            else:
                return "Интерес есть, но эмоциональная глубина требует времени для раскрытия. Дайте отношениям развиваться естественно."
        
        return "Отношения имеют потенциал для развития. Ключевой фактор — время и взаимные усилия."
    
    def _get_health_verdict(self, moon_sign, sun_sign):
        """Вердикт по здоровью"""
        if moon_sign in ['Рак', 'Дева', 'Козерог']:
            return "Общее состояние здоровья ХОРОШЕЕ. Организм обладает ресурсами для восстановления и поддержания баланса."
        else:
            return "Состояние в норме, но требуются профилактические меры. Обратите внимание на режим и эмоциональный фон."
    
    # Вспомогательные методы для генерации случайных астрологических данных
    def _get_rising_sign(self):
        signs = ['Овне', 'Тельце', 'Близнецах', 'Раке', 'Льве', 'Деве', 'Весах', 'Скорпионе', 'Стрельце', 'Козероге', 'Водолее', 'Рыбах']
        return random.choice(signs)
    
    def _get_ruler(self):
        rulers = ['Марс', 'Венера', 'Меркурий', 'Луна', 'Солнце', 'Меркурий', 'Венера', 'Марс', 'Юпитер', 'Сатурн', 'Уран', 'Нептун']
        return random.choice(rulers)
    
    def _get_sign(self):
        signs = ['Овна', 'Тельца', 'Близнецов', 'Рака', 'Льва', 'Девы', 'Весов', 'Скорпиона', 'Стрельца', 'Козерога', 'Водолея', 'Рыб']
        return random.choice(signs)
    
    def _get_second_house(self):
        return self._get_rising_sign()
    
    def _get_money_ruler(self):
        return self._get_ruler()
    
    def _get_partner_house(self):
        return self._get_rising_sign()
    
    def _get_partner_ruler(self):
        return self._get_ruler()
    
    def _get_venus_sign(self):
        return self._get_sign()
    
    def _get_health_house(self):
        return self._get_rising_sign()
    
    def _get_health_ruler(self):
        return self._get_ruler()
    
    def _get_finance_verdict_symbol(self, moon_sign, sun_sign):
        if moon_sign in ['Телец', 'Рак', 'Козерог']:
            return "💰"
        else:
            return "⏳"
    
    def _get_relationship_verdict_symbol(self, moon_sign, sun_sign):
        if moon_sign in ['Рак', 'Телец', 'Рыбы']:
            return "💖"
        else:
            return "🤔"
    
    def _get_health_verdict_symbol(self, moon_sign, sun_sign):
        if moon_sign in ['Рак', 'Дева', 'Козерог']:
            return "💪"
        else:
            return "🏥"
    
    def _get_finance_strategy(self, moon_sign):
        strategies = [
            "Проверьте все финансовые каналы на этой неделе",
            "Составьте детальный план распределения средств",
            "Проявите терпение - деньги в пути"
        ]
        return random.choice(strategies)
    
    def _get_relationship_strategy(self, moon_sign):
        strategies = [
            "Дайте отношениям развиваться естественно",
            "Проявляйте искренность, но сохраняйте достоинство",
            "Слушайте сердце, но не игнорируйте разум"
        ]
        return random.choice(strategies)
    
    def _get_health_strategy(self, moon_sign):
        strategies = [
            "Соблюдайте режим сна и отдыха",
            "Включите в рацион больше витаминов",
            "Регулярные прогулки укрепят здоровье"
        ]
        return random.choice(strategies)
    
    def _get_greeting_response(self, moon_sign, sun_sign):
        responses = [
            f"👑 *Профессиональный Хорарный Император к вашим услугам!*\n\nЗадайте вопрос о финансах, отношениях, здоровье или карьере для глубинного астрологического анализа.",
            f"🔮 *Глубинный астрологический анализ готов!*\n\nЛуна в {moon_sign} и Солнце в {sun_sign} ждут вашего вопроса.",
        ]
        verdict = "👑"
        analysis = random.choice(responses)
        strategy = "Задайте конкретный вопрос для профессионального разбора"
        return verdict, analysis, strategy
    
    # Заглушки для остальных методов анализа
    def _analyze_debt_return(self, moon_sign, sun_sign):
        aspects = [
            f"· Луна в {moon_sign} — возврат долга вероятен, но требует времени.",
            "· Управитель 2-го дома делает аспект к управителю 8-го — долг будет возвращен.",
            "· Отсутствие напряженных аспектов — конфликтов по поводу долга удастся избежать."
        ]
        return "\n".join(aspects)
    
    def _analyze_investment(self, moon_sign, sun_sign):
        aspects = [
            f"· Солнце в {sun_sign} — инвестиция имеет потенциал для роста.",
            "· Управитель 2-го дома в сильном положении — финансовые риски минимальны.",
            "· Луна делает благоприятный аспект — эмоционально это верное решение."
        ]
        return "\n".join(aspects)
    
    def _analyze_general_finance(self, moon_sign, sun_sign):
        aspects = [
            f"· Луна в {moon_sign} — эмоциональное отношение к деньгам стабильное.",
            f"· Солнце в {sun_sign} — финансовая энергия на хорошем уровне.",
            "· Общая картина показывает устойчивое положение."
        ]
        return "\n".join(aspects)
    
    def _analyze_ex_return(self, moon_sign, sun_sign):
        aspects = [
            f"· Луна в {moon_sign} — эмоциональная связь еще присутствует.",
            "· Управитель 7-го дома ретроградный — возможен возврат к прошлому.",
            "· Венера делает аспект к управителю 1-го дома — притяжение сохранилось."
        ]
        return "\n".join(aspects)
    
    def _analyze_relationship_future(self, moon_sign, sun_sign):
        aspects = [
            f"· Луна в {moon_sign} — эмоциональный фундамент для будущего есть.",
            "· Солнце в сильном положении — отношения имеют потенциал роста.",
            "· Управители домов в гармонии — совместимость на хорошем уровне."
        ]
        return "\n".join(aspects)
    
    def _analyze_general_relationship(self, moon_sign, sun_sign):
        aspects = [
            f"· Луна в {moon_sign} — текущее эмоциональное состояние стабильное.",
            f"· Солнце в {sun_sign} — энергия отношений на хорошем уровне.",
            "· Общая картина показывает гармоничное развитие."
        ]
        return "\n".join(aspects)
    
    def _career_horary_analysis(self, question, moon_sign, sun_sign):
        return self._general_horary_analysis(question, moon_sign, sun_sign)
    
    def _general_horary_analysis(self, question, moon_sign, sun_sign):
        current_time = datetime.now(timezone.utc) + timedelta(hours=3)
        time_str = current_time.strftime('%H:%M, %d %B %Y')
        
        analysis_text = f"""
*Общий астрологический анализ*

*Время:* {time_str}
*Вопрос:* «{question}»

---

*Карта вопроса:*

• *1-й дом (Ты):* в {self._get_rising_sign()}
• *Управитель — {self._get_ruler()}* в {random.randint(1, 30)}° {self._get_sign()}

• *Соответствующий дом вопроса:* в благоприятном положении
• *Общие сигнификаторы:* 
  · Луна в {moon_sign}
  · Солнце в {sun_sign}

---

*Ключевые аспекты:*

· Луна в {moon_sign} — эмоциональный фон стабильный
· Солнце в {sun_sign} — волевая энергия на хорошем уровне  
· Управитель вопроса в сильном положении — ситуация развивается благоприятно

---

*Вердикт:*

На основании карты, ситуация имеет ПОЗИТИВНУЮ динамику. 
Текущие энергетические потоки поддерживают ваши намерения.
"""
        
        verdict = "🌟"
        strategy = "Продолжайте действовать в выбранном направлении"
        
        return verdict, analysis_text, strategy

# Создаем экземпляр астролога
astrologer = ProfessionalAstrologer()

def get_moscow_time():
    utc_time = datetime.now(timezone.utc)
    moscow_time = utc_time + timedelta(hours=3)
    return moscow_time.strftime('%H:%M, %d.%m.%Y')

def get_random_zodiac():
    signs = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 
             'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']
    return random.choice(signs)

# УМНАЯ ОБРАБОТКА ГРУПП с АВТОПРИГЛАШЕНИЕМ В ЛС
@bot.message_handler(chat_types=['supergroup', 'group'])
def handle_group_message(message):
    try:
        if message.text:
            question = None
            
            # 🎯 АВТОМАТИЧЕСКОЕ ПРИГЛАШЕНИЕ В ЛС при упоминании
            if '@HoraryEmperorBot' in message.text:
                bot_text = message.text.replace('@HoraryEmperorBot', '').strip()
                
                if not bot_text or len(bot_text) < 3:
                    # Пытаемся отправить приглашение в ЛС
                    try:
                        welcome_msg = """
💫 *ДОБРО ПОЖАЛОВАТЬ В КОНФИДЕНЦИАЛЬНЫЙ АНАЛИЗ!*

🔒 *Ваши вопросы защищены полной конфиденциальностью*

*Задайте вопрос о:*
• 💰 Финансах и денежных потоках
• 💖 Отношениях и чувствах  
• 🏥 Здоровье и самочувствии
• 🚀 Карьере и профессиональном росте

*Примеры конфиденциальных вопросов:*
• «Придут ли мне деньги до пятницы?»
• «Любит ли меня этот человек?»
• «Получу ли я эту работу?»

✨ *Ваша тайна в безопасности!*
"""
                        bot.send_message(message.from_user.id, welcome_msg)
                        bot.reply_to(message, "📨 *Приглашение в личные сообщения отправлено! Задайте вопрос конфиденциально!*")
                    except Exception as e:
                        # Если не получается в ЛС, показываем приглашение в группе
                        group_invite = """
🔒 *КОНФИДЕНЦИАЛЬНЫЙ ПРОФЕССИОНАЛЬНЫЙ АНАЛИЗ*

*Для полной конфиденциальности:* 
💌 *Напишите мне в ЛИЧНЫЕ СООБЩЕНИЯ* - @HoraryEmperorBot

*Или используйте варианты:*
• Напишите "Личное [ваш вопрос]" - отвечу здесь
• Задайте вопрос прямо здесь - публичный ответ

✨ *Ваша тайна в безопасности!*
"""
                        bot.reply_to(message, group_invite)
                    return
                
                if bot_text.lower().startswith('личное'):
                    question = bot_text.replace('личное', '').strip()
                    if question:
                        try:
                            analysis = get_detailed_analysis(question)
                            private_msg = f"🔒 *ЛИЧНЫЙ ПРОФЕССИОНАЛЬНЫЙ АНАЛИЗ*\n\n{analysis}"
                            bot.send_message(message.from_user.id, private_msg)
                            bot.reply_to(message, "📨 *Конфиденциальный анализ отправлен в ваши личные сообщения!*")
                        except:
                            bot.reply_to(message, "❌ *Для конфиденциального анализа напишите мне в ЛС: @HoraryEmperorBot*")
                    return
                else:
                    question = bot_text
            
            # 🎯 ОБРАБОТКА ПРЯМЫХ ОБРАЩЕНИЙ
            elif message.text.lower() in ['император', 'бот', 'император?', 'бот?', 'астролог']:
                help_text = """
👑 *ПРОФЕССИОНАЛЬНЫЙ ХОРАРНЫЙ ИМПЕРАТОР*

*Для КОНФИДЕНЦИАЛЬНОГО анализа:*
💌 Напишите мне в ЛС - @HoraryEmperorBot

*Публичные варианты:*
• Напишите "Личное [вопрос]" - отвечу здесь
• Задайте вопрос прямо в чате

*Анализирую:* 💰 Финансы • 💖 Отношения • 🏥 Здоровье • 🚀 Карьера
"""
                bot.reply_to(message, help_text)
                return
            
            # 🔒 ОБРАБОТКА "ЛИЧНОЕ"
            elif message.text.lower().startswith('личное'):
                question = message.text.replace('личное', '').strip()
                if question:
                    try:
                        analysis = get_detailed_analysis(question)
                        private_msg = f"🔒 *ЛИЧНЫЙ АНАЛИЗ*\n\n{analysis}"
                        bot.send_message(message.from_user.id, private_msg)
                        bot.reply_to(message, "📨 *Конфиденциальный анализ отправлен в личные сообщения!*")
                    except:
                        invitation = "💌 *Для конфиденциального анализа напишите мне в ЛС:* @HoraryEmperorBot"
                        bot.reply_to(message, invitation)
                return
            
            # 📊 ПУБЛИЧНЫЙ АНАЛИЗ
            elif '?' in message.text and len(message.text) > 10:
                question = message.text.strip()
            
            if question and len(question) > 5:
                analysis = get_detailed_analysis(question)
                
                # Добавляем приглашение в ЛС к публичному ответу
                analysis_with_invite = analysis + "\n\n💌 *Для конфиденциальных вопросов - пишите в личные сообщения*"
                bot.reply_to(message, analysis_with_invite)
                
    except Exception as e:
        print(f"Ошибка в группе: {e}")

# ЛИЧНЫЕ СООБЩЕНИЯ - ПОЛНЫЙ ПРОФЕССИОНАЛЬНЫЙ АНАЛИЗ
@bot.message_handler(func=lambda message: True, chat_types=['private'])
def handle_private_message(message):
    if message.text.startswith('/'):
        if message.text == '/start':
            start_text = """
🔮 *ПРОФЕССИОНАЛЬНЫЙ ХОРАРНЫЙ ИМПЕРАТОР*

*Глубинный КОНФИДЕНЦИАЛЬНЫЙ астрологический анализ*

💫 *Ваши вопросы остаются между нами!*

*Я анализирую:*
• 💰 *Финансы* — придут ли деньги, вернут ли долг, окупятся ли инвестиции
• 💖 *Отношения* — любит ли человек, будет ли будущее, вернется ли партнер  
• 🏥 *Здоровье* — поправлюсь ли, поможет ли лечение, что укрепит здоровье
• 🚀 *Карьера* — устроюсь ли на работу, будет ли повышение, успешен ли проект

*Задайте конкретный вопрос для профессионального разбора!*
"""
            bot.reply_to(message, start_text)
        return
    
    try:
        if len(message.text.strip()) < 5 or message.text.lower().strip() in ['император', 'бот', 'привет']:
            responses = [
                "👑 *Задайте вопрос для конфиденциального астрологического анализа!*",
                "🔮 *Что вас волнует? Финансы, отношения, здоровье? Ваша тайна в безопасности!*",
                "💫 *Готов к глубинной астрологической диагностике вашей ситуации! Конфиденциально!*"
            ]
            bot.reply_to(message, random.choice(responses))
            return
        
        display_time = get_moscow_time()
        moon_sign = get_random_zodiac()
        sun_sign = get_random_zodiac()
        
        question_type, emoji = astrologer.analyze_question_type(message.text)
        
        user_id = message.from_user.id
        if user_id in astrologer.waiting_for_clarification:
            question_type = astrologer.waiting_for_clarification[user_id]
            del astrologer.waiting_for_clarification[user_id]
            
            verdict, analysis, strategy = astrologer._get_professional_reading(
                message.text, moon_sign, sun_sign, question_type
            )
        else:
            verdict, analysis, strategy = astrologer.generate_professional_analysis(
                message.text, moon_sign, sun_sign, question_type, user_id
            )
        
        response = f"""
{verdict} *КОНФИДЕНЦИАЛЬНЫЙ ПРОФЕССИОНАЛЬНЫЙ АНАЛИЗ*
⏰ {display_time}, МОСКВА
🔒 *Ваш вопрос защищен*

{analysis}

🎯 *Рекомендация:* {strategy}

✨ Уровень анализа: {astrologer.experience + 1}
💫 Благодарю за доверие!
"""
        bot.reply_to(message, response)
        astrologer.experience += 1
        
    except Exception as e:
        bot.reply_to(message, f"❌ *Ошибка анализа:* {str(e)}")

def get_detailed_analysis(question):
    """Функция для анализа в группах"""
    display_time = get_moscow_time()
    moon_sign = get_random_zodiac()
    sun_sign = get_random_zodiac()
    
    question_type, emoji = astrologer.analyze_question_type(question)
    verdict, analysis, strategy = astrologer.generate_professional_analysis(
        question, moon_sign, sun_sign, question_type
    )
    
    return f"""
{verdict} *ПРОФЕССИОНАЛЬНЫЙ АНАЛИЗ*
⏰ {display_time}

{analysis}

🎯 *Рекомендация:* {strategy}

✨ @HoraryEmperorBot
"""

print("🔄 ПРОФЕССИОНАЛЬНЫЙ ХОРАРНЫЙ ИМПЕРАТОР запущен...")
print("🌐 HTTP-сервер здоровья работает на порту 5000")

# 🔧 Стабильный запуск
try:
    print("🔗 Подключаемся к Telegram...")
    time.sleep(5)
    bot.remove_webhook()
    print("✅ Webhook удален")
    time.sleep(2)
    print("🔄 Запускаем polling...")
    bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
except Exception as e:
    print(f"❌ Ошибка подключения: {e}")
    print("🔄 Перезапуск через 15 секунд...")
    time.sleep(15)
