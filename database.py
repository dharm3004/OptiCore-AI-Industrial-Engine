import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv("E:/OptiCore_AI/.env")

MONGO_URI = os.getenv("MONGO_URI")


client = MongoClient(MONGO_URI)

db = client["opticore_ai"]

users_collection = db["users"]
logs_collection = db["activity_logs"]
predictions_collection = db["predictions"]