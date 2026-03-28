from fastapi import FastAPI
from backend import get_data
import random
from datetime import datetime, timedelta

app = FastAPI()

# 🔥 Global storage (simulating database)
data_store = []

@app.get("/")
def home():
    return {"message": "AquaGen API running"}

@app.get("/data")
def get_sensor_data():
    global data_store

    # First time → initialize
    if not data_store:
        df, data = get_data()
        data_store = data
    else:
        last = data_store[-1]

        last_time = datetime.strptime(last["time"], "%H:%M")
        new_time = last_time + timedelta(minutes=5)

        new_entry = {
            "time": new_time.strftime("%H:%M"),
            "flow": last["flow"] + random.randint(-5, 10),
            "level": last["level"] - random.randint(0, 2),
            "pressure": round(last["pressure"] + random.uniform(-0.1, 0.1), 2)
        }

        data_store.append(new_entry)

    return data_store