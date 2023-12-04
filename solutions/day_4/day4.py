import os
from collections import defaultdict

def parse_numbers(num_line):
    return set([num for num in num_line.split(" ") if len(num)])

def parse_card(card_line):
    number_list = card_line.split("|")
    return [parse_numbers(number_line.strip()) for number_line in number_list]

def matches(card):
    return len(card[0]) - len(card[0] - card[1])

def part1():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        total = 0

        for line in my_file:
            _, card_line = line.split(":")
            
            card = parse_card(card_line)
            num_matches = matches(card)

            if matches: total += (pow(2, num_matches - 1))
        
        return total

def part2():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        copy_count = defaultdict(int)

        for card_number, line in enumerate(my_file, 1):
            _, card_line = line.split(":")

            current_count = copy_count[card_number]
            card = parse_card(card_line)

            num_matches = matches(card)
            if not current_count and not num_matches:
                return sum(copy_count.values()) + max(copy_count.keys())
            
            for next_card in range(card_number + 1, card_number + num_matches + 1):
                copy_count[next_card] += (current_count + 1)
        
        return sum(copy_count.values()) + max(copy_count.keys())
    
if __name__ == '__main__':
    print(part2())
