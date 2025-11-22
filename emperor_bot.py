import telebot
import time
import ephem
from datetime import datetime, timedelta
import math
import pytz

BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
bot = telebot.TeleBot(BOT_TOKEN)

def get_moscow_time():
    """Получаем ТОЧНОЕ московское время"""
    moscow_tz = pytz.timezone('Europe/Moscow')
    return datetime.now(moscow_tz)

def get_russian_zodiac(eng_sign):
    zodiac_map = {
        'Aries': 'Овен', 'Taurus': 'Телец', 'Gemini': 'Близнецы',
        'Cancer': 'Рак', 'Leo': 'Лев', 'Virgo': 'Дева',
        'Libra': 'Весы', 'Scorpio': 'Скорпион', 'Sagittarius': 'Стрелец',
        'Capricorn': 'Козерог', 'Aquarius': 'Водолей', 'Pisces': 'Рыбы'
    }
    return zodiac_map.get(eng_sign, eng_sign)

def get_planet_ruler(sign):
    rulers = {
        'Aries': 'Марс', 'Taurus': 'Венера', 'Gemini': 'Меркурий',
        'Cancer': 'Луна', 'Leo': 'Солнце', 'Virgo': 'Меркурий',
        'Libra': 'Венера', 'Scorpio': 'Плутон', 'Sagittarius': 'Юпитер',
        'Capricorn': 'Сатурн', 'Aquarius': 'Уран', 'Pisces': 'Нептун'
    }
    return rulers.get(sign, 'Неизвестно')

def get_current_planets_positions(observer):
    """Получаем текущие позиции планет"""
    planets_data = {}
    
    planets = {
        'Луна': ephem.Moon(),
        'Солнце': ephem.Sun(),
        'Меркурий': ephem.Mercury(),
        'Венера': ephem.Venus(),
        'Марс': ephem.Mars(),
        'Юпитер': ephem.Jupiter(),
        'Сатурн': ephem.Saturn()
    }
    
    for name, planet in planets.items():
        planet.compute(observer)
        sign = get_russian_zodiac(ephem.constellation(planet)[1])
        planets_data[name] = {
            'sign': sign,
            'ruler': get_planet_ruler(sign),
            'position': f"{math.degrees(planet.ra):.1f}°"
        }
    
    return planets_data

def detect_question_type(question):
    """Определяем тип вопроса для правильного анализа"""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['деньг', 'финанс', 'заработ', 'придут', 'получу']):
        return {
            'theme': 'Финансы',
            'house': 2,
            'meaning': 'Ваши деньги, ресурсы, материальные поступления',
            'significator': 'Венера'
        }
    elif any(word in question_lower for word in ['любит', 'скуч', 'отношен', 'чувств']):
        return {
            'theme': 'Любовь и отношения', 
            'house': 7,
            'meaning': 'Партнер, серьезные отношения',
            'significator': 'Венера'
        }
    elif any(word in question_lower for word in ['работ', 'карьер', 'бизнес']):
        return {
            'theme': 'Карьера',
            'house': 10, 
            'meaning': 'Профессия, статус, достижения',
            'significator': 'Сатурн'
        }
    else:
        return {
            'theme': 'Общий вопрос',
            'house': 1,
            'meaning': 'Личность, инициатива',
            'significator': 'Солнце'
        }

def get_ascendant(observer):
    """Определение восходящего знака"""
    sun = ephem.Sun()
    sun.compute(observer)
    return get_russian_zodiac(ephem.constellation(sun)[1])

