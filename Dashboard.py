import streamlit as st
import pandas as pd
from market_operations.market import EnergyMarket, Bid
from icecream import ic
import altair as alt
st.session_state['authenticated'] = False
st.session_state['user'] = ''

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
def generate_energy_price_forecast_chart():
    # Updated sample data to simulate energy price fluctuations similar to stock prices
    data = {
        "Time (hours)": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "Price (CAD/mAh)": [50, 55, 53, 58, 62, 58, 64, 63, 61]  # Updated simulated energy price data
    }
    threshold = 60  # Updated Buy/Sell threshold to match new data
    df = pd.DataFrame(data)
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('Time (hours)', title='Time (hours)'),
        y=alt.Y('Price (CAD/mAh)', title='Price (CAD/mAh)'),
    ).properties(
        title='Energy Price Forecast'
    )

    # Adding a horizontal line for the buy/sell threshold
    threshold_line = alt.Chart(pd.DataFrame({'y': [threshold]})).mark_rule(color='red').encode(y='y')

    # Combine the line chart with the threshold line
    final_chart = chart + threshold_line
    st.altair_chart(final_chart, use_container_width=True)

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
generate_energy_price_forecast_chart()
