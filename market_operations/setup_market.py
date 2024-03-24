from market_operations.market import Actor, Bid, EnergyMarket
# from market import Actor, Bid, EnergyMarket
import pandas as pd
import os
import requests

LOCAL_SERVER_URL = 'http://127.0.0.1:8001'
ONLINE_SERVER_URL = 'http://54.202.120.41:8001'

CURRENT_URL = LOCAL_SERVER_URL
# Setup the energy market with 5 buyers
def setup_energy_market_with_buyers():

    # Remove existing files to start fresh
    if os.path.exists("bids.csv"):
        os.remove("bids.csv")
    if os.path.exists("matched_bids.csv"):
        os.remove("matched_bids.csv") 
    

    # Define the API endpoint for deleting test data
    api_endpoint = CURRENT_URL + "/delete-test-data"
    headers = {"x-api-key": "secret"}

    # Make the DELETE request to the API
    response = requests.delete(api_endpoint, headers=headers)

    # Check the response status
    if response.status_code == 200:
        print("Test data deleted successfully.")
    elif response.status_code == 404:
        print("Test data does not exist.")
    else:
        print(f"Failed to delete test data: {response.text}")

    # Initialize market grid CSV
    df = pd.DataFrame('0', index=range(5), columns=range(5))
    df.to_csv("market_grid.csv")
    empty_df = pd.DataFrame(columns=["hash", "price", "quantity", "actor_name", "actor_type", "actor_capacity", "x", "y", "buying"])
    empty_df.to_csv("bids.csv")
    empty_df = pd.DataFrame(columns=["hash", "price", "quantity", "actor_name", "actor_type", "actor_capacity", "x", "y", "buying"])
    empty_df.to_csv("bids.csv")

    # requests.get('http://127.0.0.1:8001/setup')

    # Instantiate the energy market
    energy_market = EnergyMarket()
    # Define buyers
    buyer1 = Actor("Buyer1", "consumer", 1000, 4, 0)
    buyer2 = Actor("Buyer2", "consumer", 1500, 0, 3)
    buyer3 = Actor("Buyer3", "consumer", 2000, 4, 3)
    buyer4 = Actor("Buyer3", "consumer", 2500, 4, 4)

    # Define sellers
    seller1 = Actor("Seller1", "producer", 1000, 1, 0)
    seller2 = Actor("Seller2", "producer", 1500, 3, 4)

    # Create bids
    bid_buyer1 = Bid(5, 30, buyer1, True)
    bid_buyer2 = Bid(20, 25, buyer2, True)
    # bid_buyer3 = Bid(25, 1000, buyer3, True)
    # bid_buyer4 = Bid(30, 1250, buyer4, True)
    bid_seller1 = Bid(50, 2000, seller1, False)
    bid_seller2 = Bid(45, 1500, seller2, False)

    # Add bids to the market
    energy_market.add_bid(bid_buyer1)
    energy_market.add_bid(bid_buyer2)
    # energy_market.add_bid(bid_buyer3)
    # energy_market.add_bid(bid_buyer4)
    # energy_market.add_bid(bid_seller1)
    # energy_market.add_bid(bid_seller2)

setup_energy_market_with_buyers()
