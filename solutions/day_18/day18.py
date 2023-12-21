import os
import numpy as np

[-3, -2, -1, 0, 1, 2, 3]
[0, 1, 2, 3, 4, 5, 6, 7]

DIRECTION = {
    "L": (0, -1),
    "U": (-1, 0),
    "R": (0, 1),
    "D": (1, 0),
    "0": (0, 1),
    "1": (1, 0),
    "2": (0, -1),
    "3": (-1, 0)
}

def instruction(line):
    direction, distance, _ = line.split(" ")

    return (DIRECTION[direction], int(distance))

def hex_instruction(line):
    _, __, hex_value = line.split(" ")
    hex_number, direction = hex_value[2: -2], hex_value[-2:-1]

    return (DIRECTION[direction], int(hex_number, 16))

def print_grid(grid):
    for row in grid:
        print("".join(row))

def print_loop(loop):
    min_row, max_row = loop["row_range"]
    min_col, max_col = loop["col_range"]
    marked = loop["marked"]

    print(min_row, max_row, min_col, max_col)

    grid = [["." for _ in range(min_col, max_col + 1)] for __ in range(min_row, max_row + 1)]

    for row in range(0, max_row - min_row + 2):
        for col in range(0, max_col - min_col + 2):
            if (min_row + row, min_col + col) in marked: 
                grid[row][col] = marked[(min_row + row, min_col + col)]

    print_grid(grid)

def create_loop(instructions):
    marked = {}

    row, col = 0, 0
    marked[(row, col)] = "#"

    min_row, max_row = float("inf"), -float("inf")
    min_col, max_col  = float("inf"), -float("inf")

    for direction, distance in instructions:
        drow, dcol = direction
        for _ in range(distance):
            row, col = row + drow, col + dcol

            min_row, max_row = min(min_row, row), max(max_row, row)
            min_col, max_col = min(min_col, col), max(max_col, col)
            
            marked[(row, col)] = "#"
    
    return {
        "marked": marked,
        "col_range": [min_col, max_col],
        "row_range": [min_row, max_row]
    }
    

def flood_fill(loop, row, col):
    min_row, max_row = loop["row_range"]
    min_col, max_col = loop["col_range"]
    marked = loop["marked"]

    stack = [(row, col)]

    while stack:
        row, col = stack.pop()

        if row < min_row or col < min_col or row > max_row or col > max_col or (row, col) in marked:
            continue

        marked[(row, col)] = "*"

        stack.append((row + 1, col))
        stack.append((row - 1, col))
        stack.append((row, col + 1))
        stack.append((row, col - 1))


def count_enclosed(loop):
    min_row, max_row = loop["row_range"]
    min_col, max_col = loop["col_range"]
    marked = loop["marked"]

    for row in range(min_row, max_row + 1):
        if (row, min_col) not in marked: flood_fill(loop, row, min_col)
        if (row, max_col) not in marked: flood_fill(loop, row, max_col)
    
    for col in range(min_col, max_col + 1):
        if (min_row, col) not in marked: flood_fill(loop, min_row, col)
        if (max_row, col) not in marked: flood_fill(loop, max_row, col)

    count = 0
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            if (row, col) not in marked or marked[(row, col)] == "#":
                count += 1
    
    return count

def part1(lines):
    instructions = [instruction(line) for line in lines]
    loop = create_loop(instructions)
    count = count_enclosed(loop)

    return count

####################################################################
################ FAST SOLUTION BELOW THIS ##########################
####################################################################
# For Shoelace formula, we don't need all the points on the border but only the ones that define the 
# loop, for eg: if there is a straight line, we only need to consider the two points - start and end
# of the line, so we can optimise there
# For Picks theorum, we also calculate the number of total points on the border, this can be done by
# simply adding all the distances + 1 (for the original point)
# refer: https://www.reddit.com/r/adventofcode/comments/18l0qtr/comment/kdveugr/

# https://stackoverflow.com/a/30408825

def get_loop_details(instructions):
    row, col = 0, 0
    coordinates = [(row, col)]

    num_points = 1
    for direction, distance in instructions:
        drow, dcol = direction
        row, col = row + distance * drow, col + distance * dcol
        num_points += distance
        coordinates.append((row, col))

    return (coordinates, num_points)

def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))


def shoe_lace_and_picks_theorum(instructions):
    coordinates, num_points = get_loop_details(instructions)
    coordinates = np.array(coordinates)

    return (PolyArea(coordinates[:, 0], coordinates[:, 1]) + num_points // 2 + 1)

def part1_faster(lines):
    instructions = [instruction(line) for line in lines]

    return shoe_lace_and_picks_theorum(instructions)

def part2(lines):
    instructions = [hex_instruction(line) for line in lines]

    return shoe_lace_and_picks_theorum(instructions)

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        lines = [line.rstrip() for line in my_file]

        print("Part 1:", part1(lines))
        print("Part 1:", part1_faster(lines))
        print("Part 2:", part2(lines))


        