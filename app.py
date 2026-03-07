import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from datetime import datetime
import requests
import shap

# ---------------------------
# API SETTINGS
# ---------------------------
API_KEY = "85cd98261c221d95c40aa5f9b8ce4f6a"
CITY = "Delhi"

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Energy Forecast", layout="wide")
st.title("⚡ Energy Demand Forecast Dashboard")

# ---------------------------
# LOAD MODEL
# ---------------------------
model = joblib.load("models/xgboost_energy_model_v2.pkl")
features = model.get_booster().feature_names

explainer = shap.TreeExplainer(model)

# ---------------------------
# WEATHER API
# ---------------------------
def get_weather():

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        weather = {
            "temp": data["main"]["temp"],
            "temp_min": data["main"]["temp_min"],
            "temp_max": data["main"]["temp_max"],
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "wind_deg": data["wind"]["deg"],
            "clouds_all": data["clouds"]["all"]
        }

    except:
        weather = {
            "temp":20,
            "temp_min":18,
            "temp_max":22,
            "pressure":1010,
            "humidity":50,
            "wind_speed":5,
            "wind_deg":100,
            "clouds_all":20
        }

    return weather


weather = get_weather()

st.subheader("🌦 Current Weather")

col1,col2,col3,col4 = st.columns(4)

col1.metric("Temperature",f"{weather['temp']} °C")
col2.metric("Humidity",f"{weather['humidity']} %")
col3.metric("Wind Speed",f"{weather['wind_speed']} m/s")
col4.metric("Clouds",f"{weather['clouds_all']} %")

# ---------------------------
# SIDEBAR INPUTS
# ---------------------------
st.sidebar.header("Inputs")

load_lag_1 = st.sidebar.number_input("Previous Hour Load", value=25000)
load_lag_24 = st.sidebar.number_input("Load 24 Hours Ago", value=26000)
load_lag_168 = st.sidebar.number_input("Load 7 Days Ago", value=25500)

solar_forecast = st.sidebar.number_input("Solar Forecast", value=500)
wind_forecast = st.sidebar.number_input("Wind Forecast", value=600)

# ---------------------------
# FEATURE BUILDER
# ---------------------------
def build_features(hour):

    df = pd.DataFrame(np.zeros((1,len(features))),columns=features)

    now = datetime.now()

    df["hour_x"] = hour
    df["day_x"] = now.day
    df["month_x"] = now.month
    df["weekday_x"] = now.weekday()
    df["is_weekend_x"] = int(now.weekday()>=5)

    df["load_lag_1"] = load_lag_1
    df["load_lag_24"] = load_lag_24
    df["load_lag_168"] = load_lag_168

    df["forecast solar day ahead"] = solar_forecast
    df["forecast wind onshore day ahead"] = wind_forecast

    df["generation solar"] = solar_forecast
    df["generation wind onshore"] = wind_forecast

    df["temp"] = weather["temp"]
    df["temp_min"] = weather["temp_min"]
    df["temp_max"] = weather["temp_max"]
    df["pressure"] = weather["pressure"]
    df["humidity"] = weather["humidity"]
    df["wind_speed"] = weather["wind_speed"]
    df["wind_deg"] = weather["wind_deg"]
    df["clouds_all"] = weather["clouds_all"]

    return df


# ---------------------------
# LIVE PREDICTION
# ---------------------------
st.subheader("🔮 Live Prediction")

hour_input = st.slider("Select Hour",0,23,12)

if st.button("Predict Load"):

    X = build_features(hour_input)

    pred = model.predict(X)

    st.success(f"Predicted Load: {pred[0]:,.2f} MW")

    # SHAP LOCAL
    shap_values = explainer.shap_values(X)

    st.subheader("🔍 Prediction Explanation")

    fig, ax = plt.subplots()

    shap.plots.waterfall(
        shap.Explanation(
            values=shap_values[0],
            base_values=explainer.expected_value,
            data=X.iloc[0],
            feature_names=X.columns
        ),
        show=False
    )

    st.pyplot(fig)


# ---------------------------
# 24 HOUR FORECAST
# ---------------------------
st.subheader("📊 24 Hour Load Forecast")

hours = list(range(24))
predictions = []

for h in hours:

    X = build_features(h)
    p = model.predict(X)[0]
    predictions.append(p)

forecast_df = pd.DataFrame({
    "Hour":hours,
    "Predicted_Load":predictions
})

fig = plt.figure()

plt.plot(forecast_df["Hour"],forecast_df["Predicted_Load"],marker="o")

plt.xlabel("Hour")
plt.ylabel("Load (MW)")
plt.title("Next 24 Hour Energy Forecast")

st.pyplot(fig)

st.dataframe(forecast_df)

# ---------------------------
# GLOBAL FEATURE IMPORTANCE
# ---------------------------
st.subheader("🌍 Global Feature Importance")

sample_data = pd.DataFrame(
    np.random.rand(200,len(features)),
    columns=features
)

shap_values_global = explainer.shap_values(sample_data)

fig = plt.figure()

shap.summary_plot(shap_values_global,sample_data,show=False)

st.pyplot(fig)




# ---------------------------
# LOAD HISTORICAL DATA
# ---------------------------

data = pd.read_csv(r"E:\OptiCore_AI\data\processed\merged_energy_weather.csv")

# agar dataset bada ho to sample le lo
data = data.sample(2000, random_state=42)

# ---------------------------
# ACTUAL VS PREDICTED
# ---------------------------

st.subheader("📉 Actual vs Predicted Load")

X_hist = data[features]

y_actual = data["total load actual"]

y_pred = model.predict(X_hist)

fig = plt.figure()

plt.plot(y_actual.values[:200], label="Actual")
plt.plot(y_pred[:200], label="Predicted")

plt.legend()

plt.title("Actual vs Predicted Load")

st.pyplot(fig)

# ---------------------------
# ERROR DISTRIBUTION
# ---------------------------

st.subheader("📊 Prediction Error Distribution")

errors = y_actual.values - y_pred

fig = plt.figure()

plt.hist(errors, bins=40)

plt.xlabel("Error")

plt.ylabel("Frequency")

plt.title("Prediction Error Distribution")

st.pyplot(fig)

# ---------------------------
# RESIDUAL PLOT
# ---------------------------

st.subheader("📈 Residual Plot")

fig = plt.figure()

plt.scatter(y_pred, errors)

plt.xlabel("Predicted Load")

plt.ylabel("Residual Error")

plt.title("Residual Analysis")

st.pyplot(fig)

# ---------------------------
# LOAD VS TEMPERATURE
# ---------------------------

st.subheader("🌡 Load vs Temperature")

fig = plt.figure()

plt.scatter(data["temp"], data["total load actual"])

plt.xlabel("Temperature")

plt.ylabel("Load")

plt.title("Load vs Temperature Relationship")

st.pyplot(fig)