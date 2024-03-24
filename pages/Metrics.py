import streamlit as st
import pandas as pd
import altair as alt
import requests


import time

LOCAL_SERVER_URL = 'http://127.0.0.1:8001'
ONLINE_SERVER_URL = 'http://54.202.120.41:8001'

CURRENT_URL = LOCAL_SERVER_URL

def fetch_soc_data(username):
    api_url = f"http://127.0.0.1:8001/get-soc-data/{username}"
    headers = {"x-api-key": "secret"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data, columns=["current", "mAh", "voltage", "timestamp"])
    else:
        print(f"Failed to fetch SOC data: {response.text}")
        return pd.DataFrame()

def display_soc_data(username):
    df_soc = fetch_soc_data(username)

    if not df_soc.empty:
        df_soc['timestamp'] = pd.to_datetime(df_soc['timestamp'])
        df_soc['mAh'] = pd.to_numeric(df_soc['mAh'])
        df_soc['voltage'] = pd.to_numeric(df_soc['voltage'])

        df_soc['mAh'] = 1000 - df_soc.index
        print(df_soc.head())

        # Generate and display the SOC graph
        soc_chart = (
            alt.Chart(df_soc)
            .mark_line()
            .encode(
                x=alt.X('timestamp:T', title='Time'),
                y=alt.Y('mAh:Q', title='mAh'),
                color='voltage:Q'
            )
            .properties(title="SOC Data Over Time for {}".format(username))
        )
        st.altair_chart(soc_chart, use_container_width=True)

    # Display modals for the last entry of voltage and current
    if not df_soc.empty:
        last_entry = df_soc.iloc[-1]
        st.info(f"Last Voltage: {last_entry['voltage']}V")
        st.info(f"Last Current: {last_entry['current']}A")
    else:
        st.write("No SOC data available for the user.")

# Main loop to refresh data every 10 seconds
username = "jsmith"  # Example username
while True:
    display_soc_data(username)
    time.sleep(10)
    st.rerun()
    
