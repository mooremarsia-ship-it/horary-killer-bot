def get_detailed_analysis(question_text):
    try:
        # РЕАЛЬНОЕ время для отображения
        from datetime import datetime
        real_time = datetime.now()
        display_time = real_time.strftime('%H:%M, %d.%m.%Y')
        
        # Время для астрономических расчетов (оставляем как было)
        observer = ephem.Observer()
        observer.lat = '55.7558'
        observer.lon = '37.6173'  
        observer.date = real_time  # используем реальное время для расчетов
        
        # Остальной код без изменений...
        moon = ephem.Moon()
        sun = ephem.Sun()
        mars = ephem.Mars()
        venus = ephem.Venus()
        mercury = ephem.Mercury()
        jupiter = ephem.Jupiter()
        
        moon.compute(observer)
        sun.compute(observer)
        mars.compute(observer)
        venus.compute(observer)
        mercury.compute(observer)
        jupiter.compute(observer)
        
        moon_sign = get_russian_zodiac(ephem.constellation(moon)[1])
        sun_sign = get_russian_zodiac(ephem.constellation(sun)[1])
        mars_sign = get_russian_zodiac(ephem.constellation(mars)[1])
        venus_sign = get_russian_zodiac(ephem.constellation(venus)[1])
        mercury_sign = get_russian_zodiac(ephem.constellation(mercury)[1])
        jupiter_sign = get_russian_zodiac(ephem.constellation(jupiter)[1])
        
        moon_ruler = get_planet_ruler(moon_sign)
        sun_ruler = get_planet_ruler(sun_sign)
        mars_ruler = get_planet_ruler(mars_sign)
        venus_ruler = get_planet_ruler(venus_sign)
        
        favorable_signs = ['Телец', 'Рак', 'Весы', 'Стрелец', 'Рыбы']
        
        if moon_sign in favorable_signs and venus_sign in favorable_signs:
            verdict = "ДА ✅"
            reason = f"Луна в {moon_sign} и Венера в {venus_sign} создают отличные условия для финансов"
            advice = "Действуйте активно - период благоприятствует денежным потокам"
        elif moon_sign in favorable_signs:
            verdict = "ДА ✅" 
            reason = f"Луна в {moon_sign} способствует успешному исходу"
            advice = "Проявите инициативу - звезды поддерживают ваши начинания"
        else:
            verdict = "НЕТ ❌"
            reason = f"Луна в {moon_sign} указывает на временные затруднения"
            advice = "Проявите терпение - лучшее время еще впереди"
        
        analysis = f"""
🔮 ДЕТАЛЬНЫЙ ХОРАРНЫЙ АНАЛИЗ
⏰ {display_time}, МОСКВА

❓ ВОПРОС: {question_text}

📊 ДЕТАЛИ КАРТЫ:

• 🌙 Луна: {moon_sign} (упр. {moon_ruler}) - эмоциональный фон
• ☀️ Солнце: {sun_sign} (упр. {sun_ruler}) - источник воли
• ♀️ Венера: {venus_sign} (упр. {venus_ruler}) - деньги, ценности
• ♂️ Марс: {mars_sign} (упр. {mars_ruler}) - энергия действий
• ☿ Меркурий: {mercury_sign} - коммуникация, переговоры
• ♃ Юпитер: {jupiter_sign} - удача, расширение

⚡ ВЕРДИКТ: {verdict}
📖 ОБОСНОВАНИЕ: {reason}

💫 РЕКОМЕНДАЦИЯ: {advice}

🌟 АСТРОЛОГИЧЕСКИЙ КОНТЕКСТ:
Текущее положение планет {("благоприятствует финансовым операциям" if "ДА" in verdict else "требует осторожности в денежных вопросах")}. 
Обратите внимание на {venus_sign} для финансов и {moon_sign} для эмоционального состояния.
"""
        return analysis
        
    except Exception as e:
        return f"❌ Ошибка анализа: {str(e)}"
