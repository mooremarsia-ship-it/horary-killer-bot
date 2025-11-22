# 🕵️ ХОРАРНЫЙ УБИЙЦА - АСТРОЛОГИЧЕСКОЕ ЯДРО
import ephem
from datetime import datetime

print("🔮 ХОРАРНЫЙ УБИЙЦА - РАБОЧАЯ СИСТЕМА\n")

# Создаем астрологическую карту
observer = ephem.Observer()
observer.lat = '55.7558'
observer.lon = '37.6173'
observer.date = datetime.now()

print("📍 Место: Москва")
print(f"⏰ Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")

# Расчет планет
planets = {
    'Солнце': ephem.Sun(),
    'Луна': ephem.Moon(), 
    'Меркурий': ephem.Mercury(),
    'Венера': ephem.Venus(),
    'Марс': ephem.Mars(),
}

print("\n📊 ПОЗИЦИИ ПЛАНЕТ:")
for name, planet in planets.items():
    planet.compute(observer)
    constellation = ephem.constellation(planet)[1]
    print(f"   {name}: {constellation}")

# Простая логика вердикта
moon_sign = ephem.constellation(planets['Луна'])[1]
if moon_sign in ['Libra', 'Taurus', 'Cancer']:
    verdict = "ДА"
    reason = f"Луна в гармоничном знаке {moon_sign}"
else:
    verdict = "НЕТ" 
    reason = f"Луна в сложном положении ({moon_sign})"

print(f"\n⚡ ВЕРДИКТ: {verdict}")
print(f"📖 ОБОСНОВАНИЕ: {reason}")
print(f"\n🚀 СИСТЕМА ГОТОВА К ИНТЕГРАЦИИ С БОТОМ")
