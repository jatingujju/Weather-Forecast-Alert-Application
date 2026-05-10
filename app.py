import os
import smtplib
from email.mime.text import MIMEText

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

from dotenv import load_dotenv
from datetime import datetime

# =========================
# LOAD ENV VARIABLES
# =========================
load_dotenv()

API_KEY = os.getenv("API_KEY")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# =========================
# EMAIL ALERT FUNCTION
# =========================
def send_email_alert(subject, message):

    try:

        msg = MIMEText(message)

        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        server.send_message(msg)

        server.quit()

        st.success("📧 Email alert sent successfully!")

    except Exception as e:

        st.error(f"Email Error: {e}")


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Advanced Weather Forecast Dashboard",
    page_icon="🌦",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(to right, #141e30, #243b55);
        color: white;
    }

    h1, h2, h3 {
        color: #00e5ff;
    }

    div[data-testid="metric-container"] {
        background-color: rgba(255,255,255,0.08);
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    div[data-testid="stSidebar"] {
        background-color: #0f172a;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# TITLE
# =========================
st.title("🌦 Advanced Weather Forecast & Alert Dashboard")

st.markdown(
    "### Real-Time Weather Monitoring, Forecasting & Alert System"
)

# =========================
# SIDEBAR
# =========================
st.sidebar.header("⚙ Dashboard Settings")

city = st.sidebar.text_input(
    "Enter City Name",
    "Aurangabad"
)

# =========================
# BUTTON
# =========================
if st.sidebar.button("Get Weather Forecast"):

    try:

        # =========================
        # API URL
        # =========================
        url = (
            f"http://api.weatherapi.com/v1/forecast.json?"
            f"key={API_KEY}&q={city}&days=3"
        )

        # =========================
        # API REQUEST
        # =========================
        response = requests.get(url)

        data = response.json()

        # =========================
        # ERROR HANDLING
        # =========================
        if "error" in data:

            st.error(data["error"]["message"])

        else:

            # =========================
            # CURRENT WEATHER DATA
            # =========================
            temperature = data["current"]["temp_c"]

            humidity = data["current"]["humidity"]

            weather = data["current"]["condition"]["text"]

            wind_speed = data["current"]["wind_kph"]

            pressure = data["current"]["pressure_mb"]

            feels_like = data["current"]["feelslike_c"]

            # =========================
            # METRICS SECTION
            # =========================
            st.subheader("📊 Current Weather Metrics")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "🌡 Temperature",
                f"{temperature} °C"
            )

            col2.metric(
                "💧 Humidity",
                f"{humidity}%"
            )

            col3.metric(
                "🌬 Wind Speed",
                f"{wind_speed} kph"
            )

            col4, col5, col6 = st.columns(3)

            col4.metric(
                "☁ Condition",
                weather
            )

            col5.metric(
                "📌 Pressure",
                f"{pressure} mb"
            )

            col6.metric(
                "🥵 Feels Like",
                f"{feels_like} °C"
            )

            # =========================
            # ALERT SYSTEM
            # =========================
            st.subheader("🚨 Weather Alerts")

            alerts = []

            # HIGH TEMPERATURE ALERT
            if temperature > 35:

                alerts.append("🔥 High Temperature Alert!")

                send_email_alert(
                    "High Temperature Alert",
                    f"Current temperature in {city} is {temperature}°C"
                )

            # HIGH HUMIDITY ALERT
            if humidity > 80:

                alerts.append("💧 High Humidity Alert!")

            # RAIN ALERT
            if "rain" in weather.lower():

                alerts.append("🌧 Rain Alert!")

            # STORM ALERT
            if "storm" in weather.lower():

                alerts.append("⛈ Storm Alert!")

            # DISPLAY ALERTS
            if alerts:

                for alert in alerts:

                    st.warning(alert)

            else:

                st.success("✅ No severe weather alerts.")

            # =========================
            # CURRENT WEATHER CHART
            # =========================
            st.subheader("📈 Current Weather Visualization")

            labels = [
                "Temperature",
                "Humidity",
                "Wind Speed"
            ]

            values = [
                temperature,
                humidity,
                wind_speed
            ]

            fig, ax = plt.subplots(figsize=(8, 5))

            # Colorful bars
            colors = [
                "#ff4b4b",
                "#00c9a7",
                "#4d96ff"
            ]

            ax.bar(
                labels,
                values,
                color=colors
            )

            ax.set_title(
                f"Current Weather Data for {city}"
            )

            ax.set_ylabel("Values")

            st.pyplot(fig)

            # =========================
            # SAVE REPORT
            # =========================
            report = {

                "Date": [datetime.now()],

                "City": [city],

                "Temperature": [temperature],

                "Humidity": [humidity],

                "Condition": [weather],

                "Wind Speed": [wind_speed],

                "Pressure": [pressure],

                "Feels Like": [feels_like]

            }

            df = pd.DataFrame(report)

            os.makedirs("reports", exist_ok=True)

            filename = (
                f"reports/{city}_dashboard_report.csv"
            )

            df.to_csv(
                filename,
                index=False
            )

            st.success(
                f"📁 Report saved successfully: {filename}"
            )

            # =========================
            # DATA TABLE
            # =========================
            st.subheader("📋 Current Weather Data Table")

            st.dataframe(df)

            # =========================
            # 3-DAY FORECAST SECTION
            # =========================
            st.subheader("📅 3-Day Weather Forecast")

            forecast_days = data["forecast"]["forecastday"]

            forecast_dates = []

            forecast_temps = []

            cols = st.columns(3)

            for index, day in enumerate(forecast_days):

                date = day["date"]

                avg_temp = day["day"]["avgtemp_c"]

                condition = day["day"]["condition"]["text"]

                rain_chance = day["day"]["daily_chance_of_rain"]

                icon = day["day"]["condition"]["icon"]

                forecast_dates.append(date)

                forecast_temps.append(avg_temp)

                with cols[index]:

                    st.markdown(f"### 📆 {date}")

                    st.image(
                        f"https:{icon}",
                        width=80
                    )

                    st.write(
                        f"🌡 Avg Temp: {avg_temp} °C"
                    )

                    st.write(
                        f"☁ Condition: {condition}"
                    )

                    st.write(
                        f"🌧 Rain Chance: {rain_chance}%"
                    )

                    # Forecast Alerts
                    if avg_temp > 35:

                        st.error("🔥 Heat Alert")

                    elif rain_chance > 70:

                        st.warning(
                            "🌧 High Rain Probability"
                        )

                    else:

                        st.success("✅ Normal Weather")

            # =========================
            # FORECAST TREND GRAPH
            # =========================
            st.subheader("📈 Forecast Temperature Trend")

            fig2, ax2 = plt.subplots(figsize=(10, 5))

            ax2.plot(
                forecast_dates,
                forecast_temps,
                marker="o",
                linewidth=3,
                color="#00e5ff"
            )

            ax2.set_title(
                "3-Day Temperature Forecast"
            )

            ax2.set_ylabel(
                "Temperature (°C)"
            )

            ax2.grid(True)

            st.pyplot(fig2)

    except Exception as e:

        st.error(f"Error Occurred: {e}")