from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Твой астрологический сервер
ASTRO_SERVER = "https://horary-killer-bot.onrender.com"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Принимаем сообщения от Telegram"""
    data = request.json
    message = data.get('message', {})
    text = message.get('text', '')
    chat_id = message.get('chat', {}).get('id')
    
    # Игнорируем команды
    if text.startswith('/'):
        return jsonify({"status": "ignored"})
    
    # Получаем вердикт от астрологического ядра
    try:
        response = requests.get(ASTRO_SERVER)
        if response.status_code == 200:
            if "Вердикт: ДА" in response.text:
                verdict = "ДА ✅"
            elif "Вердикт: НЕТ" in response.text:
                verdict = "НЕТ ❌"
            else:
                verdict = "НЕОПРЕДЕЛЕНО ⚡"
            
            # Здесь будет код отправки ответа в Telegram
            response_text = f"🔮 ХОРАРНЫЙ УБИЙЦА:\nВопрос: {text}\nВердикт: {verdict}"
            
            return jsonify({
                "status": "success",
                "response": response_text
            })
    except Exception as e:
        return jsonify({"error": str(e)})
    
    return jsonify({"status": "error"})

@app.route('/')
def home():
    return "НАСТОЯЩИЙ ТЕЛЕГРАМ БОТ АКТИВЕН!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
