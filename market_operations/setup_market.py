from market import Actor, Bid, EnergyMarket
import csv
import pandas as pd

# Setup the energy market with 3 buyers
def setup_energy_market_with_buyers():

    import os
    if os.path.exists("bids.csv"):
        os.remove("bids.csv")

    df = pd.DataFrame('0', index=range(5), columns=range(5))
    df.to_csv("market_grid.csv")

    energy_market = EnergyMarket()
    # Define buyers
    buyer1 = Actor("Buyer1", "consumer", 100, 1, 1)
    buyer2 = Actor("Buyer2", "consumer", 150, 1, 2)
    buyer3 = Actor("Buyer3", "consumer", 200, 4, 3)

    # Create bids for the buyers
    bid_buyer1 = Bid(15, 50, buyer1, True)
    bid_buyer2 = Bid(20, 75, buyer2, True)
    bid_buyer3 = Bid(25, 100, buyer3, True)

    # Add bids to the market
    energy_market.add_bid(bid_buyer1)
    energy_market.add_bid(bid_buyer2)
    energy_market.add_bid(bid_buyer3)

# Call the function to setup the market
setup_energy_market_with_buyers()
