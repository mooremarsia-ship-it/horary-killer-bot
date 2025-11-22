
import telebot
import time
import ephem
from datetime import datetime
import math

BOT_TOKEN = "7166686748:AAFnyfjq5UsunijP_p8HQiYeKHh3qoAM5RA"
bot = telebot.TeleBot(BOT_TOKEN)

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

def calculate_houses(observer):
    """Расчет домов гороскопа"""
    sun = ephem.Sun()
    sun.compute(observer)
    
    # Простая система домов - каждый знак = 30 градусов
    asc_deg = math.degrees(sun.az)
    asc_sign_num = int(asc_deg / 30)
    
    signs = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева',
             'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']
    
    houses = {}
    for i in range(12):
        house_sign = signs[(asc_sign_num + i) % 12]
        houses[i+1] = house_sign
    
    return houses

def detect_question_theme(question):
    """Определение темы вопроса и соответствующих домов"""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['деньг', 'финанс', 'денег', 'заработ']):
        return "Финансы", 2, "Деньги, ресурсы, материальные ценности"
    elif any(word in question_lower for word in ['любит', 'скуч', 'отношен', 'чувств', 'любов']):
        return "Любовь и отношения", 7, "Партнерство, брак, серьезные отношения"
    elif any(word in question_lower for word in ['работ', 'карьер', 'бизнес', 'проект']):
        return "Карьера", 10, "Профессия, статус, достижения"
    elif any(word in question_lower for word in ['здоров', 'болез', 'самочувств']):
        return "Здоровье", 6, "Здоровье, болезни, обслуживание"
    elif any(word in question_lower for word in ['путешеств', 'поездк', 'переезд']):
        return "Путешествия", 9, "Дальние поездки, высшее образование"
    else:
        return "Общий вопрос", 1, "Личность, инициатива, самореализация"

def calculate_aspects(planet1, planet2):
    """Расчет аспектов между планетами"""
    deg1 = math.degrees(planet1.ra)
    deg2 = math.degrees(planet2.ra)
    
    difference = abs(deg1 - deg2) % 360
    if difference > 180:
        difference = 360 - difference
    
    # Определение аспектов
    if difference <= 8:  # Соединение
        return "соединение", "Встреча, слияние энергий"
    elif abs(difference - 180) <= 8:  # Оппозиция
        return "оппозиция", "Конфликт, выбор, напряжение"
    elif abs(difference - 120) <= 8:  # Трин
        return "трин", "Поток, удача, гармония"
    elif abs(difference - 90) <= 8:  # Квадрат
        return "квадрат", "Вызов, напряжение, развитие"
    elif abs(difference - 60) <= 8:  # Секстиль
        return "секстиль", "Возможность, шанс, сотрудничество"
    else:
        return "нет аспекта", "Нет значимого взаимодействия"

def get_planet_meaning(planet_name):
    """Значение планет в хорарной астрологии"""
    meanings = {
        'Sun': 'Отец, власть, сердце, жизненная сила',
        'Moon': 'Мать, эмоции, безопасность, народ',
        'Mercury': 'Брат, информация, обмен, коммуникация',
        'Venus': 'Сестра, любовь, деньги, красота, гармония',
        'Mars': 'Воин, действие, агрессия, импульс',
        'Jupiter': 'Учитель, расширение, удача, мудрость',
        'Saturn': 'Старец, ограничения, карма, время',
        'Uranus': 'Бунтарь, неожиданности, свобода',
        'Neptune': 'Мистик, иллюзии, тайны, вдохновение',
        'Pluto': 'Маг, трансформация, смерть и возрождение'
    }
    return meanings.get(planet_name, 'Неизвестное значение')

