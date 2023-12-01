from functools import reduce
import os 

spelling_to_number = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9 
}

class Trie:
    def __init__(self):
        self.children = {}
        self.is_end = False

    def insert(self, word: str) -> None:
        current = self

        for char in word:
            if char not in current.children:
                current.children[char] = Trie()   
            current = current.children[char]
        
        current.is_end = True

        return self

def number_at(string, start):
    if string[start].isnumeric(): return int(string[start])

    current_node = number_trie
    for end in range(start, len(string)):
        if current_node.is_end:
            return spelling_to_number[string[start: end]]
        
        if string[end] not in current_node.children:
            return -1

        current_node = current_node.children[string[end]]

    if current_node.is_end:
        return spelling_to_number[string[start: end + 1]]
    
    return -1

def get_calibration_value(document_string):
    left, right = 0, len(document_string) - 1

    num_left, num_right = -1, -1
    while left <= right:
        num_left, num_right = number_at(document_string, left), number_at(document_string, right)
        if num_left != -1 and num_right != -1:
            return num_left * 10 + num_right

        left = left + 1 if num_left == -1  else left
        right = right - 1 if num_right == -1 else right
        
    return num_left or num_right

number_trie = reduce(lambda trie, word: trie.insert(word), spelling_to_number.keys(), Trie())

with open(os.path.join(os.path.dirname(__file__), "day1.txt")) as my_file:        
    total = 0
    for line in my_file:
        total += get_calibration_value(line)
    
    print(total)