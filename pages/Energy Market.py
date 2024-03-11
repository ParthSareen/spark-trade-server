import streamlit as st
import altair as alt
from market_operations import *
import pandas as pd
from icecream import ic
from market_operations.setup_market import setup_energy_market_with_buyers

st.set_page_config(page_title="Energy Market", page_icon="📊")
st.title('Energy Market')

from market_operations.market import Actor, Bid, EnergyMarket


def toggle_grid_view():
    energy_market = EnergyMarket()

    # grid_df = pd.DataFrame(energy_market.grid)
    def prettify_grid_value(value):
        if isinstance(value, str) and "_" in value:
            quantity = energy_market.bids[value].quantity
            parts = value.split("_")
            name = parts[0]
            price = parts[1]
            action = "sells" if parts[2] == "False" else "buys"
            return f"{name} {action} {quantity} mAh at price: {price}"
        return value

    grid_df = energy_market.grid_df.applymap(prettify_grid_value)
    print(grid_df)
    st.dataframe(grid_df.style.applymap(lambda x: 'background-color: green' if 'sells' in x else ('background-color: orange' if 'buys' in x else ''), subset=grid_df.columns))

grid_view_expander = st.expander("Grid View", expanded=True)
with grid_view_expander:
    if st.button("Refresh Grid View"):
        toggle_grid_view()

def remove_bid(bid: Bid):
    energy_market = EnergyMarket()
    energy_market.remove_bid(bid)


create_sell_bid_expander = st.expander("Create Sell Bid")
with create_sell_bid_expander:
    sell_bid = None
    energy_market: EnergyMarket = EnergyMarket()
    with st.form("sell_bid_form"):
        st.write("Enter your sell bid details:")
        # TODO: replace with user name @Fares
        seller_name = "jsmith"
        # seller_capacity = st.number_input("Capacity", min_value=0.0, format="%.2f", key="seller_capacity_form")
        seller_capacity = 10000
        seller_x, seller_y = 0, 0
        sell_price = st.number_input("Price (CAD)", min_value=5.0, format="%.2f", key="sell_price_form")
        sell_quantity = st.number_input("Quantity (mAh)", min_value=200, key="sell_quantity_form")
        submit_button = st.form_submit_button("Submit Sell Bid")

    if submit_button:
        seller = Actor(seller_name, "producer", seller_capacity, seller_x, seller_y)
        sell_bid = Bid(sell_price, sell_quantity, seller, False)
        try:
            energy_market.add_bid(sell_bid)
            import time
            my_bar = st.progress(0, text='Submitting Bid')

            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text='Submitting Bid')
            st.success("Sell bid added successfully!")
        except ValueError as e:
            st.error(f"Failed to add sell bid: {e}")


if st.button('Remove Old Bids'):
    energy_market.remove_old_calls(seller_name='jsmith')

if st.button('Submit for Matching'):
    sell_bid = energy_market.bids[energy_market.grid[0][0]]
    if sell_bid is None:
        st.error("Please submit a sell bid first")
        st.stop()
    buying_bids = energy_market.find_all_bids(sell_bid)
    ic(buying_bids)
    matched = energy_market.match_bid(sell_bid, buying_bids)
    if matched:
        st.success("Matching completed successfully!")
        st.write(matched)
    else:
        st.write("No matching bids found")

if st.button('Reset Market Ops'):
    setup_energy_market_with_buyers()