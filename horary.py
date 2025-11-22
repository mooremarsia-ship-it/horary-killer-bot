from flask import Flask
import ephem
from datetime import datetime

app = Flask(__name__)

def calculate_horary():
    observer = ephem.Observer()
    observer.lat = '55.7558'
    observer.lon = '37.6173'
    observer.date = datetime.now()
    
    planets = {
        'Солнце': ephem.Sun(),
        'Луна': ephem.Moon(),
    }
    
    for planet in planets.values():
        planet.compute(observer)
    
    moon_sign = ephem.constellation(planets['Луна'])[1]
    return "ДА" if moon_sign in ['Libra', 'Taurus'] else "НЕТ"

@app.route('/')
def home():
    verdict = calculate_horary()
    return f'''
    <html>
        <body>
            <h1>🔮 ХОРАРНЫЙ УБИЙЦА АКТИВЕН</h1>
            <p>⚡ Вердикт: {verdict}</p>
            <p>⏰ Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
