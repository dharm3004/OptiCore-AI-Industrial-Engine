import pandas as pd
from datetime import datetime


def log_activity(username, action):

    log_file = "logs/activity_log.csv"

    data = {
        "user": username,
        "action": action,
        "time": datetime.now()
    }

    df = pd.DataFrame([data])

    try:
        old = pd.read_csv(log_file)
        df = pd.concat([old, df])
    except:
        pass

    df.to_csv(log_file, index=False)