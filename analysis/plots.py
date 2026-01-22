import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def plot_current_vs_forecast(current, forecast):
    times = [datetime.now()] + [
        datetime.strptime(item["time"], "%Y-%m-%d %H:%M:%S")
        for item in forecast
    ]
    temps = [current["temperature"]] + [item["temp"] for item in forecast]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(times, temps, marker="o")
    ax.set_title("Current vs Forecast Temperature")
    ax.set_ylabel("Temperature (°C)")
    ax.grid(True)
    return fig

def plot_daily_avg_temperature(forecast):
    df = pd.DataFrame(forecast)
    df["date"] = df["time"].dt.date
    daily_avg = df.groupby("date")["temp"].mean()

    fig, ax = plt.subplots()
    ax.plot(daily_avg.index, daily_avg.values, marker="o")
    ax.set_title("5-Day Average Temperature")
    ax.grid(True)
    return fig

def plot_humidity_pie(humidity):
    fig, ax = plt.subplots()
    ax.pie(
        [humidity, 100 - humidity],
        labels=["Humidity", "Remaining Air"],
        autopct="%1.1f%%"
    )
    return fig

def plot_wind_speed_trend(forecast):
    times = forecast and [item["time"] for item in forecast]
    speeds = [item["windspeed"] for item in forecast]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(times, speeds, marker="o")
    ax.set_title("Wind Speed Trend")
    ax.set_ylabel("m/s")
    ax.grid(True)
    return fig
