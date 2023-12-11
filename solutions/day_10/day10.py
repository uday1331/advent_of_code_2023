import os

in_bounds = lambda grid, row, col: row >= 0 and col >= 0 and row < len(grid) and col < len(grid[0])

pipe_fns = {
    "-": {
        "E": lambda row, col: (row, col + 1, "E"),
        "W": lambda row, col: (row, col - 1, "W")
    },
    "|": {
        "S": lambda row, col: (row + 1, col, "S"),
        "N": lambda row, col: (row - 1, col, "N")
    },
    "L": {
        "S": lambda row, col: (row, col + 1, "E"),
        "W": lambda row, col: (row - 1, col, "N")
    },
    "J": {
        "S": lambda row, col: (row, col - 1, "W"),
        "E": lambda row, col: (row - 1, col, "N")
    },
    "7": {
        "N": lambda row, col: (row, col - 1, "W"),
        "E": lambda row, col: (row + 1, col, "S")
    },
    "F": {
        "N": lambda row, col: (row, col + 1, "E"),
        "W": lambda row, col:  (row + 1, col, "S")
    }
}

def find_start(grid):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "S":
                return (row, col)
    
    return (None, None)
            
def loop_steps(grid, row, col, direction):
    loop_coordinates = []

    while in_bounds(grid, row, col):
        if grid[row][col] == "S": return loop_coordinates
        if grid[row][col] == "." or direction not in pipe_fns[grid[row][col]]: return []
        
        loop_coordinates.append((row, col))
        pipe_fn = pipe_fns[grid[row][col]][direction]

        row, col, direction = pipe_fn(row, col)
    
    return []

def mark_connected_unenclosed(grid, forbidden_coordinates, start_row, start_col):
    stack = [(start_row, start_col)]

    while stack:
        row, col = stack.pop()

        if not in_bounds(grid, row, col) or (row, col) in forbidden_coordinates or grid[row][col] == "X": continue

        grid[row][col] = "X"

        stack.extend([(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)])

def mark_all_unenclosed(grid, forbidden_coordinates):
    num_rows, num_cols = len(grid), len(grid[0])

    for row in range(num_rows):
        mark_connected_unenclosed(grid, forbidden_coordinates, row, 0)
        mark_connected_unenclosed(grid, forbidden_coordinates, row, num_cols - 1)

    for col in range(num_cols):
        mark_connected_unenclosed(grid, forbidden_coordinates, 0, col)
        mark_connected_unenclosed(grid, forbidden_coordinates, num_rows - 1, col)

def count_dots(grid):
    num_rows, num_cols = len(grid), len(grid[0])

    count = 0
    for row in range(num_rows):
        for col in range(num_cols):
            if grid[row][col] == ".": count += 1
    
    return count

def part1(grid):
    start_row, start_col = find_start(grid)
    start_arguments = [(-1, 0, "N"), (1, 0, "S"), (0, -1, "W"), (0, 1, "E")]
    
    max_step_count = max([len(loop_steps(grid, start_row + dr, start_col + dc, direction)) for dr, dc, direction in start_arguments])

    return (max_step_count + 1) // 2

def part2(grid):
    start_row, start_col = find_start(grid)
    start_arguments = [(-1, 0, "N"), (1, 0, "S"), (0, -1, "W"), (0, 1, "E")]

    loop_coordinates_list = [loop_steps(grid, start_row + dr, start_col + dc, direction) for dr, dc, direction in start_arguments]
    loop_coordinates = next(loop for loop in loop_coordinates_list if loop)
    loop_coordinates.append((start_row, start_col))

    mark_all_unenclosed(grid, loop_coordinates)

    for row in grid:
        print("".join(row))
    

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        grid = [list(line.rstrip()) for line in my_file]

        print(part2(grid))