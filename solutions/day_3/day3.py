import os
import re

def special_character(character):
    return character != "." and not character.isalnum()

def neighbors(row, col_start, col_end):
    same_row = [(row, col_start - 1), (row, col_end + 1)]
    above_row = [(row - 1, col) for col in range(col_start - 1, col_end + 2)]
    below_row = [(row + 1, col) for col in range(col_start - 1, col_end + 2)]
    
    return same_row + above_row + below_row

def adjacent_coordinates(engine_schematic, row, col_start, col_end):
    def valid_coordinate(row, col):
        return row > -1 and col > -1 and row < len(engine_schematic) and col < len(engine_schematic[0])
    
    return list(filter(lambda c: valid_coordinate(*c), neighbors(row, col_start, col_end)))

def adjacent_characters(engine_schematic, row, col_start, col_end):
    return [engine_schematic[row][col] for (row, col) in adjacent_coordinates(engine_schematic, row, col_start, col_end)]

def is_part_number(engine_schematic, row, col_start, col_end):
    return any(filter(lambda char: char != "." and not char.isalnum(), adjacent_characters(engine_schematic, row, col_start, col_end)))

def find_symbol(engine_schematic, symbol, row):
    return [(match.group(), match.start(), match.end()) for match in re.finditer(symbol, engine_schematic[row])]

def marked_schematic(engine_schematic):
    num_rows, num_cols = len(engine_schematic), len(engine_schematic[0])

    marker = [[None for _ in range(num_cols)] for __ in range(num_rows) ]

    for row in range(len(engine_schematic)):
        for number, start, end in find_symbol(engine_schematic, r'[0-9]+', row):
            for col in range(start, end):
                marker[row][col] = f"{number}@{row},{start},{end}"
    
    return marker

def reduced_adjacent(marked_schematic, row, col_start, col_end):
    adjacent_number_symbols = set(adjacent_characters(marked_schematic, row, col_start, col_end))
    adjacent_number_symbols.remove(None)

    return list(adjacent_number_symbols)

def part1(engine_schematic):
    total = 0

    for row in range(len(engine_schematic)):
        for number, start, end in find_symbol(engine_schematic, r'[0-9]+', row):
            if is_part_number(engine_schematic, row, start, end - 1):
                total += int(number)
    
    return total


def part2(engine_schematic):
    marked_numbers = marked_schematic(engine_schematic)
    total = 0

    for row in range(len(engine_schematic)):
        for _, start, end in find_symbol(engine_schematic, r'\*', row):
            adjacents = reduced_adjacent(marked_numbers, row, start, end - 1)
            
            if len(adjacents) == 2:
                total += int(adjacents[0].split("@")[0]) * int(adjacents[1].split("@")[0])
    
    return total

if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:        
        engine_schematic = [line.strip() for line in my_file]

        print(part1(engine_schematic))
        print(part2(engine_schematic))