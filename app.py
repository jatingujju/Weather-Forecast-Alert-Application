import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    "### Interactive Weather Monitoring Dashboard"
)

# -----------------------------------
# LOAD DATASET
# -----------------------------------
try:
    df = pd.read_csv("data/weather_data.csv")

except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# -----------------------------------
# SIDEBAR INPUTS
# -----------------------------------
st.sidebar.header("📌 Enter Weather Details")

# LOCATION SELECTOR
location = st.sidebar.selectbox(
    "📍 Select Location",
    [
        "Mumbai",
        "Delhi",
        "Pune",
        "Bangalore",
        "Hyderabad",
        "Chennai",
        "Kolkata"
    ]
)

# TEMPERATURE INPUT
temperature = st.sidebar.number_input(
    "🌡 Temperature (°C)",
    min_value=-10,
    max_value=60,
    value=30
)

# HUMIDITY INPUT
humidity = st.sidebar.slider(
    "💧 Humidity (%)",
    min_value=0,
    max_value=100,
    value=70
)

# RAINFALL INPUT
rainfall = st.sidebar.number_input(
    "🌧 Rainfall (mm)",
    min_value=0,
    max_value=500,
    value=10
)

# -----------------------------------
# USER INPUT DATAFRAME
# -----------------------------------
weather_data = pd.DataFrame({
    "Location": [location],
    "Temperature": [temperature],
    "Humidity": [humidity],
    "Rainfall": [rainfall]
})

# -----------------------------------
# SHOW ENTERED DATA
# -----------------------------------
st.subheader("📁 Entered Weather Data")

st.dataframe(weather_data)

# -----------------------------------
# KPI CARDS
# -----------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📍 Location",
    location
)

col2.metric(
    "🌡 Temperature",
    f"{temperature} °C"
)

col3.metric(
    "💧 Humidity",
    f"{humidity}%"
)

col4.metric(
    "🌧 Rainfall",
    f"{rainfall} mm"
)

# -----------------------------------
# INTERACTIVE CHARTS
# -----------------------------------
st.subheader("📊 Weather Visualization")

st.bar_chart(weather_data.set_index("Location"))

# -----------------------------------
# MATPLOTLIB GRAPH
# -----------------------------------
st.subheader("📉 Detailed Weather Analysis")

fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(
    ["Temperature", "Humidity", "Rainfall"],
    [temperature, humidity, rainfall]
)

ax.set_title(f"Weather Analysis - {location}")

st.pyplot(fig)

# -----------------------------------
# WEATHER ALERT SYSTEM
# -----------------------------------
st.subheader("🚨 Weather Alert System")

if st.button("Generate Weather Alert"):

    if temperature > 40:
        st.error("🔥 High Temperature Alert!")

    elif rainfall > 100:
        st.warning("🌧 Heavy Rainfall Alert!")

    elif humidity > 85:
        st.info("💧 High Humidity Alert!")

    else:
        st.success("✅ Weather Conditions Normal")

# -----------------------------------
# HISTORICAL DATASET
# -----------------------------------
st.subheader("📋 Historical Weather Dataset")

st.dataframe(df.head())

# -----------------------------------
# LINE CHART
# -----------------------------------
st.subheader("🌡 Historical Temperature Trend")

if "temperature" in df.columns:
    st.line_chart(df["temperature"])

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("---")

st.write("👨‍💻 Developed by Jatin Gujarathi")