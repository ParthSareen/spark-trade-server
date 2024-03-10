from dataclasses import dataclass
from collections import deque
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
        # self.grid = [[0 for _ in range(5)] for _ in range(5)]
        # self.save_grid_to_csv()
        self.grid = [[]]
        self.grid_df = None
        self.load_grid_from_csv()
        self.load_bids_from_csv()
    
    def __del__(self):
        # Save the grid to a CSV file
        self.save_grid_to_csv()
        # Save the bids to a CSV file
        self.save_bids_to_csv()
        print("EnergyMarket object is being destroyed, saving grid and bids to CSV.")

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
            ic(self.grid)
            ic(self.grid_df)
        except FileNotFoundError:
            print(f"File {filename} not found. Initializing an empty grid.")
            self.grid = [[0 for _ in range(5)] for _ in range(5)]
       
        
    def save_grid_to_csv(self, filename: str = "market_grid.csv") -> None:
        self.grid_df = pd.DataFrame(self.grid)
        self.grid_df.to_csv(filename)
        


    def add_bid(self, bid: Bid) -> None:
        self.load_grid_from_csv()
        ic(self.grid)
        hash = bid.actor.name + "_" + str(bid.price) + "_" + str(bid.buying)
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
        hash = bid.actor.name + "_" + str(bid.price) + "_" + str(bid.buying)
        if hash in self.bids:
            del self.bids[hash]
            self.grid[bid.actor.x][bid.actor.y] = hash
            self.save_grid_to_csv()
        else:
            raise ValueError("Bid does not exist")

    def print_grid(self) -> None:
        for row in self.grid:
            print(" ".join(str(cell) for cell in row)) 
        print('\n')
    
    
    def match_single_bid(self, bid: Bid) -> None:
        self.load_grid_from_csv()

        def is_valid(x, y):
            return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]) 

        def euclidean_distance(x1, y1, x2, y2):
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        def ends_with_true(node_value):
            return node_value.endswith('False')

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        queue = deque([(bid.actor.x, bid.actor.y)])  # Store current position and initial distance as 0
        visited = set((bid.actor.x, bid.actor.y))
        closest_nodes = []
        while queue:
            x, y = queue.popleft()
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if is_valid(new_x, new_y) and (new_x, new_y) not in visited:
                    if ends_with_true(self.grid[new_x][new_y]):
                        closest_nodes.append((new_x, new_y))

                visited.add((new_x, new_y))
                queue.append((new_x, new_y))

    def find_all_bids(self, input_bid: Bid) -> List[str]:
        self.load_grid_from_csv()
        def euclidean_distance(x1, y1, x2, y2):
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        bids_ending_with_false = []
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                if isinstance(cell, str) and cell.endswith('False'):
                    distance = euclidean_distance(input_bid.actor.x, input_bid.actor.y, x, y)
                    bids_ending_with_false.append((cell, distance))
        return bids_ending_with_false


def main():
    actor1 = Actor("actor1", "producer", 100, 0, 0)
    actor2 = Actor("actor2", "consumer", 100, 4, 4)
    bid1 = Bid(10, 10, actor1, True)
    bid2 = Bid(10, 10, actor2, False)
    market = EnergyMarket()
    market.add_bid(bid1)
    market.add_bid(bid2)
    # market.match_single_bid(bid1)
    market.find_all_bids(bid1)
    print("Initial grid:")
    market.print_grid()
    market.remove_bid(bid1)
    market.print_grid()

if __name__ == "__main__":
    main()