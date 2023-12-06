import os 

from ast import Tuple
from typing import List
from functools import reduce

def source_to_destination(source_start, destination_start, input):
    return destination_start + (input - source_start)

def map_source(map, source):
    for ((source_start, source_end), (destination_start, _)) in map.items():
        if source >= source_start and source <= source_end:
            return source_to_destination(source_start, destination_start, source)
    
    return source

# interval1 - interval2
# example: 
# subtract_interval((1, 10), (2, 5))   -> ((2, 5), [(1, 1), (6, 10)])
# subtract_interval([1, 10], [11, 13]) -> ((), [])
def split_by_intersection(interval1, interval2):
    intersection = max(interval1[0], interval2[0]), min(interval1[1], interval2[1])
    
    remainder = []
    if intersection[0] != interval1[0]:
        remainder.append((interval1[0], intersection[0] - 1))
    if intersection[1] != interval1[1]:
        remainder.append((intersection[1] + 1, interval1[1]))

    return (intersection[0], intersection[1]), remainder

def intersects(interval1, interval2):
    return max(interval1[0], interval2[0]) <= min(interval1[1], interval2[1])

def map_ranges(map, unmapped):
    mapped = []

    while unmapped:
        current_range = unmapped.pop()

        match_source, match_destination = next((item for item in map.items() if intersects(current_range, item[0])), (None, None))
        if not match_source:
            mapped.append(current_range)
            continue

        intersection, remainder = split_by_intersection(current_range, match_source)
        destination_interval = (source_to_destination(match_source[0], match_destination[0], intersection[0]), 
                                source_to_destination(match_source[0], match_destination[0], intersection[1]))
        
        mapped.append(destination_interval)
        unmapped.extend(remainder)

    return mapped

def seeds(seeds_line):
    seed_numbers = seeds_line.split(":")[1].strip().split(" ")
    return [int(num) for num in seed_numbers]

def seed_ranges(seeds_line):
    seed_list = seeds(seeds_line)

    return [(seed_list[i], seed_list[i] + seed_list[i + 1] - 1) for i in range(0, len(seed_list), 2)]

def mapping(map_line):
    destination, source, range = [int(num) for num in map_line.split(" ")]
    return ((source, source + range - 1), (destination, destination + range - 1))
    
def consecutive_maps(map_lines):
    def reduce_line(map_list, line):
        if not line: return map_list

        if line.find("map:") != -1:
            map_list.append({})
        else:
            key, value = mapping(line)
            map_list[-1][key] = value
        
        return map_list
    
    return reduce(lambda map_list, line: reduce_line(map_list, line), map_lines, [])

def part1():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        lines = [line.rstrip() for line in my_file]

        first, rest = lines[0], lines[1:]
        seed_list, map_list = seeds(first), consecutive_maps(rest)

        destination_fn = lambda source, map: map_source(map, source)
        return min([reduce(destination_fn, map_list, seed) for seed in seed_list])
    
def part2():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        lines = [line.rstrip() for line in my_file]

        first, rest = lines[0], lines[1:]
        source_list, map_list = seed_ranges(first), consecutive_maps(rest)

        # find intersections for source intervals consecutively through every map
        map_list.reverse()
        while map_list: source_list = map_ranges(map_list.pop(), source_list)
        
        return min([source[0] for source in source_list])

if __name__ == '__main__':
    print(part1())
    print(part2())

# print(split_by_intersection([1, 10], [2, 5]))
# print(split_by_intersection([2, 5], [1, 10]))
# print(split_by_intersection([1, 11], [1, 10]))
# print(split_by_intersection([11, 11], [1, 10]))
# print(split_by_intersection([1, 10], [11, 13]))
# print(map_ranges({(98, 99): (50, 51), (50, 97): (52, 99)}, [(79, 93)]))