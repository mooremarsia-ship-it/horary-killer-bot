from flask import Flask, request, jsonify
import ephem
from datetime import datetime

app = Flask(__name__)

def calculate_horary(question_text, question_time):
    """Твоя астрологическая логика"""
    observer = ephem.Observer()
    observer.lat = '55.7558'
    observer.lon = '37.6173'
    observer.date = question_time
    
    planets = {
        'Солнце': ephem.Sun(),
        'Луна': ephem.Moon(), 
        'Меркурий': ephem.Mercury(),
        'Венера': ephem.Venus(),
        'Марс': ephem.Mars(),
    }
    
    for planet in planets.values():
        planet.compute(observer)
    
    # Астрологическая логика
    moon_sign = ephem.constellation(planets['Луна'])[1]
    if moon_sign in ['Libra', 'Taurus', 'Cancer']:
        return "ДА", f"Луна в гармоничном знаке {moon_sign}"
    else:
        return "НЕТ", f"Луна в сложном положении ({moon_sign})"

@app.route('/health')
def health_check():
    return "Хорарный Убийца активен!"

@app.route('/horary', methods=['POST'])
def horary_endpoint():
    """Конечная точка для бота"""
    data = request.json
    question = data.get('question', '')
    question_time = datetime.now()
    
    verdict, reasoning = calculate_horary(question, question_time)
    
    response = {
        'verdict': verdict,
        'reasoning': reasoning,
        'time': question_time.isoformat()
    }
    
    return jsonify(response)

if name == '__main__':
    app.run(host='0.0.0.0', port=5000)
