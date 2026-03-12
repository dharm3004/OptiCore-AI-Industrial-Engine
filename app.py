import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import requests
import shap
import plotly.express as px
import plotly.graph_objects as go
import time
from sklearn.metrics import mean_absolute_error, r2_score

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Energy Forecast Dashboard", layout="wide")

st.title("⚡ Energy Demand Forecast Dashboard")

# --------------------------------------------------
# REAL TIME DASHBOARD
# --------------------------------------------------
auto_refresh = st.sidebar.checkbox("🔄 Live Monitoring")

if auto_refresh:
    time.sleep(30)
    st.rerun()


# --------------------------------------------------
# API SETTINGS
# --------------------------------------------------
API_KEY = "YOUR_API_KEY"
CITY = "Delhi"

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------
model = joblib.load("models/xgboost_energy_model_v2.pkl")

features = model.get_booster().feature_names

explainer = shap.TreeExplainer(model)

# --------------------------------------------------
# WEATHER API
# --------------------------------------------------
def get_weather():

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        r = requests.get(url)
        data = r.json()

        weather = {
            "temp":data["main"]["temp"],
            "humidity":data["main"]["humidity"],
            "wind_speed":data["wind"]["speed"],
            "clouds":data["clouds"]["all"]
        }

    except:

        weather = {
            "temp":20,
            "humidity":50,
            "wind_speed":5,
            "clouds":20
        }

    return weather


weather = get_weather()

# --------------------------------------------------
# WEATHER KPI
# --------------------------------------------------
st.subheader("🌦 Live Weather")

c1,c2,c3,c4 = st.columns(4)

c1.metric("🌡 Temperature",f"{weather['temp']} °C")
c2.metric("💧 Humidity",f"{weather['humidity']} %")
c3.metric("🌬 Wind Speed",f"{weather['wind_speed']} m/s")
c4.metric("☁ Cloud Cover",f"{weather['clouds']} %") 

# --------------------------------------------------
# SIDEBAR INPUTS
# --------------------------------------------------
st.sidebar.header("⚙ Prediction Inputs")

load_lag_1 = st.sidebar.number_input("Previous Hour Load",25000)
load_lag_24 = st.sidebar.number_input("Load 24 Hours Ago",26000)
load_lag_168 = st.sidebar.number_input("Load 7 Days Ago",25500)

solar_forecast = st.sidebar.number_input("Solar Forecast",500)
wind_forecast = st.sidebar.number_input("Wind Forecast",600)

# --------------------------------------------------
# FEATURE BUILDER
# --------------------------------------------------
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
    df["humidity"] = weather["humidity"]
    df["wind_speed"] = weather["wind_speed"]

    return df

# --------------------------------------------------
# LIVE PREDICTION
# --------------------------------------------------
st.subheader("🔮 Live Prediction")

hour = st.slider("Select Hour",0,23,12)

