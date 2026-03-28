import pandas as pd
import matplotlib.pyplot as plt

def get_data():
    data = [
         {"time": "10:00", "flow": 120, "level": 75, "pressure": 3.2},
         {"time": "10:05", "flow": 135, "level": 73, "pressure": 3.1},
         {"time": "10:10", "flow": 128, "level": 72, "pressure": 3.0},
         {"time": "10:15", "flow": 150, "level": 70, "pressure": 2.9},
     ]
    df = pd.DataFrame(data)
    return df,data

if __name__ == "__main__":
    df,data = get_data()
     




    plt.figure()
    plt.plot(df["time"], df["flow"],marker = 'o')
    plt.title("Water Flow Over Time")
    plt.xlabel("Time")
    plt.ylabel("Flow")
    plt.grid()


    plt.figure()
    plt.plot(df["time"], df["flow"], label="Flow",marker = 'o')
    plt.plot(df["time"], df["level"], label="Level",marker = 'o')
    plt.xlabel("Time")
    plt.ylabel("Flow")
    plt.legend()
    plt.title("Water System Overview")
    plt.grid()


    alert_found = False

    for i in data:
        if i["flow"] > 140:
            print(f"⚠️ High flow detected at {i['time']}")

        if not alert_found:
            print("✅ All values normal")    