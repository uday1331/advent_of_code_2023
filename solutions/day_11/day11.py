import os 

def get_cosmos_data(grid):
    num_rows, num_cols = len(grid), len(grid[0])

    expandable_rows = [True for _ in range(num_rows)]
    expandable_cols = [True for _ in range(num_cols)]

    galaxy_coordinates = []

    for row in range(num_rows):
        for col in range(num_cols):
            if grid[row][col] == "#":
                galaxy_coordinates.append((row, col))
                expandable_rows[row] = False
                expandable_cols[col] = False
    
    return {
        "galaxy_coordinates": galaxy_coordinates,
        "expandable_rows": expandable_rows,
        "expandable_cols": expandable_cols
    }

# eg: 5 -> 9, indices are (5, 1) and (9, 4) => row; 5 -> 9 and col 1 -> 4
# print(distance((5, 1), (9, 4), expandable))
def distance(point1, point2, cosmos_data, expansion_value):
    row_min, row_max = min(point1[0], point2[0]), max(point1[0], point2[0])
    col_min, col_max = min(point1[1], point2[1]), max(point1[1], point2[1])

    expandable_rows, expandable_cols = cosmos_data["expandable_rows"], cosmos_data["expandable_cols"]

    distance = 0
    for row in range(row_min + 1, row_max + 1):
        if expandable_rows[row]: 
            distance += expansion_value
        else:
            distance += 1
    for col in range(col_min + 1, col_max + 1):
        if expandable_cols[col]: 
            distance += expansion_value
        else:
            distance += 1
    
    return distance

def sum_distance_pairs(cosmos_data, expansion_value):
    coordinates = cosmos_data["galaxy_coordinates"]
    num_coordinates = len(coordinates)

    total_distance = 0
    for start_index, point1 in enumerate(coordinates):
        for index in range(start_index + 1, num_coordinates):
            total_distance += distance(point1, coordinates[index], cosmos_data, expansion_value)
    
    return total_distance

def part1(cosmos_data):
    return sum_distance_pairs(cosmos_data, 2)

def part2(cosmos_data):
    return sum_distance_pairs(cosmos_data, 1_000_000)
    
if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        grid = [list(line.rstrip()) for line in my_file]

        cosmos_data = get_cosmos_data(grid)
        
        print(part1(cosmos_data))
        print(part2(cosmos_data))