from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Твой астрологический сервер
ASTRO_SERVER = "https://horary-killer-bot.onrender.com"

@app.route('/telegram-webhook', methods=['POST'])
def telegram_webhook():
    """Принимаем сообщения от Telegram бота"""
    data = request.json
    message_text = data.get('message', {}).get('text', '')
    
    if message_text.startswith('/'):
        # Это команда, пропускаем
        return jsonify({"status": "ignored"})
    
    # Отправляем вопрос на астрологический сервер
    try:
        response = requests.get(ASTRO_SERVER)
        if response.status_code == 200:
            # Парсим вердикт из HTML
            if "Вердикт: ДА" in response.text:
                verdict = "ДА"
            elif "Вердикт: НЕТ" in response.text:
                verdict = "НЕТ"
            else:
                verdict = "НЕОПРЕДЕЛЕНО"
            
            return jsonify({
                "response": f"⚡ ВЕРДИКТ: {verdict}",
                "original_question": message_text
            })
    except Exception as e:
        return jsonify({"error": str(e)})
    
    return jsonify({"response": "Система временно недоступна"})

@app.route('/')
def home():
    return "Мост для Хорарного Убийцы активен!"

if name == '__main__':
    app.run(host='0.0.0.0', port=5001)
