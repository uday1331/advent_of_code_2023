import os
import re

from functools import reduce

NUM_BOXES = 256

def operation(op_string):
    if re.match(r"[a-z]+=[0-9]", op_string):
        split_string = op_string.split("=")
        return ("=", split_string[0], int(split_string[1]))
    else:
        split_string = op_string.split("-")
        return ("-", split_string[0])

def ascii_hash(op_string):
    characters = list(op_string)

    hash_value = 0
    for char in characters:
        hash_value += ord(char)
        hash_value *= 17
        hash_value %= 256
    
    return hash_value

def apply_operation(op, boxes):
    op_char, label = op[:2]
    box_no = ascii_hash(label)             

    if op_char == "=":
        boxes[box_no][label] = op[-1]
    else:
        if label in boxes[box_no]:
            del boxes[box_no][label]
    
    return boxes

def part1(op_list):
    return sum([ascii_hash(op) for op in op_list])

def part2(op_list):
    initial_boxes = [{} for _ in range(NUM_BOXES)]
    operation_list = [operation(op_string) for op_string in op_list]

    boxes = reduce(lambda boxes, op: apply_operation(op, boxes), operation_list, initial_boxes)
    sum_focusing_power = 0

    for box_no, box in enumerate(boxes):
        for slot_no, focal_length in enumerate(box.values()):
            sum_focusing_power += (box_no + 1) * (slot_no + 1) * focal_length
    
    return sum_focusing_power
        

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        op_list = my_file.readline().split(",")

        print("Part 1:", part1(op_list))
        print("Part 2:", part2(op_list))