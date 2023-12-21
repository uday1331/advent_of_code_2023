import os
import heapq

from collections import namedtuple

Node = namedtuple('Node', ['coordinate', 'direction', 'direction_count'])
                                                             
in_bounds = lambda grid, row, col: row >= 0 and col >= 0 and row < len(grid) and col < len(grid[0])

def neighbors(row, col):
    return [ Node((row + dr, col + dc), (dr, dc), 1) for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)] ]

# using dijkshtra's
def shortest_path(grid, src_row, src_col):
    upper_limit = 3

    shortest = {}
    min_heap = [ (grid[src_row][src_col], Node(coordinate=(0, 0), direction=(1, 0), direction_count = 1)) ]

    while min_heap:
         distance, node = heapq.heappop(min_heap)
         if node.coordinate in shortest:
             continue
         
         shortest[node.coordinate] = distance

         for neighbor in neighbors(*(node.coordinate)):
            row, col = neighbor.coordinate

            if not in_bounds(grid, *(neighbor.coordinate)): continue

            neighbor_distance = distance + grid[row][col]
            if node.direction != neighbor.direction:
                 heapq.heappush(min_heap, (neighbor_distance, neighbor))
                 continue
            
            if node.direction_count < upper_limit:
                 heapq.heappush(min_heap, (neighbor_distance, Node(neighbor.coordinate, neighbor.direction, node.direction_count + 1)))
    
    print(shortest)







if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        grid = [[int(num) for num in line.rstrip()] for line in my_file]

        print(grid)
        shortest_path(grid, *(0, 0))