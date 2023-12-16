import os

def grid_load(grid):
    num_rows = len(grid)

    total_load = 0
    for index, row in enumerate(grid):
        total_load += (num_rows - index) * row.count("O")
    
    return total_load

def rotate_right(grid):
    low, high = 0, len(grid) - 1

    while low < high:
        for index in range(high - low):
            first_value = grid[low][low + index]
            grid[low][low + index] = grid[high - index][low]
            grid[high - index][low] = grid[high][high - index]
            grid[high][high - index] = grid[low + index][high]
            grid[low + index][high] = first_value
        
        low, high = low + 1, high - 1
    
def tilt_north(grid):
    len_grid = len(grid)

    for col in range(len_grid):
        top = 0
        for bottom in range(len_grid):

            if grid[bottom][col] == "#":
                top = bottom + 1

            if grid[bottom][col] == "O":
                while top <= bottom and grid[top][col] not in [".", "O"]:
                    top += 1
                
                grid[bottom][col] = "."
                grid[top][col] = "O"

                top += 1

def tilt_cycle(grid):
    tilt_north(grid)
    rotate_right(grid)

    tilt_north(grid)
    rotate_right(grid)

    tilt_north(grid)
    rotate_right(grid)

    tilt_north(grid)
    rotate_right(grid)

def hash_grid(grid):
    return "/".join(["".join(row) for row in grid])

def part1(grid):
    tilt_north(grid)

    print("Part 1:", grid_load(grid))

def print_grid(grid):
    for row in grid:
        print("".join(row))

def part2(grid, times):
    time = 0

    last_seen = { hash_grid(grid): 0 }
    for time in range(1, times + 1):
        tilt_cycle(grid)

        key = hash_grid(grid)
        if key in last_seen:
            break

        last_seen[key] = time
        time += 1
    
    start = last_seen[key]
    cycle = time - start
    
    time_to_grid = {}
    for grid, time in last_seen.items():
        time_to_grid[time] = grid
    
    result_value = time_to_grid[start + (times - start) % cycle]
    result_grid = [list(row) for row in result_value.split("/")]

    print("Part 2:", grid_load(result_grid))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        grid = [list(line.strip()) for line in my_file]
        
        # part1(grid)
        part2(grid, 1_000_000_000)
