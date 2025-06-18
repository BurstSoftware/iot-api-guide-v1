import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

# Streamlit app configuration
st.set_page_config(page_title="Simple IoT Data Viewer", page_icon="📊", layout="wide")

# Title and description
st.title("Simple IoT Data Viewer")
st.markdown("""
This app fetches sensor data (temperature and humidity) from a GitHub-hosted CSV file and displays it in a table and chart.

**Data Source**: [sensor_data.csv on GitHub](https://raw.githubusercontent.com/BurstSoftware/iot-api-guide-v1/main/sensor_data.csv)
""")

# GitHub raw URL for sensor_data.csv
SENSOR_DATA_URL = "https://raw.githubusercontent.com/BurstSoftware/iot-api-guide-v1/main/sensor_data.csv"

# Function to fetch and load sensor data from GitHub CSV
@st.cache_data(ttl=60)  # Cache for 60 seconds
def load_sensor_data():
    try:
        response = requests.get(SENSOR_DATA_URL, timeout=5)
        response.raise_for_status()  # Raise error for bad status
        csv_content = StringIO(response.text)
        df = pd.read_csv(csv_content)
        # Validate required columns
        if not all(col in df.columns for col in ["timestamp", "temperature", "humidity"]):
            raise ValueError("CSV missing required columns: timestamp, temperature, humidity")
        return df
    except (requests.RequestException, ValueError) as e:
        st.error(f"Error fetching or parsing sensor data: {e}")
        return pd.DataFrame(columns=["timestamp", "temperature", "humidity"])
    except pd.errors.ParserError:
        st.error("Invalid CSV format in sensor_data.csv")
        return pd.DataFrame(columns=["timestamp", "temperature", "humidity"])

# Fetch data
df = load_sensor_data()

# Display data
if not df.empty:
    st.subheader("Sensor Data Table")
    st.dataframe(df[["timestamp", "temperature", "humidity"]], use_container_width=True)

    st.subheader("Sensor Data Chart")
    fig = px.line(df, x="timestamp", y=["temperature", "humidity"],
                  title="Temperature and Humidity Over Time",
                  labels={"value": "Measurement", "variable": "Sensor Type"})
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available to display.")

# Footer
st.markdown("""
---
**How to Extend**:
- Replace GitHub CSV with a real IoT API (e.g., AWS IoT).
- Add real-time updates or control features.
- Deploy on Streamlit Cloud.

**Resources**:
- [Streamlit Docs](https://docs.streamlit.io/)
- [GitHub Raw Files](https://docs.github.com/en/repositories/working-with-files/using-files)
""")
