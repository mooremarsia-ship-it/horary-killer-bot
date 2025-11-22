@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('/'):
        if message.text == '/start':
            bot.reply_to(message, "🔮 Я — Хорарный Император. Задай вопрос о любви, деньгах, работе...")
        return
    
    # СТАРЫЙ КОД - использует простую функцию вместо развернутого анализа!
    verdict = get_astrological_verdict(message.text)
    bot.reply_to(message, verdict)
