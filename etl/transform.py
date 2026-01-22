import pandas as pd

def transform_forecast_weather(forecast: list) -> list:
    df = pd.DataFrame(forecast)
    df["time"] = pd.to_datetime(df["time"])
    return df.to_dict(orient="records")
