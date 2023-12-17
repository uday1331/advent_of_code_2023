import os

UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)

REFLECTION_MAP = {
    "/": { 
        UP: [ RIGHT ], 
        RIGHT: [ UP ], 
        LEFT: [ DOWN ], 
        DOWN: [ LEFT ] 
    },
    "\\": { 
        UP: [ LEFT ], 
        LEFT: [ UP ], 
        RIGHT: [ DOWN ], 
        DOWN: [ RIGHT ]},
    "|": {
        LEFT: [ UP, DOWN ],
        RIGHT: [ UP, DOWN ]
    },
    "-": {
        UP: [ LEFT, RIGHT ],
        DOWN: [ LEFT, RIGHT ]
    },
}

def print_grid(grid):
    for row in grid:
        print("".join(row))

def light_grid(grid, start_coordinates, start_direction):
    stack = [(*start_coordinates, *start_direction)]

    energized_coordinates = set()
    memory = set()

    num_rows, num_cols = len(grid), len(grid[0])

    while stack:
        row, col, drow, dcol = stack.pop()
        direction = (drow, dcol)

        if row < 0 or col < 0 or row == num_rows or col == num_cols or (row, col, drow, dcol) in memory:
            continue

        memory.add((row, col, drow, dcol))
        energized_coordinates.add((row, col))

        object = grid[row][col]
        if object not in REFLECTION_MAP or direction not in REFLECTION_MAP[object]:
            stack.append((row + drow, col + dcol, drow, dcol))
            continue

        directions = REFLECTION_MAP[object][direction]
        for drow, dcol in directions:
            stack.append((row + drow, col + dcol, drow, dcol))
    
    return energized_coordinates

def part1(grid):
    return len(light_grid(grid, (0, 0), RIGHT))

def part2(grid):
    num_rows, num_cols = len(grid), len(grid[0])

    top = max(len(light_grid(grid, (0, col), DOWN)) for col in range(num_cols))
    bottom = max(len(light_grid(grid, (num_rows - 1, col), UP)) for col in range(num_cols))

    left = max(len(light_grid(grid, (row, 0), RIGHT)) for row in range(num_rows))
    right = max(len(light_grid(grid, (row, num_cols - 1), LEFT)) for row in range(num_rows))

    return max(top, bottom, left, right)
    
if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        grid = [list(line.rstrip()) for line in my_file]

        print("Part 1:", part1(grid))
        print("Part 2:", part2(grid))