def analyze_aspects_for_verdict(planets_data, question_type):
    """Анализ аспектов для определения вердикта"""
    moon_sign = planets_data['Луна']['sign']
    significator_sign = planets_data[question_type['significator']]['sign']
    
    # Логика вердикта на основе Луны и сигнификатора
    favorable_moon = ['Телец', 'Рак', 'Весы', 'Стрелец', 'Рыбы']
    favorable_combinations = [
        ('Венера', 'Телец'), ('Венера', 'Весы'), ('Юпитер', 'Стрелец'),
        ('Луна', 'Рак'), ('Солнце', 'Лев'), ('Меркурий', 'Близнецы')
    ]
    
    current_combination = (question_type['significator'], significator_sign)
    
    if moon_sign in favorable_moon and current_combination in favorable_combinations:
        return "ДА ✅", f"Луна в {moon_sign} и {question_type['significator']} в {significator_sign} создают исключительно благоприятные условия"
    elif moon_sign in favorable_moon:
        return "ДА ✅", f"Луна в {moon_sign} способствует успешному исходу"
    elif current_combination in favorable_combinations:
        return "ДА ✅", f"{question_type['significator']} в {significator_sign} указывает на положительный результат"
    else:
        return "НЕТ ❌", f"Текущая конфигурация планет указывает на препятствия"

def generate_detailed_analysis(question, planets_data, question_type, current_time):
    """Генерация детального анализа"""
    
    ascendant = get_ascendant(ephem.Observer())
    verdict, reasoning = analyze_aspects_for_verdict(planets_data, question_type)
    
    analysis = f"""
🔮 ХОРАРНАЯ КАРТА НА {current_time.strftime('%H:%M, %d.%m.%Y')}, МОСКВА

Восход: {ascendant}. Луна: {planets_data['Луна']['sign']}.

---

АНАЛИЗ: {question}

· Вопрошающий (1-й дом): {ascendant}. Управитель — {planets_data[question_type['significator']]['ruler']}.
· {question_type['theme']} ({question_type['house']}-й дом): {planets_data[question_type['significator']]['sign']}. Управитель — {planets_data[question_type['significator']]['ruler']}.

КЛЮЧЕВЫЕ ПОЗИЦИИ:

1. Луна ({planets_data['Луна']['sign']}) в {planets_data['Луна']['position']}
   · Эмоциональный фон ситуации: {get_moon_interpretation(planets_data['Луна']['sign'])}

2. {question_type['significator']} ({planets_data[question_type['significator']]['sign']}) в {planets_data[question_type['significator']]['position']}
   · Ключевой сигнификатор: {get_planet_interpretation(question_type['significator'], planets_data[question_type['significator']]['sign'])}

3. Марс ({planets_data['Марс']['sign']}) в {planets_data['Марс']['position']}
   · Энергия действий: {get_mars_interpretation(planets_data['Марс']['sign'])}

---

ВЕРДИКТ: {verdict}

{reasoning}

💫 АСТРОЛОГИЧЕСКАЯ КАРТИНА:
Текущая конфигурация планет {("благоприятствует вашим намерениям" if "ДА" in verdict else "требует осторожного подхода")}. 
{get_strategic_advice(planets_data['Луна']['sign'], question_type['theme'])}

📊 ТЕХНИЧЕСКИЕ ДАННЫЕ:
• Точное время вопроса: {current_time.strftime('%H:%M:%S')} МСК
• Эмоциональный фон: {planets_data['Луна']['sign']}
• Ключевая планета: {question_type['significator']}
• Астрологический час: {get_astrological_hour(current_time)}
"""
    return analysis

def get_astrological_hour(current_time):
    """Определение астрологического часа"""
    hour = current_time.hour
    # Простая система планетарных часов
    planetary_hours = {
        0: 'Сатурн', 1: 'Юпитер', 2: 'Марс', 3: 'Солнце',
        4: 'Венера', 5: 'Меркурий', 6: 'Луна',
        7: 'Сатурн', 8: 'Юпитер', 9: 'Марс', 10: 'Солнце',
        11: 'Венера', 12: 'Меркурий', 13: 'Луна',
        14: 'Сатурн', 15: 'Юпитер', 16: 'Марс', 17: 'Солнце', 
        18: 'Венера', 19: 'Меркурий', 20: 'Луна',
        21: 'Сатурн', 22: 'Юпитер', 23: 'Марス'
    }
    return planetary_hours.get(hour, 'Неизвестно')

