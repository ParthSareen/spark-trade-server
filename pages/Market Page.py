import streamlit as st
import altair as alt
from market_operations import *
import pandas as pd

st.set_page_config(page_title="Energy Market", page_icon="📊")
st.title('Energy Market')

from market_operations.market import Actor, Bid, EnergyMarket

energy_market = EnergyMarket()

def toggle_grid_view():
    st.write("Initial grid with buyers:")
    grid_df = pd.DataFrame(energy_market.grid)
    print(grid_df)
    st.dataframe(grid_df.style.applymap(lambda x: 'background-color: green' if x.endswith('_True') else ('background-color: orange' if x.endswith('_False') else ''), subset=grid_df.columns))

option = st.selectbox("Choose an action:", ["", "Grid View", "Create Sell Bid"])

if option == "Grid View":
    toggle_grid_view()
elif option == "Create Sell Bid":
    with st.form("sell_bid_form"):
        st.write("Enter your sell bid details:")
        seller_name = "Seller1"
        seller_capacity = st.number_input("Capacity", min_value=0.0, format="%.2f", key="seller_capacity_form")
        seller_x, seller_y = 0, 0
        sell_price = st.number_input("Price", min_value=0.0, format="%.2f", key="sell_price_form")
        sell_quantity = st.number_input("Quantity", min_value=0, key="sell_quantity_form")
        submit_button = st.form_submit_button("Submit Sell Bid")

    if submit_button:
        seller = Actor(seller_name, "producer", seller_capacity, seller_x, seller_y)
        sell_bid = Bid(sell_price, sell_quantity, seller, False)
        try:
            energy_market.add_bid(sell_bid)
            st.success("Sell bid added successfully!")
            import time
            st.progress(100)
            time.sleep(1.515)  # Adjusted total sleep time for better user experience
        except ValueError as e:
            st.error(f"Failed to add sell bid: {e}")
