from datetime import datetime
from database import logs_collection


def log_activity(username, action):

    data = {
        "user": username,
        "action": action,
        "time": datetime.now()
    }

    logs_collection.insert_one(data)