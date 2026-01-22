def extract_current_weather(data: dict) -> dict:
    return {
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "windspeed": data["wind"]["speed"],
        "condition": data["weather"][0]["main"],
        "icon": data["weather"][0]["icon"]
    }

def extract_forecast_weather(data: dict) -> list:
    extracted = []
    for item in data["list"]:
        extracted.append({
            "time": item["dt_txt"],
            "temp": item["main"]["temp"],
            "humidity": item["main"]["humidity"],
            "windspeed": item["wind"]["speed"],
            "condition": item["weather"][0]["main"]
        })
    return extracted
