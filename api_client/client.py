import requests
import streamlit as st

API_KEY = st.secrets["OPENWEATHER_API_KEY"]
BASE_URL = "https://api.openweathermap.org/data/2.5"

def fetch_current_weather(city: str) -> dict:
    url = f"{BASE_URL}/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    return requests.get(url, params=params).json()

def fetch_forecast_weather(city: str) -> dict:
    url = f"{BASE_URL}/forecast"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    return requests.get(url, params=params).json()