def get_true_horary_analysis(question_text):
    """НАСТОЯЩИЙ хорарный анализ по всем правилам"""
    try:
        # Фиксируем ТОЧНОЕ время вопроса
        question_time = datetime.now()
        
        observer = ephem.Observer()
        observer.lat = '55.7558'  # Москва
        observer.lon = '37.6173'  
        observer.date = question_time
        
        # Расчет всех планет
        planets = {
            'Sun': ephem.Sun(),
            'Moon': ephem.Moon(),
            'Mercury': ephem.Mercury(),
            'Venus': ephem.Venus(),
            'Mars': ephem.Mars(),
            'Jupiter': ephem.Jupiter(),
            'Saturn': ephem.Saturn(),
            'Uranus': ephem.Uranus(),
            'Neptune': ephem.Neptune(),
            'Pluto': ephem.Pluto()
        }
        
        for planet in planets.values():
            planet.compute(observer)
        
        # Определение домов
        houses = calculate_houses(observer)
        
        # Анализ вопроса
        theme, house_num, house_meaning = detect_question_theme(question_text)
        
        # Управители домов
        ascendant_sign = houses[1]
        question_house_sign = houses[house_num]
        
        asc_ruler = get_planet_ruler(ascendant_sign)
        question_ruler = get_planet_ruler(question_house_sign)
        
        # Поиск аспектов между управителями
        asc_planet = planets.get([k for k,v in planets.items() if get_planet_ruler(get_russian_zodiac(ephem.constellation(v)[1])) == asc_ruler][0]) if any(get_planet_ruler(get_russian_zodiac(ephem.constellation(v)[1])) == asc_ruler for v in planets.values()) else planets['Sun']
        question_planet = planets.get([k for k,v in planets.items() if get_planet_ruler(get_russian_zodiac(ephem.constellation(v)[1])) == question_ruler][0]) if any(get_planet_ruler(get_russian_zodiac(ephem.constellation(v)[1])) == question_ruler for v in planets.values()) else planets['Moon']
        
        aspect, aspect_meaning = calculate_aspects(asc_planet, question_planet)
        
        # Определение вердикта на основе аспектов
        if aspect in ['трин', 'секстиль', 'соединение']:
            verdict = "ДА ✅"
            reason = f"Обнаружен гармоничный аспект ({aspect}) между управителями"
        else:
            verdict = "НЕТ ❌"
            reason = f"Аспект {aspect} указывает на препятствия"
        
        # Формирование профессионального ответа
        analysis = f"""
🔮 ХОРАРНАЯ КАРТА НА {question_time.strftime('%H:%M, %d.%m.%Y')}, МОСКВА

Восход: {ascendant_sign}. Луна: {get_russian_zodiac(ephem.constellation(planets['Moon'])[1])}.

---

АНАЛИЗ: {question_text}

· Вопрошающий (1-й дом): {ascendant_sign}. Управитель — {asc_ruler}.
· {theme} ({house_num}-й дом): {question_house_sign}. Управитель — {question_ruler}.

КЛЮЧЕВЫЕ АСПЕКТЫ:

1. {asc_ruler} (Вы) и {question_ruler} (Цель) - {aspect.upper()}
   · {aspect_meaning}

2. Луна в {get_russian_zodiac(ephem.constellation(planets['Moon'])[1])}
   · {get_planet_meaning('Moon')} - определяет эмоциональный фон ситуации

3. Основные позиции:
   · Солнце ({get_russian_zodiac(ephem.constellation(planets['Sun'])[1])}) - {get_planet_meaning('Sun')}
   · Венера ({get_russian_zodiac(ephem.constellation(planets['Venus'])[1])}) - {get_planet_meaning('Venus')}
   · Марс ({get_russian_zodiac(ephem.constellation(planets['Mars'])[1])}) - {get_planet_meaning('Mars')}

---

ВЕРДИКТ: {verdict}

{reason}.

💫 ФИЛОСОФИЯ ОТВЕТА:
Хорарная карта - это не предсказание, а карта энергетических течений. 
{("Вы находитесь в потоке благоприятных энергий - действуйте уверенно" if verdict == "ДА ✅" else "Сейчас период энергетических сложностей - проявите терпение и стратегическое мышление")}

📊 ТЕХНИЧЕСКИЕ ДЕТАЛИ:
• Время вопроса: {question_time.strftime('%H:%M:%S')}
• Аспект между сигнификаторами: {aspect}
• Эмоциональный фон: {get_russian_zodiac(ephem.constellation(planets['Moon'])[1])}
"""
        return analysis
        
    except Exception as e:
        return f"❌ Ошибка построения карты: {str(e)}"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('/'):
        if message.text == '/start':
            bot.reply_to(message, "🔮 Я — Хорарный Император. Задай ОСТРЫЙ и КОНКРЕТНЫЙ вопрос, и я построю карту звездного неба на момент твоего вопроса!")
        return
    
    analysis = get_true_horary_analysis(message.text)
    bot.reply_to(message, analysis)

print("🔄 Хорарный Император с МОЗГАМИ запущен...")
while True:
    try:
        bot.polling(none_stop=True, interval=1)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
