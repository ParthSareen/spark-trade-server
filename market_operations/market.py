from dataclasses import dataclass
from collections import deque
from typing import List


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


class Market:
    def __init__(self) -> None:
        self.sellers = {} 
        self.buyers = {} 
        self.bids = {}
        self.grid = [[0 for _ in range(5)] for _ in range(5)]


    def add_bid(self, bid: Bid) -> None:
        hash = bid.actor.name + str(bid.price)+ str(bid.buying)
        if hash not in self.bids:
            self.bids[hash] = bid
            self.grid[bid.actor.x][bid.actor.y] = hash
        else:
            raise ValueError("Bid already exists")
        
    def remove_bid(self, bid: Bid) -> None:
        hash = bid.actor.name + str(bid.price) + str(bid.buying)
        if hash in self.bids:
            del self.bids[hash]
            self.grid[bid.actor.x][bid.actor.y] = hash
        else:
            raise ValueError("Bid does not exist")

    def print_grid(self) -> None:
        for row in self.grid:
            print(" ".join(str(cell) for cell in row)) 
        print('\n')
    
    def match_single_bid(self, bid: Bid) -> None:

        def is_valid(x, y):
            return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]) and self.grid[x][y] != 0
        from collections import deque

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        queue = deque([((bid.actor.x, bid.actor.y), 0)])  # Store current position and distance
        visited = set((bid.actor.x, bid.actor.y))
        closest_nodes = []

        while queue and len(closest_nodes) < 2:
            (x, y), dist = queue.popleft()
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited:
                    if is_valid(nx, ny):
                        closest_nodes.append((self.grid[nx][ny], dist + 1))  # Add node value and distance
                        if len(closest_nodes) == 2:
                            break
                    visited.add((nx, ny))
                    queue.append(((nx, ny), dist + 1))
        print(closest_nodes)
        return closest_nodes
        

def main():
    actor1 = Actor("actor1", "producer", 100, 0, 0)
    actor2 = Actor("actor2", "consumer", 100, 4, 4)
    bid1 = Bid(10, 10, actor1, True)
    bid2 = Bid(10, 10, actor2, False)
    market = Market()
    market.add_bid(bid1)
    market.add_bid(bid2)
    market.match_single_bid(bid1)
    print("Initial grid:")
    market.print_grid()
    market.remove_bid(bid1)
    market.print_grid()

if __name__ == "__main__":
    main()