import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

# Streamlit app configuration
st.set_page_config(page_title="IoT Data Viewer", page_icon="📊")

# Title
st.title("IoT Data Viewer")

# GitHub raw URL for sensor_data.csv
SENSOR_DATA_URL = "https://raw.githubusercontent.com/BurstSoftware/iot-api-guide-v1/main/sensor_data.csv"

# Function to fetch and load sensor data from GitHub CSV
@st.cache_data(ttl=300)  # Cache for 5 minutes to reduce GitHub requests
def load_sensor_data():
    try:
        response = requests.get(SENSOR_DATA_URL, timeout=5)
        response.raise_for_status()
        csv_content = StringIO(response.text)
        df = pd.read_csv(csv_content)
        if not all(col in df.columns for col in ["timestamp", "temperature", "humidity"]):
            raise ValueError("CSV must have columns: timestamp, temperature, humidity")
        return df
    except requests.RequestException as e:
        st.error(f"Failed to fetch data from GitHub: {e}")
        return pd.DataFrame(columns=["timestamp", "temperature", "humidity"])
    except (ValueError, pd.errors.ParserError) as e:
        st.error(f"Data error: {e}")
        return pd.DataFrame(columns=["timestamp", "temperature", "humidity"])

# Load and display data
df = load_sensor_data()

if not df.empty:
    st.subheader("Sensor Data")
    st.dataframe(df)
    st.subheader("Temperature and Humidity Chart")
    fig = px.line(df, x="timestamp", y=["temperature", "humidity"],
                  title="Sensor Data Over Time",
                  labels={"value": "Measurement", "variable": "Sensor Type"})
    st.plotly_chart(fig)
else:
    st.warning("No data available. Check the CSV file on GitHub.")
