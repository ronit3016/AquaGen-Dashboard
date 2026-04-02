import streamlit as st
import matplotlib.pyplot as plt
import requests
import time
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=3000, key="datarefresh")

st.set_page_config(
    page_title="AquaGen Dashboard",   # 🔥 this changes browser tab name
    page_icon="💧",
    layout="wide"
)
# -------------------------------
# 🔹 Title
# -------------------------------
st.title("💧 AquaGen Mini Dashboard")

# -------------------------------
# 🔹 API Call
# -------------------------------
response = requests.get("https://aquagen-dashboard.onrender.com/data")
data = response.json()

df = pd.DataFrame(data)

# -------------------------------
# 🔹 Alert Logic (compute once)
# -------------------------------
alerts = []

for i in range(1, len(data)):
    prev = data[i-1]["flow"]
    curr = data[i]["flow"]

    # detect sudden jump (20% increase)
    if curr > prev * 1.2:
        alerts.append(data[i])

recent_alerts = alerts[-3:]

st.divider()
st.subheader("📜 Alert History")

# show last 10 alerts from full history
history_alerts = []

for i in range(1, len(data)):
    prev = data[i-1]["flow"]
    curr = data[i]["flow"]

    if curr > prev * 1.2:
        history_alerts.append(data[i])

if history_alerts:
    for a in history_alerts[-10:]:
        st.warning(f"Spike detected at {a['time']}")
else:
    st.success("No past anomalies")

# -------------------------------
# 🧾 System Summary (TOP PRIORITY)
# -------------------------------
st.subheader("🧾 System Summary")

col1, col2 = st.columns(2)

with col1:
    if alerts:
        st.error(f"🔴 {len(alerts)} Active Issues")
    else:
        st.success("🟢 System Stable")

with col2:
    if len(df) > 1:
        if df["flow"].iloc[-1] > df["flow"].iloc[0]:
            st.info("📈 Increasing Usage Trend")
        else:
            st.info("📉 Decreasing Usage Trend")
    else:
        st.info("Not enough data yet")

st.divider()

# -------------------------------
# 🚨 Active Alerts
# -------------------------------
st.subheader("🚨 Active Alerts")

if recent_alerts:
    for a in recent_alerts:
        st.error(f"High flow at {a['time']}")
else:
    st.success("No active alerts")

st.divider()

# -------------------------------
# 📌 Current Metrics
# -------------------------------
st.subheader("📌 Current Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Flow", df["flow"].iloc[-1])
col2.metric("Level", df["level"].iloc[-1])
col3.metric("Pressure", df["pressure"].iloc[-1])

st.divider()

# -------------------------------
# 📈 Graph
# -------------------------------
# -------------------------------
# 📈 Graph
# -------------------------------
st.subheader("📈 Water System Trends")

fig, ax = plt.subplots(figsize=(6, 3))

ax.plot(df["time"], df["flow"], label="Flow", marker='o')
ax.plot(df["time"], df["level"], label="Level", marker='o')
ax.plot(df["time"], df["pressure"], label="Pressure", marker='o')

ax.set_xlabel("Time")
ax.set_ylabel("Values")
ax.set_title("System Trends")
ax.grid(True)

ax.set_xticks(range(0, len(df), max(1, len(df)//10)))
ax.tick_params(axis='x', rotation=45)

# create space inside frame
fig.subplots_adjust(left=0.2, right=0.75, bottom=0.35, top=0.85)

# move legend OUTSIDE into white space
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

st.pyplot(fig, use_container_width=False)

# -------------------------------
# 📈 Insights
# -------------------------------
st.subheader("📈 Insights")

if len(df) > 1:
    if df["flow"].iloc[-1] > df["flow"].iloc[0]:
        st.info("📈 Flow is increasing over time")
    else:
        st.info("📉 Flow is decreasing")
else:
    st.info("Not enough data yet")

# -------------------------------
# 📊 Raw Data (LOW PRIORITY → bottom)
# -------------------------------
st.subheader("📊 Raw Data")
st.write(df)

