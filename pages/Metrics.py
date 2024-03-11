import streamlit as st
import pandas as pd
import altair as alt
import requests


if not st.session_state.get('authenticated', False):
    st.write("You must be logged in to view this page")
    st.stop()

if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame()


st.set_page_config(page_title="Energy Metrics ⚡", page_icon="📊")
st.title('Energy Metrics ⚡')

user = st.session_state.get('user', 'jsmith')

if 'last_row_index' not in st.session_state:
    st.session_state['last_row_index'] = -1


@st.cache_data(ttl=10)
def fetch_data(user, last_row_index):
    """Fetch new data from the Flask API."""
    try:
        response = requests.get(
            f"{st.session_state['flask_url']}/get-diff-ui", 
            params={"user": user, "last_row_index": last_row_index},
            headers={'x-api-key': 'secret'}
        )
        response.raise_for_status()
        
        new_rows = response.json().get('new_rows', [])
        return new_rows
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return []

st.write("""
         Instantly view your battery's current state of charge, voltage, and amps in this interface. 
         Stay informed and in control with essential data at your fingertips.
         """)


# Fetch initial data or updated data on refresh
new_data = fetch_data(user, st.session_state['last_row_index'])


# Update the last row index if new data was fetched
if new_data:
    df_new = pd.DataFrame(new_data)
    df_new['time'] = pd.to_datetime(df_new['timestamp'])
    st.session_state['last_row_index'] += len(new_data)
    
    # Append new data to existing data frame in session state
    if 'df' in st.session_state:
        st.session_state['df'] = pd.concat([st.session_state['df'], df_new], ignore_index=True)
    else:
        st.session_state['df'] = df_new


if not st.session_state['df'].empty:
    df = st.session_state['df']
    chart = (
        alt.Chart(data=df, title="Current State of Charge")
        .mark_line()
        .encode(
            x=alt.X("time:T", title="Time", axis=alt.Axis(format="%H:%M")),
            y=alt.Y("mAh:Q", title="mAh"), 
        )
    )
    st.altair_chart(chart, use_container_width=True)

    # Uncomment below to see the raw CSV
    # st.write("Raw CSV data:")
    # st.dataframe(df)

    with st.expander("Current Voltage (V)", expanded=True):
        voltage = df["voltage"].values[-1]
        st.markdown(f"<h2>{voltage}</h2>", unsafe_allow_html=True)

    with st.expander("Current Amps (mA)", expanded=True):
        current = df["current"].values[-1]
        st.markdown(f"<h2>{current}</h2>", unsafe_allow_html=True)
        
else:
    st.write("No data available.")

# Button for manual refresh
st.info("Data is refreshed every 10 seconds. Click 'Refresh Data' to update immediately.")
if st.button('Refresh Data'):
    fetch_data(user, st.session_state['last_row_index'])

