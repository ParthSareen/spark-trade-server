import pandas as pd
import numpy as np
from icecream import ic
from streamlit_d3graph import d3graph
from market_operations.market import *

em = EnergyMarket()


d3 = d3graph()
d3.config['staticGraph'] = True
d3.config['directed'] = False  # Ensure the graph is undirected
d3.config['charge'] = -800  # Adjust the charge to control the spacing between nodes
d3.config['gravity'] = 0.05  # Adjust gravity to control how tight the graph is
d3.config['origin'] = {'x': 0, 'y': 0}  # Set the origin to the top left

def create_adjacency_matrix(size):
    matrix = np.zeros((size*size, size*size))
    for row in range(size):
        for col in range(size):
            index = row * size + col
            # Horizontal and vertical neighbors
            if col > 0: # Left
                matrix[index, index-1] = 1
            if col < size - 1: # Right
                matrix[index, index+1] = 1
            if row > 0: # Up
                matrix[index, index-size] = 1
            if row < size - 1: # Down
                matrix[index, index+size] = 1
            # Diagonal neighbors
            if row > 0 and col > 0: # Top-left
                matrix[index, index-size-1] = 1
            if row > 0 and col < size - 1: # Top-right
                matrix[index, index-size+1] = 1
            if row < size - 1 and col > 0: # Bottom-left
                matrix[index, index+size-1] = 1
            if row < size - 1 and col < size - 1: # Bottom-right
                matrix[index, index+size+1] = 1
    return matrix

# Create a 5x5 grid adjacency matrix
grid_size = 5
adjacency_matrix = create_adjacency_matrix(grid_size)
market_grid_df = pd.read_csv('market_grid.csv').astype(str)

# Initialize lists to store the 'label' and 'degree' values
labels = []
degrees = []

# Iterate through the DataFrame to extract 'label' and 'degree'
print(em.bids)
for _, row in market_grid_df.iterrows():
    for cell in row[1:]:  # Skip the index column
        if cell != '0':  # Check if the cell is not '0'
            bid: Bid = em.hash_to_bid(cell)

            parts = cell.split('_')
            label = parts[0]  # The 'label' is the 0th index of the split string
            degree = bid.quantity
            # degree = int(parts[1])  # The 'degree' is the 1st index of the split string
            labels.append(label)
            degrees.append(degree)
        else:
            labels.append('0')
            degrees.append(0)  # Keep degree as 0 for '0' values to later set node size to 0

# Create a new DataFrame with 'label' and 'degree'
transformed_df = pd.DataFrame({'label': labels, 'degree': degrees})

# Display the transformed DataFrame
# print("Transformed DataFrame:")
# print(transformed_df)

d3.graph(adjacency_matrix)
# Set node size to 0 for nodes with 'degree' value 0
node_size = [0 if degree == 0 else degree for degree in transformed_df['degree'].values]
colors = []
for label in transformed_df['label'].values:
    if label.startswith('B'):
        colors.append('#00E0BD')
    elif label.startswith('j'):  # Example condition for elif
        colors.append('#3CEE04')  # Example color for elif condition
    else:
        colors.append('#FFFFFF')
d3.set_node_properties(color=colors, size=node_size)

d3.show()
