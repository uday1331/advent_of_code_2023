import os
from functools import cache

@cache
def is_spring_at(spring_row, start_index, match_length):
    if start_index + match_length > len(spring_row):
        return False
    
    for index in range(start_index, start_index + match_length):
        if spring_row[index] not in ["#", "?"]: 
            return False
    
    if index + 1 < len(spring_row) and spring_row[index + 1] == "#": 
        return False
    
    return True

# 1. if spring_row[index] == "#": have to match current length
# 2. if spring_row[index] == "?": can be a match or can not be
# 3. if not 1, then check for match starting index + 1

memoise = {}

def find_ways(spring_row, index, spring_length_list):
    if index >= len(spring_row): return len(spring_length_list) == 0
    if len(spring_length_list) == 0: return spring_row[index: ].find("#") == -1

    key = (spring_row, index, "".join([str(l) for l in spring_length_list]))
    if key in memoise: 
        return memoise[key]

    match_length = spring_length_list.pop()
    found_spring = is_spring_at(spring_row, index, match_length)

    total = 0
    if found_spring: 
        total += find_ways(spring_row, index + match_length + 1, spring_length_list)
    
    spring_length_list.append(match_length)
    if spring_row[index] != "#": 
        total += find_ways(spring_row, index + 1, spring_length_list)
    
    memoise[key] = total
    return memoise[key]

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        records = [line.rstrip().split(" ") for line in my_file]
        
        spring_row_list = [sprint_row for sprint_row, _ in records]
        spring_length_lists = [[int(length) for length in sprint_length_list.split(",")] for _, sprint_length_list in records]

        total = 0
        for spring_row, spring_length_list in zip(spring_row_list, spring_length_lists):
            multiple = 5

            spring_length_list = (spring_length_list * multiple)
            spring_length_list.reverse()

            spring_row = "?".join([spring_row for _ in range(multiple)])

            total += find_ways(spring_row, 0, spring_length_list)
        
        print(total)

# ?#?#?#?#?#?#?#? 1,3,1,6
# #?#?#?#?#?#?#? and 3,1,6 | 