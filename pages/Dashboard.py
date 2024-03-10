import streamlit as st
import pandas as pd
from market_operations.market import EnergyMarket, Bid
from icecream import ic

# Initialize the EnergyMarket
market = EnergyMarket()

# Function to get open calls as a DataFrame
def get_open_calls(market):
    # bids = list(market.bids.values())
    bids = market.bids.values()
    ic(bids)
    data = {
        "Price": [bid.price for bid in bids],
        "Quantity": [bid.quantity for bid in bids],
        "Actor": [bid.actor.name for bid in bids],
        "Buying": [bid.buying for bid in bids]
    }
    df = pd.DataFrame(data)
    return df
# Function to generate a line chart for mAh vs. Time
def generate_line_chart():
    # Sample data for a chart with decreasing, flat, and again decreasing patterns
    data = {
        "Time (minutes)": [10, 20, 30, 40, 50, 60, 70, 80, 90],
        "mAh": [10000, 9000, 8000, 8000, 7000, 7000, 6000, 4000, 2000]  # Adjusted values to include flat portions
    }
    df = pd.DataFrame(data)
    st.line_chart(df.set_index("Time (minutes)"))

# Streamlit Dashboard
st.title("Energy Market Dashboard")

# Display Profit
# profit = calculate_profit(market.bids)
with st.expander("YTD Profit", expanded=True):
    profit = 1241
    if profit > 0:
        st.markdown(f"<h2 style='color:green;'>${profit}</h2>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2>${profit}</h2>", unsafe_allow_html=False)


# Display Open Calls
open_calls = get_open_calls(market)
st.write("Open Calls:")
st.dataframe(open_calls[['Price', 'Quantity', 'Actor', 'Buying']])

# Display Line Chart
st.write("mAh vs. Time Chart")
generate_line_chart()
