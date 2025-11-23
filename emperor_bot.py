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
        self.waiting_for_clarification = {}  # Для отслеживания уточнений
    
    def analyze_question_type(self, question):
        question_lower = question.lower()
        if any(word in question_lower for word in ['деньг', 'финанс', 'денег', 'рубл', 'евро', 'доллар', 'зарплат', 'преми', 'долг', 'кредит']):
            return "ФИНАНСЫ", "💰"
        elif any(word in question_lower for word in ['любит', 'скуч', 'отношен', 'брак', 'замуж', 'встреч', 'парень', 'мужчин', 'девушк', 'чувств', 'любов', 'сердц']):
            return "ОТНОШЕНИЯ", "💖" 
        elif any(word in question_lower for word in ['работ', 'карьер', 'должност', 'бизнес', 'проект', 'начальник', 'коллег', 'офис', 'зарплат']):
            return "КАРЬЕРА", "🚀"
        elif any(word in question_lower for word in ['здоров', 'болез', 'лечен', 'врач', 'больниц', 'самочувств', 'анализ', 'диагноз']):
            return "ЗДОРОВЬЕ", "🏥"
        elif any(word in question_lower for word in ['поезд', 'путешеств', 'переезд', 'отпуск', 'билет', 'отдых']):
            return "ПУТЕШЕСТВИЯ", "✈️"
        else:
            return "ОБЩИЙ", "🔮"
    
    def generate_smart_response(self, question, moon_sign, sun_sign, question_type, user_id=None):
        """УМНЫЙ анализ с ДИАЛОГОВОСТЬЮ"""
        
        # Если вопрос слишком короткий или просто обращение
        if len(question.strip()) < 5 or question.lower() in ['император', 'бот', 'привет']:
            return self._get_greeting_response(moon_sign, sun_sign)
        
        # ЕСЛИ ВОПРОС СЛИШКОМ ОБЩИЙ - ПРОСИМ УТОЧНИТЬ
        if self._is_too_general(question):
            if user_id:
                self.waiting_for_clarification[user_id] = question_type
            return self._ask_for_clarification(question_type, moon_sign, sun_sign)
        
        # ДЕТАЛЬНЫЙ АНАЛИЗ КОНКРЕТНОГО ВОПРОСА
        return self._get_detailed_analysis(question, moon_sign, sun_sign, question_type)
    
    def _is_too_general(self, question):
        """Проверяет, слишком ли общий вопрос"""
        question_lower = question.lower()
        
        too_general_patterns = [
            'вопрос про деньги', 'про финансы', 'про отношения', 
            'про работу', 'про здоровье', 'про карьеру',
            'про путешествия', 'про поездку', 'про любовь',
            'что с деньгами', 'что в отношениях', 'как с работой',
            'про это', 'про то', 'насчет денег', 'насчет отношений'
        ]
        
        return any(pattern in question_lower for pattern in too_general_patterns)
    
    def _ask_for_clarification(self, question_type, moon_sign, sun_sign):
        """Просит уточнить вопрос"""
        
        clarifications = {
            "ФИНАНСЫ": [
                f"🔮 Луна в {moon_sign} хочет знать подробнее! Уточни:\n• Получу ли я деньги до конца месяца?\n• Вернут ли мне долг?\n• Стоит ли делать эту покупку?\n• Повысят ли мне зарплату?",
                f"💰 Солнце в {sun_sign} ждет деталей! Например:\n• Когда придут ожидаемые деньги?\n• Стоит ли инвестировать в этот проект?\n• Будет ли прибыль от вложений?\n• Стоит ли брать кредит?"
            ],
            "ОТНОШЕНИЯ": [
                f"💖 {moon_sign} чувствует, что нужно уточнить! Спроси:\n• Любит ли меня этот человек?\n• Вернется ли ко мне бывший?\n• Стоит ли начинать новые отношения?\n• Будет ли у нас будущее?",
                f"✨ {sun_sign} хочет понять суть! Например:\n• Изменяет ли мне партнер?\n• Когда я встречу свою судьбу?\n• Стоит ли прощать его?\n• Почему он так себя ведет?"
            ],
            "КАРЬЕРА": [
                f"🚀 {moon_sign} советует конкретику! Уточни:\n• Устроюсь ли я на эту работу?\n• Стоит ли менять профессию?\n• Получу ли я повышение?\n• Будет ли успешен мой проект?",
                f"🌟 {sun_sign} ждет ясности! Например:\n• Стоит ли соглашаться на предложение?\n• Когда ждать карьерного роста?\n• Правильно ли я выбрал профессию?\n• Стоит ли увольняться?"
            ],
            "ЗДОРОВЬЕ": [
                f"🏥 {moon_sign} заботится о твоем здоровье! Уточни:\n• Поправлюсь ли я скоро?\n• Правильное ли лечение мне назначили?\n• Стоит ли делать операцию?\n• Когда наступит улучшение?",
                f"💊 {sun_sign} хочет помочь! Например:\n• Эффективно ли это лекарство?\n• Стоит ли менять врача?\n• Какие анализы нужно сдать?\n• Когда пройдут симптомы?"
            ],
            "ПУТЕШЕСТВИЯ": [
                f"✈️ {moon_sign} готов к путешествиям! Уточни:\n• Стоит ли ехать в эту поездку?\n• Будет ли путешествие удачным?\n• Когда лучше ехать?\n• С кем стоит путешествовать?",
                f"🌍 {sun_sign} ждет маршрут! Например:\n• Безопасна ли эта страна?\n• Стоит ли покупать билеты сейчас?\n• Какие места посетить?\n• Будет ли хорошая погода?"
            ]
        }
        
        default_clarification = f"🔮 Луна в {moon_sign} и Солнце в {sun_sign} хотят понять тебя лучше! Задай конкретный вопрос - и я дам точный ответ!"
        
        clarification_options = clarifications.get(question_type, [default_clarification])
        verdict = "🤔"
        analysis = random.choice(clarification_options)
        strategy = "Просто переформулируй вопрос конкретнее - и получишь точный ответ!"
        
        return verdict, analysis, strategy
    
    def _get_detailed_analysis(self, question, moon_sign, sun_sign, question_type):
        """ДЕТАЛЬНЫЙ анализ КОНКРЕТНОГО вопроса"""
        
        # СПЕЦИФИЧЕСКИЕ ШАБЛОНЫ ДЛЯ РАЗНЫХ ТИПОВ ВОПРОСОВ
        if question_type == "ФИНАНСЫ":
            return self._get_specific_finance_analysis(question, moon_sign, sun_sign)
        elif question_type == "ОТНОШЕНИЯ":
            return self._get_specific_relationship_analysis(question, moon_sign, sun_sign)
        elif question_type == "КАРЬЕРА":
            return self._get_specific_career_analysis(question, moon_sign, sun_sign)
        elif question_type == "ЗДОРОВЬЕ":
            return self._get_specific_health_analysis(question, moon_sign, sun_sign)
        elif question_type == "ПУТЕШЕСТВИЯ":
            return self._get_specific_travel_analysis(question, moon_sign, sun_sign)
        else:
            return self._get_general_analysis(question, moon_sign, sun_sign)
    
    def _get_specific_finance_analysis(self, question, moon_sign, sun_sign):
        """КОНКРЕТНЫЙ анализ финансовых вопросов"""
        question_lower = question.lower()
        
        # РАЗНЫЕ ТИПЫ ФИНАНСОВЫХ ВОПРОСОВ
        if any(word in question_lower for word in ['получу', 'придут', 'деньги', 'зарплат', 'преми', 'доход']):
            return self._analyze_money_coming(question, moon_sign, sun_sign)
        elif any(word in question_lower for word in ['долг', 'вернут', 'задолжал', 'одолжил']):
            return self._analyze_debt_return(question, moon_sign, sun_sign)
        elif any(word in question_lower for word in ['покупк', 'трат', 'потрат', 'купить']):
            return self._analyze_purchase(question, moon_sign, sun_sign)
        elif any(word in question_lower for word in ['инвест', 'вложен', 'бизнес']):
            return self._analyze_investment(question, moon_sign, sun_sign)
        elif any(word in question_lower for word in ['кредит', 'заем', 'ипотек']):
            return self._analyze_credit(question, moon_sign, sun_sign)
        else:
            return self._get_finance_analysis(question, moon_sign, sun_sign)
    
    def _analyze_money_coming(self, question, moon_sign, sun_sign):
        """Анализ поступления денег"""
        money_signs = ['Телец', 'Рак', 'Козерог', 'Скорпион']
        
        if moon_sign in money_signs:
            verdict = "ДЕНЬГИ ПРИДУТ 💰"
            base_reason = "Финансовые потоки активны!"
            
            # Конкретные сроки в зависимости от знаков
            if moon_sign == 'Телец':
                timing = "В ближайшие 2-3 недели"
            elif moon_sign == 'Рак':
                timing = "В течение месяца"
            elif moon_sign == 'Козерог':
                timing = "До конца этого периода"
            else:
                timing = "Скоро"
                
            insight = f"Луна в {moon_sign} обещает поступление средств. {timing}. Солнце в {sun_sign} советует быть готовым к новым возможностям."
        else:
            verdict = "НУЖНО ПОДОЖДАТЬ ⏳"
            base_reason = "Деньги в пути, но требуют терпения!"
            insight = f"Луна в {moon_sign} показывает некоторую задержку. Солнце в {sun_sign} рекомендует проявить настойчивость."
        
        strategies = [
            "Проверь все финансовые каналы - деньги могут прийти неожиданно",
            "Составь план распределения средств заранее",
            "Не давай деньги в долг до поступления"
        ]
        
        analysis = f"{base_reason} {insight}"
        strategy = random.choice(strategies)
        return verdict, analysis, strategy
    
    def _analyze_debt_return(self, question, moon_sign, sun_sign):
        """Анализ возврата долга"""
        if moon_sign in ['Телец', 'Козерог', 'Дева']:
            verdict = "ВЕРНУТ ✅"
            base_reason = "Долг будет возвращен!"
            
            if 'скоро' in question.lower() or 'когда' in question.lower():
                if moon_sign == 'Телец':
                    timing = "В ближайшую неделю"
                elif moon_sign == 'Козерог':
                    timing = "В течение 10-14 дней"
                else:
                    timing = "Скоро"
                insight = f"Луна в {moon_sign} показывает: {timing}. Солнце в {sun_sign} говорит о честности должника."
            else:
                insight = f"Луна в {moon_sign} гарантирует возврат. Солнце в {sun_sign} показывает ответственность человека."
        else:
            verdict = "ПРОБЛЕМЫ С ВОЗВРАТОМ ❌"
            base_reason = "Могут возникнуть сложности!"
            insight = f"Луна в {moon_sign} указывает на задержки. Солнце в {sun_sign} советует проявить терпение или напомнить о долге."
        
        strategies = [
            "Вежливо напомни о долге - это ускорит возврат",
            "Предложи вариант рассрочки, если нужно",
            "Сохраняй все документы и переписки"
        ]
        
        analysis = f"{base_reason} {insight}"
        strategy = random.choice(strategies)
        return verdict, analysis, strategy
    
    def _analyze_purchase(self, question, moon_sign, sun_sign):
        """Анализ покупки"""
        if moon_sign in ['Телец', 'Дева', 'Козерог']:
            verdict = "СТОИТ ПОКУПАТЬ 🛍️"
            base_reason = "Покупка будет удачной!"
            insight = f"Луна в {moon_sign} благословляет эту покупку. Солнце в {sun_sign} говорит о хорошем качестве."
        else:
            verdict = "ПОДУМАЙ ЕЩЕ 🤔"
            base_reason = "Лучше отложить покупку!"
            insight = f"Луна в {moon_sign} советует подождать. Солнце в {sun_sign} показывает возможные скрытые недостатки."
        
        strategies = [
            "Сравни цены в разных местах перед покупкой",
            "Проверь отзывы о товаре",
            "Убедись, что это действительно необходимо"
        ]
        
        analysis = f"{base_reason} {insight}"
        strategy = random.choice(strategies)
        return verdict, analysis, strategy
    
    def _get_specific_relationship_analysis(self, question, moon_sign, sun_sign):
        """КОНКРЕТНЫЙ анализ отношений"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['любит', 'чувств', 'нравлюсь']):
            return self._analyze_love_feelings(question, moon_sign, sun_sign)
        elif any(word in question_lower for word in ['вернется', 'вернет', 'вернуться']):
            return self._analyze_return_ex(question, moon_sign, sun_sign)
        elif any(word in question_lower for word in ['встреч', 'знакомств', 'судьб']):
            return self._analyze_meeting(question, moon_sign, sun_sign)
        elif any(word in question_lower for word in ['измен', 'обман']):
            return self._analyze_cheating(question, moon_sign, sun_sign)
        else:
            return self._get_relationship_analysis(question, moon_sign, sun_sign)
    
    def _analyze_love_feelings(self, question, moon_sign, sun_sign):
        """Анализ чувств человека"""
        heart_signs = ['Рак', 'Телец', 'Весы', 'Рыбы']
        
        if moon_sign in heart_signs:
            verdict = "ЧУВСТВА ЕСТЬ 💖"
            base_reason = "Он(а) испытывает к тебе симпатию!"
            insight = f"Луна в {moon_sign} показывает искренние чувства. Солнце в {sun_sign} говорит о глубокой привязанности."
        else:
            verdict = "НЕУВЕРЕННОСТЬ 🤷‍♀️"
            base_reason = "Чувства есть, но пока неясны!"
            insight = f"Луна в {moon_sign} указывает на внутренние сомнения. Солнце в {sun_sign} советует дать время."
        
        strategies = [
            "Прояви инициативу, но не дави",
            "Будь естественной - это привлекает",
            "Дайте отношениям развиваться постепенно"
        ]
        
        analysis = f"{base_reason} {insight}"
        strategy = random.choice(strategies)
        return verdict, analysis, strategy
    
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
        """Общий анализ отношений"""
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
        """Общий анализ финансов"""
        money_signs = ['Телец', 'Рак', 'Козерог', 'Скорпион']
        
        if moon_sign in money_signs:
            verdict = "ПОТОКИ ОТКРЫТЫ 💰"
            base_reason = "Финансовая энергия благоприятствует!"
        else:
            verdict = "ОСТОРОЖНОСТЬ 💸"
            base_reason = "Время для разумного планирования!"
        
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
        """Общий анализ карьеры"""
        career_signs = ['Лев', 'Стрелец', 'Козерог', 'Скорпион', 'Дева']
        
        if sun_sign in career_signs:
            verdict = "РОСТ 🚀"
            base_reason = "Профессиональная энергия на подъеме!"
        else:
            verdict = "РАЗВИТИЕ 📈"
            base_reason = "Время для накопления компетенций!"
        
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
        """Общий анализ путешествий"""
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
        """Общий анализ здоровья"""
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
    
    # Заглушки для остальных специфических методов
    def _get_specific_career_analysis(self, question, moon_sign, sun_sign):
        return self._get_career_analysis(question, moon_sign, sun_sign)
    
    def _get_specific_health_analysis(self, question, moon_sign, sun_sign):
        return self._get_health_analysis(question, moon_sign, sun_sign)
    
    def _get_specific_travel_analysis(self, question, moon_sign, sun_sign):
        return self._get_travel_analysis(question, moon_sign, sun_sign)
    
    def _analyze_investment(self, question, moon_sign, sun_sign):
        return self._get_finance_analysis(question, moon_sign, sun_sign)
    
    def _analyze_credit(self, question, moon_sign, sun_sign):
        return self._get_finance_analysis(question, moon_sign, sun_sign)
    
    def _analyze_return_ex(self, question, moon_sign, sun_sign):
        return self._get_relationship_analysis(question, moon_sign, sun_sign)
    
    def _analyze_meeting(self, question, moon_sign, sun_sign):
        return self._get_relationship_analysis(question, moon_sign, sun_sign)
    
    def _analyze_cheating(self, question, moon_sign, sun_sign):
        return self._get_relationship_analysis(question, moon_sign, sun_sign)

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
        
        # ПРОВЕРЯЕМ, НЕ ЖДЕМ ЛИ МЫ УТОЧНЕНИЯ
        user_id = message.from_user.id
        if user_id in smart_analyzer.waiting_for_clarification:
            question_type = smart_analyzer.waiting_for_clarification[user_id]
            del smart_analyzer.waiting_for_clarification[user_id]  # Убираем из ожидания
            
            # Анализируем уточненный вопрос
            verdict, analysis, strategy = smart_analyzer._get_detailed_analysis(
                message.text, moon_sign, sun_sign, question_type
            )
        else:
            # Обычный анализ
            verdict, analysis, strategy = smart_analyzer.generate_smart_response(
                message.text, moon_sign, sun_sign, question_type, user_id
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
