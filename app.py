import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Weather Forecast Dashboard",
    page_icon="🌦",
    layout="wide"
)

# -----------------------------------
# TITLE
# -----------------------------------
st.title("🌦 Weather Forecast & Alert System")

st.markdown(
    "### Interactive Weather Analytics Dashboard"
)

# -----------------------------------
# LOAD DATA
# -----------------------------------
try:
    df = pd.read_csv("data/weather_data.csv")

except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# -----------------------------------
# DATA CLEANING
# -----------------------------------
required_cols = ['temperature', 'humidity', 'rainfall']

for col in required_cols:

    if col not in df.columns:
        st.error(f"❌ Column '{col}' not found")
        st.stop()

    df[col] = pd.to_numeric(
        df[col],
        errors='coerce'
    ).fillna(0)

# -----------------------------------
# SIDEBAR
# -----------------------------------
st.sidebar.header("📌 Dashboard Controls")

num_rows = st.sidebar.slider(
    "Select Number of Rows",
    min_value=5,
    max_value=len(df),
    value=10
)

graph_type = st.sidebar.selectbox(
    "Select Graph",
    [
        "Temperature",
        "Humidity",
        "Rainfall"
    ]
)

show_data = st.sidebar.checkbox(
    "Show Dataset",
    value=True
)

# -----------------------------------
# FILTERED DATA
# -----------------------------------
filtered_df = df.head(num_rows)

# -----------------------------------
# KPI CARDS
# -----------------------------------
avg_temp = round(filtered_df['temperature'].mean(), 2)
max_temp = round(filtered_df['temperature'].max(), 2)

avg_humidity = round(filtered_df['humidity'].mean(), 2)

total_rainfall = round(filtered_df['rainfall'].sum(), 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("🌡 Avg Temp", avg_temp)
col2.metric("🔥 Max Temp", max_temp)
col3.metric("💧 Avg Humidity", avg_humidity)
col4.metric("🌧 Total Rainfall", total_rainfall)

# -----------------------------------
# DATASET PREVIEW
# -----------------------------------
if show_data:

    st.subheader("📁 Weather Dataset")

    st.dataframe(filtered_df)

# -----------------------------------
# INTERACTIVE CHART
# -----------------------------------
st.subheader("📊 Weather Visualization")

if graph_type == "Temperature":

    st.line_chart(filtered_df['temperature'])

elif graph_type == "Humidity":

    st.bar_chart(filtered_df['humidity'])

elif graph_type == "Rainfall":

    st.area_chart(filtered_df['rainfall'])

# -----------------------------------
# MATPLOTLIB GRAPH
# -----------------------------------
st.subheader("📉 Detailed Weather Trend")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    filtered_df['temperature'],
    marker='o',
    linewidth=2,
    label='Temperature'
)

ax.set_xlabel("Index")
ax.set_ylabel("Temperature")
ax.set_title("Temperature Trend")

ax.legend()

st.pyplot(fig)

# -----------------------------------
# WEATHER ALERTS
# -----------------------------------
st.subheader("🚨 Weather Alerts")

if max_temp > 40:
    st.error("🔥 High Temperature Alert!")

if total_rainfall > 50:
    st.warning("🌧 Heavy Rainfall Alert!")

if avg_humidity > 80:
    st.info("💧 High Humidity Detected")

# -----------------------------------
# DOWNLOAD BUTTON
# -----------------------------------
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇ Download Weather Data",
    data=csv,
    file_name='weather_data.csv',
    mime='text/csv'
)

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("---")

st.markdown(
    "👨‍💻 Developed by **Jatin Gujarathi**"
)