import streamlit as st
from market_operations import *

st.set_page_config(page_title="Energy Market", page_icon="📊")
st.title('Energy Market')

from market_operations.market import Actor, Bid, EnergyMarket


if not st.session_state.get('authenticated', False):
    st.write("You must be logged in to view this page")
    st.stop()

if 'refresh_grid' not in st.session_state:
    st.session_state.refresh_grid = True


def remove_bid(bid: Bid):
    energy_market = EnergyMarket()
    energy_market.remove_bid(bid)


def toggle_grid_view():
    energy_market = EnergyMarket()

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
    
    with st.container():
        styled_df = grid_df.style.applymap(lambda x: 'background-color: green' if 'sells' in x else ('background-color: orange' if 'buys' in x else ''), subset=grid_df.columns)
        st.dataframe(styled_df, use_container_width=True)


grid_view_expander = st.expander("Grid View", expanded=True)
with grid_view_expander:
    toggle_grid_view()
    if st.button("Refresh Grid View"):
        pass

buyer_name = st.session_state['user']

create_buy_bid_expander = st.expander("Create Buy Bid")
with create_buy_bid_expander:
    buy_bid = None
    energy_market: EnergyMarket = EnergyMarket()
    with st.form("buy_bid_form"):
        st.write("Enter your buy bid details:")

        # TODO: pull this data from arduino
        buyer_capacity, buyer_x, buyer_y = 1000, st.session_state['x'], st.session_state['y']

        buy_price = st.number_input("Price (CAD)", min_value=5.0, format="%.2f", key="buy_price_form")
        buy_quantity = st.number_input("Quantity (mAh)", min_value=200, key="buy_quantity_form")
        submit_button = st.form_submit_button("Submit Buy Bid")

    if submit_button:
        if buyer_name == "rbriggs":
            buyer_name = "Buyer1"
        else:
            buyer_name = "Buyer2"
        buyer = Actor(buyer_name, "producer", buyer_capacity, buyer_x, buyer_y)
        buy_bid = Bid(buy_price, buy_quantity, buyer, True)
        try:
            energy_market.add_bid(buy_bid)
            import time
            my_bar = st.progress(0, text='Submitting Bid')

            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text='Submitting Bid')
            st.success("Buy bid added successfully!")
        except ValueError as e:
            st.error(f"Failed to add buy bid: {e}")

if st.button('Remove Old Bids'):
    energy_market.remove_old_calls(name=buyer_name)
