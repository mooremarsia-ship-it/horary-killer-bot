def get_detailed_analysis(question_text):
    try:
        # ПРАВИЛЬНОЕ время!
        display_time = get_moscow_time()
        
        observer = ephem.Observer()
        observer.lat = '55.7558'
        observer.lon = '37.6173'
        
        # Расчет всех планет
        planets = {
            'Луна': ephem.Moon(),
            'Солнце': ephem.Sun(),
            'Венера': ephem.Venus(),
            'Марс': ephem.Mars(),
            'Меркурий': ephem.Mercury(),
            'Юпитер': ephem.Jupiter(),
            'Сатурн': ephem.Saturn()
        }
        
        for name, planet in planets.items():
            planet.compute(observer)
        
        # Получаем знаки с исправлением Ophiuchus
        moon_sign = get_zodiac_sign(planets['Луна'])
        sun_sign = get_zodiac_sign(planets['Солнце'])
        venus_sign = get_zodiac_sign(planets['Венера'])
        mars_sign = get_zodiac_sign(planets['Марс'])
        mercury_sign = get_zodiac_sign(planets['Меркурий'])
        jupiter_sign = get_zodiac_sign(planets['Юпитер'])
        saturn_sign = get_zodiac_sign(planets['Сатурн'])
        
        # Правильные управители
        moon_ruler = get_planet_ruler(moon_sign)
        sun_ruler = get_planet_ruler(sun_sign)
        venus_ruler = get_planet_ruler(venus_sign)
        mars_ruler = get_planet_ruler(mars_sign)
        
        # ИСПОЛЬЗУЕМ МОЗГ БОТА! 🧠
        question_type, house, significator = bot_brain.analyze_question_type(question_text)
        verdict, reasoning = bot_brain.make_decision(moon_sign, venus_sign, question_type)
        strategy = bot_brain.generate_strategy(verdict, moon_sign, question_type)
        
        # ДЕТАЛЬНЫЙ АНАЛИЗ
        advice_text = "благоприятствует вашим намерениям" if "ДА" in verdict else "требует осторожного подхода" if "НЕТ" in verdict else "оставляет пространство для маневра"
        
        analysis = f"""
🔮 УМНЫЙ ХОРАРНЫЙ АНАЛИЗ
⏰ {display_time}, МОСКВА

❓ ВОПРОС: {question_text}
🎯 ТИП: {question_type} ({house}-й дом)
⚖️ СИГНИФИКАТОР: {significator}

📊 ДЕТАЛЬНАЯ КАРТА:

• 🌙 Луна: {moon_sign} (упр. {moon_ruler}) - эмоциональный фон
• ☀️ Солнце: {sun_sign} (упр. {sun_ruler}) - воля и цель
• ♀️ Венера: {venus_sign} (упр. {venus_ruler}) - любовь и деньги
• ♂️ Марс: {mars_sign} (упр. {mars_ruler}) - энергия действий
• ☿ Меркурий: {mercury_sign} - коммуникация
• ♃ Юпитер: {jupiter_sign} - удача и расширение
• ♄ Сатурн: {saturn_sign} - ограничения и карма

⚡ ВЕРДИКТ: {verdict}
💡 ОБОСНОВАНИЕ: {reasoning}

🎪 СТРАТЕГИЯ: {strategy}

🌟 АСТРОЛОГИЧЕСКИЙ СОВЕТ:
Текущая конфигурация планет {advice_text}. Обратите особое внимание на положение {moon_sign} для эмоционального состояния и {venus_sign} для гармонии.

🤖 Уровень анализа: {bot_brain.experience + 1}
"""
        return analysis
        
    except Exception as e:
        return f"❌ Ошибка анализа: {str(e)}"
