import requests

def get_weather(city: str) -> str:
    """
    Получает текущую температуру для указанного города
    с помощью бесплатного API Open-Meteo.
    """
    try:
        # Геокодирование: получаем координаты города
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=ru&format=json"
        geo_resp = requests.get(geo_url, timeout=10).json()

        if "results" not in geo_resp or len(geo_resp["results"]) == 0:
            return f"[ОШИБКА] Город '{city}' не найден."

        lat = geo_resp["results"][0]["latitude"]
        lon = geo_resp["results"][0]["longitude"]

        # Получаем текущую погоду
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"
        weather_resp = requests.get(weather_url, timeout=10).json()

        temp = weather_resp["current"]["temperature_2m"]
        return f"[ПОГОДА] Сейчас в {city} примерно {temp}°C"
    except Exception as e:
        return f"[ОШИБКА] Ошибка при получении погоды: {e}"   