from __future__ import annotations
from dataclasses import dataclass
from collections import deque
import datetime
import os
import pandas as pd
from typing import List
import math
import csv
from icecream import ic


@dataclass
class Actor:
    name: str
    actor_type: str
    capcity: float
    x: int 
    y: int 


@dataclass
class Bid:
    price: float
    quantity: int
    actor: Actor 
    buying: bool


class EnergyMarket:
    def __init__(self) -> None:
        self.sellers = {} 
        self.buyers = {} 
        self.bids = {}
        self.grid = [[]]
        self.grid_df = None
        self.load_grid_from_csv()
        self.load_bids_from_csv()
    
    # def __del__(self):
    #     # Save the grid to a CSV file
    #     self.save_grid_to_csv()
    #     # Save the bids to a CSV file
    #     self.save_bids_to_csv()
    #     print("EnergyMarket object is being destroyed, saving grid and bids to CSV.")

    def save_bids_to_csv(self, filename: str = "bids.csv") -> None:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['hash', 'price', 'quantity', 'actor_name', 'actor_type', 'actor_capacity', 'x', 'y', 'buying'])
            for hash, bid in self.bids.items():
                writer.writerow([hash, bid.price, bid.quantity, bid.actor.name, bid.actor.actor_type, bid.actor.capcity, bid.actor.x, bid.actor.y, bid.buying])
    
    def load_bids_from_csv(self, filename: str = "bids.csv") -> None:
        try:
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                self.bids = {}
                for row in reader:
                    actor = Actor(name=row['actor_name'], actor_type=row['actor_type'], capcity=float(row['actor_capacity']), x=int(row['x']), y=int(row['y']))
                    bid = Bid(price=float(row['price']), quantity=int(row['quantity']), actor=actor, buying=row['buying'] == 'True')
                    self.bids[row['hash']] = bid
        except FileNotFoundError:
            print(f"File {filename} not found. Initializing an empty bids dictionary.")

    def load_grid_from_csv(self, filename: str = "market_grid.csv") -> None:
        try:
            df = pd.read_csv(filename, index_col=0, dtype=str)
            self.grid = df.values.tolist()
            self.grid_df = df
            # ic(self.grid)
            # ic(self.grid_df)
        except FileNotFoundError:
            print(f"File {filename} not found. Initializing an empty grid.")
            self.grid = [[0 for _ in range(5)] for _ in range(5)]
       
        
    def save_grid_to_csv(self, filename: str = "market_grid.csv") -> None:
        self.grid_df = pd.DataFrame(self.grid)
        self.grid_df.to_csv(filename)
        


    def add_bid(self, bid: Bid) -> None:
        self.load_grid_from_csv()
        ic('add bid', bid, self.grid)
        self.remove_old_calls(seller_name=bid.actor.name)
        hash = bid.actor.name + "_" + str(int(bid.price)) + "_" + str(bid.buying)
        if hash not in self.bids:
            self.bids[hash] = bid
            ic(bid.actor.x, bid.actor.y, hash)
            self.grid[bid.actor.x][bid.actor.y] = hash
            self.save_grid_to_csv()
            self.save_bids_to_csv()
            ic('added', self.grid)

        else:
            raise ValueError("Bid already exists")

        
    def remove_bid(self, bid: Bid) -> None:
        self.load_grid_from_csv()
        hash = bid.actor.name + "_" + str(int(bid.price)) + "_" + str(bid.buying)
        ic('removing', bid)
        if hash in self.bids:
            del self.bids[hash]
            self.grid[bid.actor.x][bid.actor.y] = '0' 
            self.save_grid_to_csv()
        else:
            raise ValueError("Bid does not exist")

    def print_grid(self) -> None:
        for row in self.grid:
            print(" ".join(str(cell) for cell in row)) 
        print('\n')
    
    

    def find_all_bids(self, input_bid: Bid) -> List[str]:
        self.load_grid_from_csv()
        def euclidean_distance(x1, y1, x2, y2):
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        bids_ending_with_true = []
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                if isinstance(cell, str) and cell.endswith('True'):
                    distance = euclidean_distance(input_bid.actor.x, input_bid.actor.y, x, y)
                    bids_ending_with_true.append((cell, distance))
        ic(bids_ending_with_true)
        return bids_ending_with_true


    def remove_old_calls(self, bid:Bid|None=None, seller_name=None) -> None:
        if not seller_name:
            seller_name = bid.actor.name
        bids_to_remove = [(bid_hash, bid_obj) for bid_hash, bid_obj in self.bids.items() if bid_obj.actor.name == seller_name]
        for bid_hash, bid_obj in bids_to_remove:
            del self.bids[bid_hash]
            self.grid[bid_obj.actor.x][bid_obj.actor.y] = '0'
        self.save_grid_to_csv()
        self.save_bids_to_csv()


    def update_bid_in_grid_and_bids(self, bid: Bid, old_hash) -> None:
        """
        Updates the bid information in both the grid and the bids dictionary.
        """
        # Generate the hash for the bid
        bid_hash = f"{bid.actor.name}_{int(bid.price)}_{bid.buying}"
        # Update the bid in the bids dictionary
        if old_hash in self.bids:
            del self.bids[old_hash]

        self.bids[bid_hash] = bid
        # Update the bid in the grid
        self.grid[bid.actor.x][bid.actor.y] = bid_hash
        ic(self.grid[bid.actor.x][bid.actor.y])
        # Save the updated grid and bids to their respective CSV files
        self.save_grid_to_csv()
        self.save_bids_to_csv()

    def match_bid(self, input_bid: Bid, buying_bids_hash_and_dist: List) -> (float, float, Bid) | None:
        highest_bid_score = 0
        highest_bid: Bid = None
        highest_bid_hash = None
        original_input_bid_hash = input_bid.actor.name + "_" + str(int(input_bid.price)) + "_" + str(input_bid.buying)

        for bid_hash in buying_bids_hash_and_dist:
            distance = bid_hash[1]
            bid = self.bids[bid_hash[0]]
            bid_score = bid.price * bid.quantity * (1 / distance)
            if bid_score > highest_bid_score and bid.price >= input_bid.price:
                highest_bid_score = bid_score 
                highest_bid = bid 

        if highest_bid:
            sell_price = highest_bid.price if highest_bid.price > input_bid.price else input_bid.price
            # sell_price = min(highest_bid.price, input_bid.price)
            sell_amt = min(highest_bid.quantity, input_bid.quantity)
            matched_bid = highest_bid
            # ic(highest_bid)
            # ic(self.bids)

            if sell_amt < highest_bid.quantity:
                highest_bid.quantity -= sell_amt
                self.update_bid_in_grid_and_bids(highest_bid, highest_bid_hash)
                self.remove_bid(input_bid)
                
            elif sell_amt < input_bid.quantity:
                input_bid.quantity -= sell_amt
                self.update_bid_in_grid_and_bids(input_bid, original_input_bid_hash)
                self.remove_bid(highest_bid)
            else:
                self.remove_bid(highest_bid)
                self.remove_bid(input_bid)
            self.save_bids_to_csv()
            # Save matched bid data to CSV
            file_path = 'matched_bids.csv'
            # Check if file exists, if not, create it and write headers
            if not os.path.exists(file_path):
                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Buyer Name', 'Sell Price', 'Sell Amount', 'Seller Name', 'Datetime'])
            # Append the new row to the file, including the current datetime
            with open(file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([input_bid.actor.name, sell_price, sell_amt, matched_bid.actor.name, current_datetime])

        else:
            return None
        return sell_price, sell_amt, matched_bid

        # matched_bids = set()
        # for bid in buying_bids:
        #     if input_bid.quantity > 0:
        #         if input_bid.quantity >= bid.quantity:
        #             input_bid.quantity -= self.bids[bid[0]].quantity
        #             matched_bids.add(bid[0])
        #         else:
        #             self.bids[bid[0]].quantity -= input_bid.quantity
        #             input_bid.quantity = 0

            


def main():
    import setup_market
    setup_market.setup_energy_market_with_buyers()
    actor2 = Actor("actor2", "consumer", 100, 4, 4)
    bid2 = Bid(20, 10, actor2, False)
    market = EnergyMarket()
    market.add_bid(bid2)
    # market.match_single_bid(bid1)
    buying_bids = market.find_all_bids(bid2)
    sell_price, sell_amt, matched_bid = market.match_bid(bid2, buying_bids)
    ic(bid2)
    ic(sell_price, sell_amt, matched_bid)


if __name__ == "__main__":
    main()