def get_moon_interpretation(sign):
    interpretations = {
        'Овен': 'импульсивность, быстрые изменения',
        'Телец': 'стабильность, практичность', 
        'Близнецы': 'общительность, информация',
        'Рак': 'эмоциональность, безопасность',
        'Лев': 'уверенность, творчество',
        'Дева': 'аналитичность, детали',
        'Весы': 'гармония, партнерство',
        'Скорпион': 'интенсивность, трансформация',
        'Стрелец': 'оптимизм, расширение',
        'Козерог': 'дисциплина, ограничения',
        'Водолей': 'независимость, инновации',
        'Рыбы': 'интуиция, духовность'
    }
    return interpretations.get(sign, 'нейтральное влияние')

def get_planet_interpretation(planet, sign):
    interpretations = {
        'Венера': f'гармония, ценности, притяжение в {sign}',
        'Солнце': f'воля, индивидуальность, цель в {sign}',
        'Сатурн': f'структура, ответственность, время в {sign}',
        'Меркурий': f'коммуникация, информация, обмен в {sign}',
        'Юпитер': f'расширение, удача, мудрость в {sign}',
        'Марс': f'действие, энергия, импульс в {sign}'
    }
    return interpretations.get(planet, f'влияние в знаке {sign}')

def get_mars_interpretation(sign):
    interpretations = {
        'Овен': 'прямое действие, инициатива',
        'Телец': 'устойчивые усилия',
        'Близнецы': 'интеллектуальная активность', 
        'Рак': 'эмоциональная мотивация',
        'Лев': 'творческая энергия',
        'Дева': 'практические действия',
        'Весы': 'сбалансированные действия',
        'Скорпион': 'интенсивная энергия',
        'Стрелец': 'энтузиазм, расширение',
        'Козерог': 'дисциплинированные действия',
        'Водолей': 'инновационные подходы',
        'Рыбы': 'интуитивные действия'
    }
    return interpretations.get(sign, 'активная энергия')

def get_strategic_advice(moon_sign, theme):
    advice_map = {
        'Финансы': {
            'Рак': 'Сосредоточьтесь на сохранении и приумножении существующих ресурсов',
            'Телец': 'Благоприятное время для финансовых операций и инвестиций',
            'Стрелец': 'Возможны неожиданные поступления, но будьте осторожны с рисками',
            'Козерог': 'Требуется дисциплинированный подход к бюджету',
            'Водолей': 'Рассмотрите нестандартные финансовые возможности'
        },
        'Любовь и отношения': {
            'Рак': 'Проявляйте заботу и эмоциональную поддержку',
            'Весы': 'Идеальное время для гармонизации отношений', 
            'Скорпион': 'Глубокие эмоциональные процессы, будьте честны',
            'Водолей': 'Сохраняйте независимость, но будьте открыты',
            'Рыбы': 'Доверяйте интуиции в вопросах сердца'
        }
    }
    
    theme_advice = advice_map.get(theme, {})
    return theme_advice.get(moon_sign, 'Действуйте в соответствии с вашей интуицией и текущими обстоятельствами')

def get_horary_analysis(question_text):
    """Основная функция анализа"""
    try:
        # ВАЖНО: Используем московское время!
        current_time = get_moscow_time()
        
        observer = ephem.Observer()
        observer.lat = '55.7558'  # Москва
        observer.lon = '37.6173'  # Москва
        observer.date = current_time
        
        # Получаем данные планет
        planets_data = get_current_planets_positions(observer)
        question_type = detect_question_type(question_text)
        
        # Генерируем анализ
        analysis = generate_detailed_analysis(question_text, planets_data, question_type, current_time)
        return analysis
        
    except Exception as e:
        return f"❌ Ошибка построения карты: {str(e)}"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('/'):
        if message.text == '/start':
            bot.reply_to(message, "🔮 Я — Хорарный Император. Задай конкретный вопрос для детального астрологического анализа!")
        return
    
    analysis = get_horary_analysis(message.text)
    bot.reply_to(message, analysis)

print("🔄 Хорарный Император с ТОЧНЫМ временем запущен...")
while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
