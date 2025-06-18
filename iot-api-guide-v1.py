import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time
from datetime import datetime

# Streamlit app configuration
st.set_page_config(page_title="IoT API Guide", page_icon="🌐", layout="wide")

# Title and description
st.title("IoT API Guide: Simulate IoT Device Interaction")
st.markdown("""
This app demonstrates how to interact with an IoT API to:
- Fetch sensor data (e.g., temperature, humidity).
- Send control commands (e.g., turn a device on/off).
- Visualize real-time data.

**Note**: This uses a mock API for demonstration. Replace with a real IoT API for production.
""")

# Mock API endpoints (replace with real IoT API endpoints)
MOCK_SENSOR_API = "https://api.mocki.co/2/123456/sensors"  # Simulated sensor data
MOCK_CONTROL_API = "https://api.mocki.co/2/123456/control"  # Simulated control endpoint

# Function to fetch sensor data from IoT API
@st.cache_data(ttl=60)  # Cache data for 60 seconds
def fetch_sensor_data():
    try:
        response = requests.get(MOCK_SENSOR_API, timeout=5)
        response.raise_for_status()  # Raise error for bad status
        data = response.json()
        return data.get("sensors", {})
    except requests.RequestException as e:
        st.error(f"Error fetching sensor data: {e}")
        return {"temperature": 0, "humidity": 0}

# Function to send control command to IoT device
def send_control_command(device_id, state):
    try:
        payload = {"device_id": device_id, "state": state}
        response = requests.post(MOCK_CONTROL_API, json=payload, timeout=5)
        response.raise_for_status()
        return response.json().get("message", "Command sent successfully!")
    except requests.RequestException as e:
        st.error(f"Error sending command: {e}")
        return "Failed to send command."

# Sidebar for configuration
st.sidebar.header("IoT Device Configuration")
device_id = st.sidebar.text_input("Device ID", value="device_001")
refresh_rate = st.sidebar.slider("Data Refresh Rate (seconds)", 5, 60, 10)
api_key = st.sidebar.text_input("API Key (for real APIs)", type="password", value="mock_key")

# Main content layout
col1, col2 = st.columns([2, 1])

# Column 1: Data visualization
with col1:
    st.subheader("Real-Time Sensor Data")
    chart_placeholder = st.empty()  # Placeholder for updating chart
    data_placeholder = st.empty()  # Placeholder for raw data

    # Initialize data storage
    if "sensor_history" not in st.session_state:
        st.session_state["sensor_history"] = []

    # Column 2: Device control
    with col2:
        st.subheader("Device Control")
        st.markdown("**Control IoT Device** (e.g., Light)")
        if st.button("Turn ON"):
            result = send_control_command(device_id, "ON")
            st.success(result)
        if st.button("Turn OFF"):
            result = send_control_command(device_id, "OFF")
            st.warning(result)

    # Simulate real-time data updates
    st.subheader("Monitoring...")
    while True:
        # Fetch sensor data
        sensor_data = fetch_sensor_data()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update session state with new data
        st.session_state["sensor_history"].append({
            "timestamp": timestamp,  # Fixed: Corrected key order
            "temperature": sensor_data.get("temperature", 0),
            "humidity": sensor_data.get("humidity", 0)
        })
        
        # Keep only last 50 data points to prevent memory issues
        st.session_state["sensor_history"] = st.session_state["sensor_history"][-50:]
        
        # Create a DataFrame for visualization
        df = pd.DataFrame(st.session_state["sensor_history"])
        
        # Display raw data
        data_placeholder.write(f"""
        **Latest Data** (at {timestamp}):
        - Temperature: {sensor_data.get('temperature', 'N/A')} °C
        - Humidity: {sensor_data.get('humidity', 'N/A')}%
        """)
        
        # Plot data using Plotly
        if not df.empty:
            fig = px.line(df, x="timestamp", y=["temperature", "humidity"], 
                         title="Sensor Data Over Time",
                         labels={"value": "Measurement", "variable": "Sensor Type"})
            fig.update_layout(showlegend=True)
            chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        # Refresh based on user-selected rate
        time.sleep(refresh_rate)

# Footer
st.markdown("""
---
**How to Extend**:
1. Replace mock APIs with real IoT platform APIs (e.g., AWS IoT, Tuya, Blynk).
2. Add authentication headers (e.g., Bearer {api_key}).
3. Implement error handling for production use.
4. Add more control options (e.g., sliders for brightness, color pickers).
5. Deploy on Streamlit Cloud for remote access.

**Resources**:
- [AWS IoT API Docs](https://docs.aws.amazon.com/iot/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Mock API Service](https://mocki.io/)
""")