if st.button("Predict Load"):

    X = build_features(hour)

    pred = model.predict(X)[0]

    st.success(f"⚡ Predicted Load: {pred:,.2f} MW")

    # INTERACTIVE GAUGE
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pred,
        title={'text': "Energy Demand"},
        gauge={
            'axis': {'range': [None, 60000]},
            'bar': {'color': "orange"},
            'steps': [
                {'range': [0,20000], 'color': "green"},
                {'range': [20000,40000], 'color': "yellow"},
                {'range': [40000,60000], 'color': "red"}
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    # SHAP explanation
    shap_values = explainer.shap_values(X)

    st.subheader("🔍 Prediction Explanation")

    fig = plt.figure()

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

# --------------------------------------------------
# 24 HOUR FORECAST
# --------------------------------------------------
st.subheader("📊 24 Hour Forecast")

hours = list(range(24))
preds = []

for h in hours:
    X = build_features(h)
    p = model.predict(X)[0]
    preds.append(p)

forecast_df = pd.DataFrame({
    "Hour":hours,
    "Load":preds
})

fig = px.line(
    forecast_df,
    x="Hour",
    y="Load",
    markers=True,
    title="Next 24 Hour Energy Forecast"
)
st.plotly_chart(fig, use_container_width=True)

st.dataframe(forecast_df,use_container_width=True)



# --------------------------------------------------
# Peak Demand Insight
# --------------------------------------------------

peak_hour = forecast_df.loc[forecast_df["Load"].idxmax()]
peak_load = forecast_df["Load"].max()   # ← ye line add karo

st.subheader("⚡ Peak Demand Insight")

st.info(
    f"Highest demand expected at Hour {int(peak_hour['Hour'])} "
    f"with {peak_hour['Load']:,.0f} MW"
)


# --------------------------------------------------
# Demand Alert System
# --------------------------------------------------

st.subheader("🚨 Demand Alert System")

if peak_load > 38000:
    st.error("⚠ High Demand Expected — Grid Load May Surge")

elif peak_load > 32000:
    st.warning("⚡ Moderate Demand Expected")

else:
    st.success("✅ Demand Within Normal Range")
    
# --------------------------------------------------
# ENERGY SYSTEM KPI
# --------------------------------------------------

st.subheader("📊 Energy System Overview")

k1, k2, k3, k4 = st.columns(4)

current_load = forecast_df["Load"].iloc[hour]
peak_load = forecast_df["Load"].max()
min_load = forecast_df["Load"].min()
renewable = solar_forecast + wind_forecast

k1.metric("⚡ Current Demand", f"{current_load:,.0f} MW")
k2.metric("📈 Peak Load", f"{peak_load:,.0f} MW")
k3.metric("📉 Minimum Load", f"{min_load:,.0f} MW")
k4.metric("🌞 Renewable Forecast", f"{renewable} MW")


# --------------------------------------------------
# 🌱 Renewable Energy Contribution
# --------------------------------------------------

st.subheader("🌱 Renewable Energy Contribution")

renewable_total = solar_forecast + wind_forecast
total_energy = current_load

renewable_percent = (renewable_total / total_energy) * 100

st.metric("Renewable Share", f"{renewable_percent:.1f}%")


# --------------------------------------------------
#  Renewable vs Demand
# --------------------------------------------------

st.subheader("🌱 Renewable vs Demand")

energy_df = pd.DataFrame({
    "Source":["Solar","Wind","Total Demand"],
    "Value":[solar_forecast, wind_forecast, current_load]
})

fig = px.bar(
    energy_df,
    x="Source",
    y="Value",
    title="Energy Mix vs Demand"
)

st.plotly_chart(fig,use_container_width=True)


# --------------------------------------------------
# 🤖 AI Energy Insights
# --------------------------------------------------
st.subheader("🤖 AI Energy Insights")

insight = f"""
Peak demand expected around {int(peak_hour['Hour'])}:00.

Current renewable contribution is {renewable_percent:.1f}% of total demand.

Higher temperature ({weather['temp']}°C) may increase electricity consumption.
"""

st.info(insight)

# --------------------------------------------------
# HOURLY HEATMAP
# --------------------------------------------------
st.subheader("🔥 Hourly Energy Demand Heatmap")

heatmap_data = forecast_df.copy()
heatmap_data["Day"] = "Today"

pivot = heatmap_data.pivot(index="Day", columns="Hour", values="Load")

fig = plt.figure(figsize=(18,3))

sns.heatmap(
    pivot,
    cmap="coolwarm",
    annot=True,
    fmt=".0f",
    linewidths=0.5,
    annot_kws={"rotation":90}
)

st.pyplot(fig)

# --------------------------------------------------
# WEEKLY HEATMAP
# --------------------------------------------------
st.subheader("🔥 Weekly Energy Demand Heatmap")

days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

heatmap_matrix = []

for d in range(7):

    daily_load = []

    for h in range(24):

        X = build_features(h)
        p = model.predict(X)[0]
        daily_load.append(p)

    heatmap_matrix.append(daily_load)

heatmap_df = pd.DataFrame(
    heatmap_matrix,
    index=days,
    columns=list(range(24))
)

fig = plt.figure(figsize=(18,5))

sns.heatmap(
    heatmap_df,
    cmap="coolwarm",
    annot=True,
    fmt=".0f",
    linewidths=0.3,
    annot_kws={"rotation":90}
)

st.pyplot(fig)

# --------------------------------------------------
# GLOBAL FEATURE IMPORTANCE
# --------------------------------------------------
st.subheader("🌍 Global Feature Importance")

sample = pd.DataFrame(
    np.random.rand(200,len(features)),
    columns=features
)

shap_vals = explainer.shap_values(sample)

fig = plt.figure()

shap.summary_plot(shap_vals,sample,show=False)

st.pyplot(fig)

# --------------------------------------------------
# HISTORICAL DATA
# --------------------------------------------------

data = pd.read_csv("data/processed/merged_energy_weather.csv")

data = data.drop_duplicates()

data = data.dropna(subset=["total load actual"])

if len(data) > 2000:
    data = data.sample(2000)

# --------------------------------------------------
# ACTUAL VS PREDICTED
# --------------------------------------------------
st.subheader("📉 Actual vs Predicted")

X_hist = data[features].fillna(0)
y_actual = data["total load actual"]

y_pred = model.predict(X_hist)

fig = plt.figure()

plt.plot(y_actual.values[:200],label="Actual")
plt.plot(y_pred[:200],label="Predicted")

plt.legend()

st.pyplot(fig)


# --------------------------------------------------
# 📊 Model Performance KPI
# --------------------------------------------------
# remove NaN before metrics
eval_df = pd.DataFrame({
    "actual": y_actual,
    "pred": y_pred
}).dropna()

mae = mean_absolute_error(eval_df["actual"], eval_df["pred"])
r2 = r2_score(eval_df["actual"], eval_df["pred"])

st.subheader("📊 Model Performance")

m1, m2 = st.columns(2)

m1.metric("MAE", f"{mae:,.2f}")
m2.metric("R² Score", f"{r2:.3f}")
# --------------------------------------------------
# ERROR DISTRIBUTION
# --------------------------------------------------
st.subheader("📊 Error Distribution")

errors = y_actual - y_pred

fig = plt.figure()

plt.hist(errors,bins=40)

st.pyplot(fig)


# --------------------------------------------------
# FORECAST Confidence Range
# --------------------------------------------------
 
st.subheader("📉 Forecast Confidence Range")

std = np.std(errors)

upper = forecast_df["Load"] + std
lower = forecast_df["Load"] - std

fig = plt.figure()

plt.plot(forecast_df["Hour"], forecast_df["Load"], label="Prediction")
plt.fill_between(
    forecast_df["Hour"],
    lower,
    upper,
    alpha=0.3,
    label="Confidence Range"
)

plt.legend()

st.pyplot(fig)


# --------------------------------------------------
# RESIDUAL PLOT
# --------------------------------------------------
st.subheader("📈 Residual Analysis")

fig = plt.figure()

plt.scatter(y_pred,errors)

plt.xlabel("Predicted")
plt.ylabel("Residual")

st.pyplot(fig)

# --------------------------------------------------
# LOAD VS TEMP
# --------------------------------------------------
st.subheader("🌡 Load vs Temperature")

fig = plt.figure()

plt.scatter(data["temp"],data["total load actual"])

plt.xlabel("Temperature")
plt.ylabel("Load")

st.pyplot(fig)




# --------------------------------------------------
# Correlation Heatmap (Analytics Insight)
# --------------------------------------------------

st.subheader("📊 Correlation Heatmap")

corr = data.corr(numeric_only=True)

fig = plt.figure(figsize=(12,8))

sns.heatmap(
    corr,
    cmap="coolwarm",
    annot=False
)

st.pyplot(fig)

