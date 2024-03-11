import streamlit as st
import pandas as pd
from market_operations.market import EnergyMarket, Bid
from icecream import ic
import altair as alt
import os
# st.session_state['authenticated'] = False
# st.session_state['user'] = ''
st.session_state['flask_url'] = 'http://127.0.0.1:8001'
# st.session_state['last_row'] = -1
# st.session_state['df'] = None

# Initialize the EnergyMarket
market = EnergyMarket()

# Function to get open calls as a DataFrame
def get_open_calls(market):
    bids = market.bids.values()
    data = {
        "Price (CAD)": [bid.price for bid in bids],
        "Quantity (mAh)": [bid.quantity for bid in bids],
        "Bidder Name": [bid.actor.name for bid in bids],
        "Buying": [bid.buying for bid in bids]
    }
    df = pd.DataFrame(data)
    return df

# Function to plot open calls
def plot_open_calls(df):
    chart = alt.Chart(df).mark_circle(size=60).encode(
        x='Bidder Name',
        y='Quantity (mAh)',
        color='Buying',
        tooltip=['Price (CAD)', 'Quantity (mAh)', 'Bidder Name', 'Buying']
    ).properties(
        title='Open Calls Overview'
    )
    st.altair_chart(chart, use_container_width=True)

# Function to generate a line chart for mAh vs. Time
def generate_energy_price_forecast_chart():
    data = {
        "Time (hours)": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "Price (CAD/mAh)": [50, 55, 53, 58, 62, 58, 64, 63, 61]
    }
    threshold = 60
    df = pd.DataFrame(data)
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('Time (hours)', title='Time (hours)'),
        y=alt.Y('Price (CAD/mAh)', title='Price (CAD/mAh)'),
    ).properties(
        title='Energy Price Forecast'
    )
    threshold_line = alt.Chart(pd.DataFrame({'y': [threshold]})).mark_rule(color='red').encode(y='y')

    final_chart = chart + threshold_line
    st.altair_chart(final_chart, use_container_width=True)

# Streamlit Dashboard
st.title("Energy Market Dashboard")

# Check if matched_bids.csv exists
if os.path.exists("matched_bids.csv"):
    # Load the matched bids data
    matched_bids_df = pd.read_csv("matched_bids.csv")
    # Calculate the YTD profit
    profit = (matched_bids_df['Sell Price'] * matched_bids_df['Sell Amount']).sum()
    # Display the updated YTD profit
    with st.expander("YTD Profit", expanded=True):
        if profit > 0:
            st.markdown(f"<h2 style='color:green;'>${profit}</h2>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h2>${profit}</h2>", unsafe_allow_html=False)

    # Display Matched Bids Data
    with st.expander("Matched Bids Data", expanded=True):
        st.write("Matched Bids Overview:")
        st.dataframe(matched_bids_df)
        
        # Scatter Plot for Matched Bids
        scatter_chart = alt.Chart(matched_bids_df).mark_circle(size=60).encode(
            x='Sell Price',
            y='Sell Amount',
            color='Buyer Name',
            tooltip=['Buyer Name', 'Sell Price', 'Sell Amount', 'Seller Name']
        ).properties(
            title='Matched Bids Scatter Plot'
        )
        st.altair_chart(scatter_chart, use_container_width=True)

# Display Open Calls
open_calls = get_open_calls(market)
st.write("Open Calls:")
st.dataframe(open_calls[['Price (CAD)', 'Quantity (mAh)', 'Bidder Name', 'Buying']])
plot_open_calls(open_calls)
# Display Line Chart
st.write("mAh vs. Time Chart")
generate_energy_price_forecast_chart()
