import joblib
import pandas as pd

model = joblib.load("models/xgboost_energy_model.pkl")

data = pd.read_csv("new_data.csv")

predictions = model.predict(data)

print(predictions)
