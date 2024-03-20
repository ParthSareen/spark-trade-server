from market_operations.market import Actor, Bid, EnergyMarket
import csv
import pandas as pd
import os

# Setup the energy market with 5 buyers
def setup_energy_market_with_buyers():

    # Remove existing files to start fresh
    if os.path.exists("bids.csv"):
        os.remove("bids.csv")
    if os.path.exists("matched_bids.csv"):
        os.remove("matched_bids.csv")   

    # Initialize market grid CSV
    df = pd.DataFrame('0', index=range(5), columns=range(5))
    df.to_csv("market_grid.csv")
    empty_df = pd.DataFrame(columns=["hash", "price", "quantity", "actor_name", "actor_type", "actor_capacity", "x", "y", "buying"])
    empty_df.to_csv("bids.csv")

    # Instantiate the energy market
    energy_market = EnergyMarket()
    energy_market.save_grid_to_csv()
    energy_market.save_bids_to_csv()

    # Define buyers with more spread
    buyer1 = Actor("Buyer1", "consumer", 1500, 0, 4)
    buyer2 = Actor("Buyer2", "consumer", 2000, 4, 0)
    buyer3 = Actor("Buyer3", "consumer", 2500, 4, 4)
    buyer4 = Actor("Buyer4", "consumer", 3000, 2, 2)

    # Define sellers
    seller1 = Actor("Seller1", "producer", 1000, 1, 0)
    seller2 = Actor("Seller2", "producer", 1500, 3, 4)

    # Create bids for the buyers
    bid_buyer1 = Bid(35, 750, buyer1, True)
    bid_buyer2 = Bid(20, 750, buyer2, True)
    bid_buyer3 = Bid(25, 1000, buyer3, True)
    bid_buyer4 = Bid(30, 1250, buyer4, True)

    # Add bids to the market
    energy_market.add_bid(bid_buyer1)
    energy_market.add_bid(bid_buyer2)
    energy_market.add_bid(bid_buyer3)
    energy_market.add_bid(bid_buyer4)

setup_energy_market_with_buyers()
