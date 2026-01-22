import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ================= API KEY =================
API_KEY = st.secrets["OPENWEATHER_API_KEY"] 
BASE_URL = "https://api.openweathermap.org/data/2.5"
# ==========================================

st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌦",
    layout="wide"
)

# ================= CSS =================
st.markdown("""
<style>

/* ---------- Global ---------- */
body {
    background-color: #f0f2f6;
}
.main {
    padding: 1rem;
    font-family: 'Arial', sans-serif;
}

/* ---------- Header ---------- */
.header {
    background: linear-gradient(90deg, #0f2027, #203a43, #2c5364);
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 20px;
}

/* ---------- Input ---------- */
.stTextInput>div>div>input {
    border-radius: 8px;
    padding: 8px;
    font-size: 14px;
}

/* ---------- Button ---------- */
.stButton>button {
    background: linear-gradient(90deg, #1CB5E0, #000851);
    color: white;
    font-size: 14px;
    font-weight: bold;
    padding: 6px 20px;
    border-radius: 8px;
    border: none;
    margin-top: 5px;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #000851, #1CB5E0);
}

/* ---------- Cards ---------- */
.card {
    background-color: white;
    padding: 12px 10px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 8px;
}
.card h3 {
    margin-bottom: 3px;
    font-size: 16px;
    color: #555;
}
.card p {
    font-size: 22px;
    font-weight: 600;
    color: #111;
}

/* ---------- Section Title ---------- */
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 8px;
    color: #111;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown('<div class="header">🌦 Compact Weather Dashboard</div>', unsafe_allow_html=True)

# ================= INPUT =================
city = st.text_input(
    "Enter City Name",
    placeholder="e.g. Karachi, Lahore, London"
)
search_btn = st.button("🔍 Get Weather")

# ================= FUNCTIONS =================
def fetch_current_weather(city):
    url = f"{BASE_URL}/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    return requests.get(url, params=params).json()

def fetch_forecast_weather(city):
    url = f"{BASE_URL}/forecast"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    return requests.get(url, params=params).json()

# ================= MAIN LOGIC =================
if search_btn and city:
    with st.spinner("Fetching weather data..."):
        current_data = fetch_current_weather(city)
        forecast_data = fetch_forecast_weather(city)

    if current_data.get("cod") != 200:
        st.error("❌ City not found. Enter a valid city.")
    else:
        # -------- Current Weather --------
        temp = current_data["main"]["temp"]
        feels_like = current_data["main"]["feels_like"]
        humidity = current_data["main"]["humidity"]
        wind = current_data["wind"]["speed"]
        condition = current_data["weather"][0]["main"]
        icon = current_data["weather"][0]["icon"]

        # -------- Metric Cards --------
        cols = st.columns(4)
        metrics = [("🌡 Temperature", f"{temp} °C"),
                   ("🤒 Feels Like", f"{feels_like} °C"),
                   ("💧 Humidity", f"{humidity} %"),
                   ("🌬 Wind", f"{wind} m/s")]
        for col, (title, value) in zip(cols, metrics):
            col.markdown(f"""
            <div class="card">
                <h3>{title}</h3>
                <p>{value}</p>
            </div>
            """, unsafe_allow_html=True)

        # -------- Condition --------
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 3])
        with c1:
            st.image(f"https://openweathermap.org/img/wn/{icon}@2x.png")
        with c2:
            st.markdown(f"""
            <div class="card">
                <h3>🌤 Condition</h3>
                <p>{condition}</p>
            </div>
            """, unsafe_allow_html=True)

        # ================= ANALYSIS =================
        st.markdown('<div class="section-title">📊 Forecast Analysis</div>', unsafe_allow_html=True)

        forecast_list = forecast_data["list"]
        times = [datetime.strptime(i["dt_txt"], "%Y-%m-%d %H:%M:%S") for i in forecast_list]
        temps = [i["main"]["temp"] for i in forecast_list]
        humidity_list = [i["main"]["humidity"] for i in forecast_list]
        wind_list = [i["wind"]["speed"] for i in forecast_list]

        # -------- Temperature Trend --------
        fig1, ax1 = plt.subplots(figsize=(9,3))
        ax1.plot(times, temps, marker="o", color="#1f77b4")
        ax1.set_title("Temperature Trend (5-Day Forecast)", fontsize=14)
        ax1.set_ylabel("°C", fontsize=12)
        ax1.tick_params(axis='x', labelrotation=45, labelsize=10)
        ax1.tick_params(axis='y', labelsize=10)
        ax1.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig1, use_container_width=True)

        # -------- Humidity Pie --------
        fig2, ax2 = plt.subplots(figsize=(3,3))
        ax2.pie([humidity, 100-humidity],
                labels=["Humidity","Remaining Air"],
                autopct="%1.0f%%",
                colors=["#1CB5E0","#d3d3d3"])
        ax2.set_title("Humidity", fontsize=12)
        st.pyplot(fig2)

        # -------- Wind Trend --------
        fig3, ax3 = plt.subplots(figsize=(9,3))
        ax3.plot(times, wind_list, marker="o", color="#ff7f0e")
        ax3.set_title("Wind Speed Trend", fontsize=14)
        ax3.set_ylabel("m/s", fontsize=12)
        ax3.tick_params(axis='x', labelrotation=45, labelsize=10)
        ax3.tick_params(axis='y', labelsize=10)
        ax3.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig3, use_container_width=True)
