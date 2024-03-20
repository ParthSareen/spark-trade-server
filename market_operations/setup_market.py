# from market_operations.market import Actor, Bid, EnergyMarket
from market import Actor, Bid, EnergyMarket
import csv
import pandas as pd
import requests

# Setup the energy market with 3 buyers
def setup_energy_market_with_buyers():

    import os
    if os.path.exists("bids.csv"):
        os.remove("bids.csv")
    if os.path.exists("matched_bids.csv"):
        os.remove("matched_bids.csv")   

    df = pd.DataFrame('0', index=range(5), columns=range(5))
    df.to_csv("market_grid.csv")
    empty_df = pd.DataFrame(columns=["hash", "price", "quantity", "actor_name", "actor_type", "actor_capacity", "x", "y", "buying"])
    empty_df.to_csv("bids.csv")

    # requests.get('http://127.0.0.1:8001/setup')

    energy_market = EnergyMarket()
    energy_market.save_grid_to_csv()
    energy_market.save_bids_to_csv()
    # Define buyers
    buyer1 = Actor("Buyer1", "consumer", 1000, 1, 1)
    buyer2 = Actor("Buyer2", "consumer", 1500, 1, 2)
    buyer3 = Actor("Buyer3", "consumer", 2000, 4, 3)

    # Define sellers
    seller1 = Actor("Seller1", "producer", 1000, 4, 0)
    seller2 = Actor("Seller2", "producer", 1500, 2, 0)

    # Create bids for the sellers
    # bid_seller1 = Bid(10, 100, seller1, False)
    # bid_seller2 = Bid(15, 1500, seller2, False)

    # Add bids to the market
    # energy_market.add_bid(bid_seller1)
    # energy_market.add_bid(bid_seller2)

    # Create bids for the buyers
    bid_buyer1 = Bid(15, 500, buyer1, True)
    bid_buyer2 = Bid(20, 750, buyer2, True)
    bid_buyer3 = Bid(25, 1000, buyer3, True)

    # Add bids to the market
    energy_market.add_bid(bid_buyer1)
    energy_market.add_bid(bid_buyer2)
    energy_market.add_bid(bid_buyer3)

setup_energy_market_with_buyers()
