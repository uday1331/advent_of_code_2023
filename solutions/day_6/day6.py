import os
import re

def numbers(number_line):
    numbers = re.split("[ ]{1,}", number_line.strip())
    return [int(num) for num in numbers]

def count_ways(time, distance):
    count = 0

    for step in range(1, time + 1):
        if step * (time - step) > distance:
            count += 1
        
    return count

def product_of_ways(times, distances):
    product = 1
    for time, distance in zip(times, distances):
        product *= max(1, count_ways(time, distance))
    
    return product

def part1():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        time_line, distance_line = [line.rstrip() for line in my_file]

        time_list, distance_list = numbers(time_line.split(":")[1]), numbers(distance_line.split(":")[1])

        return product_of_ways(time_list, distance_list)
    
def part2():
    return count_ways(40817772, 219101213651089)

if __name__ == "__main__":
    print(part1())
    print(part2())

