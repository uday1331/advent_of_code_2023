import os

def in_range(num_rows, num_cols, point):
    row, col = point
    return row > -1 and col > -1 and row < num_rows and col < num_cols

def count_reflection_mismatches(grid, left, right, dleft, dright):
    num_rows, num_cols = len(grid), len(grid[0])
    count_mismatches = 0

    while in_range(num_rows, num_cols, left) and in_range(num_rows, num_cols, right):
        left_row, left_col = left
        right_row, right_col = right

        if grid[left_row][left_col] != grid[right_row][right_col]:
            count_mismatches += 1
        
        left = (left_row + dleft[0], left_col + dleft[1])
        right = (right_row + dright[0], right_col + dright[1])
    
    return count_mismatches

def find_mirror(grid, fault_tolerance):
    num_rows, num_cols = len(grid), len(grid[0])

    mirror_at_row = [0 for _ in range(num_rows - 1)]
    mirror_at_col = [0 for _ in range(num_cols - 1)]
    
    for row in range(num_rows):
        for col in range(num_cols):
            if row < num_rows - 1:
                mirror_at_row[row] += count_reflection_mismatches(grid, (row, col), (row + 1, col), (-1, 0), (1, 0))
            
            if col < num_cols - 1:
                mirror_at_col[col] += count_reflection_mismatches(grid, (row, col), (row, col + 1), (0, -1), (0, 1))
    
    mirror_row = next((row + 1 for row, faults in enumerate(mirror_at_row) if faults == fault_tolerance), None)
    mirror_col = next((col + 1 for col, faults in enumerate(mirror_at_col) if faults == fault_tolerance), None)
    
    return (mirror_row, mirror_col)

def sum_mirrors(grid_list, fault_tolerance):
    total = 0

    for grid in grid_list:
        mirror_row, mirror_col = find_mirror(grid, fault_tolerance)

        if mirror_row: total += (100 * mirror_row)
        elif mirror_col: total += mirror_col
    
    return total

def group(sequence, separator):
    current_group = []
    for elem in sequence:
        if elem == separator:
            yield current_group
            current_group = []
        else:
            current_group.append(elem)
    yield current_group

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        grid = [line.strip() for line in my_file]
        grid_list = list(group(grid, ""))
        
        print("Part 1:", sum_mirrors(grid_list, 0))
        print("Part 2:", sum_mirrors(grid_list, 1))
        # print(find_mirror(grid_list[0], 1))
        # print(is_perfect_reflection(grid_list[0], (0, 0), (0, 1), (0, -1), (0, 1), 1))