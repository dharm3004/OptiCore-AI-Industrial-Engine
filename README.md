<div align="center">

# ⚡ OptiCore AI
### Intelligent Energy Demand Forecasting System

[![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.55-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![XGBoost](https://img.shields.io/badge/XGBoost-3.2-orange?style=for-the-badge)](https://xgboost.readthedocs.io)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?style=for-the-badge&logo=mongodb)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Dharmesh%20Rathod-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/dharmesh-rathod19)
[![GitHub](https://img.shields.io/badge/GitHub-dharm3004-181717?style=for-the-badge&logo=github)](https://github.com/dharm3004)

<br/>

> **Predict. Analyze. Optimize.** — A production-grade ML dashboard that forecasts electricity demand using XGBoost + real-time weather data, with explainable AI, role-based access control, and PDF report export.

<br/>

[📂 Project Structure](#-project-structure) · [⚙️ Setup](#️-setup--installation) · [📊 Model Performance](#-model-performance) · [🖼️ Screenshots](#️-screenshots) · [👨‍💻 Author](#-author)

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Key Features](#-key-features)
- [Tech Stack](#️-tech-stack)
- [Project Architecture](#-project-architecture)
- [Project Structure](#-project-structure)
- [Setup & Installation](#️-setup--installation)
- [Environment Variables](#-environment-variables)
- [How It Works](#-how-it-works)
- [Model Performance](#-model-performance)
- [API Reference](#-api-reference)
- [Role-Based Access](#-role-based-access-control)
- [Screenshots](#️-screenshots)
- [Future Enhancements](#-future-enhancements)
- [Why This Project Matters](#-why-this-project-matters)
- [Contributing](#-contributing)
- [Author](#-author)

---

## 🔍 Overview

**OptiCore AI** is an end-to-end intelligent energy demand forecasting platform built for real-world grid management scenarios. It combines a trained **XGBoost ML model** with **live OpenWeather API data** to predict hourly electricity consumption and deliver actionable grid management insights.

The platform goes beyond simple prediction — it offers **SHAP-based explainability**, **Power BI-style PDF exports**, **weekly demand heatmaps**, and a complete **admin control panel** with activity logging, making it suitable for production deployment in energy sector organizations.

🔗 **GitHub Repo:** [github.com/dharm3004/OptiCore-AI-Industrial-Engine](https://github.com/dharm3004/OptiCore-AI-Industrial-Engine)

---

## 🎯 Problem Statement

Energy demand is highly volatile — influenced by weather, time-of-day, seasonality, and human behavior. Traditional rule-based forecasting systems:

- ❌ Cannot capture complex non-linear patterns
- ❌ Lack real-time adaptability
- ❌ Provide no explainability for predictions
- ❌ Miss weather-demand correlations

**OptiCore AI solves this** by training an XGBoost model on merged energy + weather data (Spain grid, ~36,000 records) and deploying it in an interactive Streamlit dashboard with live weather integration and transparent AI reasoning.

---

## 🧠 Key Features

### 🔮 Smart Demand Prediction
- Hourly energy demand forecasting using a trained XGBoost model
- Lag-based feature engineering (1-hour, 24-hour, 7-day historical loads)
- Solar and wind forecast inputs for renewable-aware predictions
- Confidence interval bands around every forecast

### 🌦️ Real-Time Weather Integration
- Live data from **OpenWeather API** (temperature, humidity, wind speed, cloud cover)
- Weather KPIs displayed as live metrics on the dashboard
- Weather features directly influence model predictions

### 📊 Advanced Visualizations (10+ Charts)
- 24-hour demand forecast line chart
- Hourly demand heatmap (today)
- Weekly demand heatmap (7-day × 24-hour grid)
- Renewable vs. demand bar chart
- Actual vs. predicted comparison plot
- Error distribution histogram
- Forecast confidence range with shaded bands
- Residual scatter plot
- Load vs. temperature scatter analysis
- Full correlation heatmap

### 🤖 Explainable AI (XAI)
- **SHAP TreeExplainer** for global feature importance
- Summary plot showing which features drive predictions most
- Transparent reasoning behind every forecast

### 🧠 AI Decision Engine
- Automatic risk classification: `LOW / MODERATE / HIGH`
- Smart actionable recommendations (load balancing, generation increase)
- Real-time renewable share percentage tracking
- Live KPIs: Current Demand, Peak Load, Min Load, Renewable Forecast

### 📄 Power BI-Style PDF Export
- One-click export of all dashboard charts to a **landscape multi-chart PDF**
- ReportLab-based grid layout (3 charts per row)
- Ready for boardroom presentations

### 🔐 Secure Authentication System
- **bcrypt password hashing** — no plaintext passwords stored
- Session state management via Streamlit
- Secure login/logout flow with MongoDB user storage

### 👑 Role-Based Access Control (RBAC)
- `Admin` → Full access: predictions, admin panel, user registration
- `Analyst` → Dashboard and prediction access
- `Viewer` → Read-only dashboard access

### 📜 Admin Control Panel
- Complete activity log viewer with user-based filtering
- Bar charts for user activity and system actions
- System metrics: total actions, unique users, log records
- Download logs as CSV with live refresh

### 🗄️ MongoDB Atlas Integration
- Users collection with hashed credentials and role metadata
- Activity logs collection (user, action, timestamp)
- Scalable cloud database — zero local DB setup

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / UI** | Streamlit 1.55 |
| **ML Model** | XGBoost 3.2, Scikit-learn 1.8 |
| **Explainability** | SHAP |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly, Matplotlib, Seaborn |
| **Weather API** | OpenWeatherMap API |
| **Authentication** | bcrypt, Streamlit session state |
| **Database** | MongoDB Atlas (via PyMongo) |
| **PDF Export** | ReportLab, Plotly Kaleido |
| **Environment** | python-dotenv |
| **Language** | Python 3.13 |

---

## 🏗️ Project Architecture

```
User Login (bcrypt auth + MongoDB)
        │
        ▼
Streamlit Dashboard ──── OpenWeather API (live weather KPIs)
        │
        ├── Sidebar Inputs (lag loads, solar, wind forecast)
        │
        ├── Feature Builder ──── XGBoost Model ──── SHAP Explainer
        │                              │
        │                              ▼
        │                     24-Hour Forecast Array
        │                              │
        ├── AI Decision Engine ──── LOW / MODERATE / HIGH RISK
        │                       └── Recommended Action
        │
        ├── Historical Analysis ──── merged_energy_weather.csv
        │
        ├── Admin Panel ──── MongoDB Logs Collection
        │
        └── PDF Export ──── ReportLab Grid Layout
```

---

## 📂 Project Structure

```
OptiCore_AI/
│
├── app.py                          # Main Streamlit application
├── database.py                     # MongoDB Atlas connection
├── requirements.txt                # All dependencies
├── .env                            # Environment variables (not tracked)
│
├── auth/
│   ├── login.py                    # bcrypt login system
│   ├── register.py                 # Admin user registration
│   └── logger.py                   # Activity logger to MongoDB
│
├── admin/
│   └── admin_panel.py              # Admin control panel UI
│
├── models/
│   └── xgboost_energy_model_v2.pkl # Trained XGBoost model
│
├── data/
│   └── processed/
│       ├── energy_dataset.csv      # Processed Spain energy data
│       ├── weather_features.csv    # Processed weather data
│       └── merged_energy_weather.csv # Merged training dataset (36,002 rows)
│
├── screenshots/                    # Dashboard screenshots
│
└── notebooks/
    ├── 03_dataset_merge.ipynb      # Energy + weather data merging
    └── 04_model_training.ipynb     # XGBoost model training pipeline
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- MongoDB Atlas account (free tier works)
- OpenWeatherMap API key (free tier works)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/dharm3004/OptiCore-AI-Industrial-Engine.git
cd OptiCore-AI-Industrial-Engine
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
Create a `.env` file in the root directory:
```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/opticore
OPENWEATHER_API_KEY=your_openweather_api_key
CITY=Madrid
```

### 5️⃣ Run the Application
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `MONGO_URI` | MongoDB Atlas connection string | ✅ Yes |
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | ✅ Yes |
| `CITY` | City for live weather data | ✅ Yes |

> ⚠️ Never commit your `.env` file. Add it to `.gitignore`.

---

## 🔄 How It Works

### Data Pipeline
1. **Raw Data**: Spain electricity grid data (`energy_dataset.csv`) + multi-city weather data (`weather_features.csv`)
2. **Merge** (`03_dataset_merge.ipynb`): Filter Madrid weather → merge on timestamp → 36,002 rows × 58 features
3. **Feature Engineering** (`04_model_training.ipynb`): Lag features, time-based features, weather features
4. **Model Training**: XGBoost regressor trained and saved as `xgboost_energy_model_v2.pkl`

### Prediction Flow
```
Sidebar Inputs (lag loads + solar + wind)
    → Feature Builder
    → XGBoost Model
    → 24-Hour Forecast Array
    → AI Decision Engine (Risk Classification)
    → SHAP Explainability Plot
```

---

## 📈 Model Performance

| Metric | Value |
|---|---|
| **Algorithm** | XGBoost Regressor v2 |
| **Training Data** | 36,002 rows (Spain grid 2015–2018) |
| **Features** | Lag loads, time features, weather variables |
| **MAE** | *(displayed live in dashboard)* |
| **R² Score** | *(displayed live in dashboard)* |

> Model performance metrics (MAE + R²) are computed live in the dashboard on each session using the merged historical dataset.

---

## 🔌 API Reference

### OpenWeatherMap Integration

**Endpoint:**
```
GET https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric
```

| Field | Description |
|---|---|
| `main.temp` | Current temperature (°C) |
| `main.humidity` | Humidity (%) |
| `wind.speed` | Wind speed (m/s) |
| `clouds.all` | Cloud cover (%) |

---

## 🔐 Role-Based Access Control

| Role | Dashboard | Predictions | Admin Panel | User Registration |
|---|---|---|---|---|
| **Admin** 👑 | ✅ | ✅ | ✅ | ✅ |
| **Analyst** 📊 | ✅ | ✅ | ❌ | ❌ |
| **Viewer** 👀 | ✅ | ❌ | ❌ | ❌ |

> Roles are stored in MongoDB Atlas. Only admins can create new users via the in-app registration panel.

---

## 🖼️ Screenshots

### 🔐 Login Page
![Login Page](screenshots/loginpage.png)

---

### ⚡ Energy Demand Forecast Dashboard + Live Weather KPIs
![Dashboard](screenshots/energy_dashboard_and_weather_kpi.png)

---

### 📈 24-Hour Energy Forecast
![24 Hour Forecast](screenshots/24_hour_forecast.png)

---

### 🔥 Weekly Energy Demand Heatmap (7-Day × 24-Hour Grid)
![Weekly Heatmap](screenshots/Energy_forcast_weekly_heat_map.png)

---

### 🧠 AI Decision Engine + Energy System Overview
![System Overview](screenshots/system_overview.png)

---

### ⚙️ Admin Control Panel — Activity Logs & User Analytics
![Admin Panel](screenshots/Admin_panel.png)

---

## 🚀 Future Enhancements

- [ ] 🌍 Multi-city forecasting (beyond Madrid)
- [ ] 📄 Automated scheduled PDF report emails
- [ ] 📊 Prediction history tracking per user
- [ ] ⚡ Real-time grid anomaly detection alerts
- [ ] 🔔 Slack / email notifications for HIGH RISK events
- [ ] 🐳 Docker containerization for easy deployment
- [ ] ☁️ Deploy to Streamlit Cloud / HuggingFace Spaces

---

## 💼 Why This Project Matters

| Skill | Demonstrated By |
|---|---|
| **End-to-end ML deployment** | Training → pickle → live inference in Streamlit |
| **Real-time data integration** | Live OpenWeather API calls per session |
| **Feature engineering** | Lag features, temporal encoding, weather variables |
| **Explainable AI** | SHAP TreeExplainer with summary plots |
| **Secure authentication** | bcrypt hashing, session state, RBAC |
| **Database integration** | MongoDB Atlas for users and activity logs |
| **Data pipeline** | Jupyter notebooks → merge → train → deploy |
| **Report generation** | ReportLab PDF with multi-chart grid layout |
| **Production architecture** | Modular codebase with auth, admin, and logging layers |

---

## 🤝 Contributing

Contributions are welcome!

```bash
# 1. Fork the repo
# https://github.com/dharm3004/OptiCore-AI-Industrial-Engine

# 2. Create your branch
git checkout -b feature/YourFeature

# 3. Commit changes
git commit -m 'Add YourFeature'

# 4. Push
git push origin feature/YourFeature

# 5. Open a Pull Request
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👨‍💻 Author

**Dharmesh Rathod**
*Aspiring Data Scientist | ML Engineer | Data Analyst*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Dharmesh%20Rathod-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/dharmesh-rathod19)
[![GitHub](https://img.shields.io/badge/GitHub-dharm3004-181717?style=flat&logo=github)](https://github.com/dharm3004)
[![Email](https://img.shields.io/badge/Email-dharmrathod194%40gmail.com-red?style=flat&logo=gmail)](mailto:dharmrathod194@gmail.com)
[![Repo](https://img.shields.io/badge/Repo-OptiCore--AI-orange?style=flat&logo=github)](https://github.com/dharm3004/OptiCore-AI-Industrial-Engine)

---

<div align="center">

### ⭐ If OptiCore AI impressed you, please star the repo!

*It motivates continued development and helps others discover this project.*

**[⭐ Star on GitHub](https://github.com/dharm3004/OptiCore-AI-Industrial-Engine)**

</div>