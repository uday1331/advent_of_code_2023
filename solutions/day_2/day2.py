import os
from functools import reduce

limits = {
    "red": 12,
    "green": 13,
    "blue": 14 
}

def color_draw(color_str):
    number, color = color_str.strip().split()
    return [color, int(number)]

def draw(draw_string):
    draw = list((map(lambda color_str: color_draw(color_str), draw_string.split(","))))

    return {color: number for (color, number) in draw}

def draws(game_string):
    return list(map(lambda drw: draw(drw), game_string.split(";")))

def is_draw_possible(draw):
    return reduce(lambda result, color: result and draw[color] <= limits[color], draw.keys(), True)

def is_game_possible(draws):
    return all([is_draw_possible(draw) for draw in draws])

def weight(draws, id):
    return id if is_game_possible(draws) else 0

def reduce_draw(reduced, draw):
    def max_color(reduced, draw, color):
        if color in draw: reduced[color] = max(reduced[color], draw[color])
        return reduced

    return reduce(lambda reduced, color: max_color(reduced, draw, color), reduced.keys(), reduced)

def max_draw(draws):
    return reduce(lambda reduced, draw: reduce_draw(reduced, draw), draws, {
        "red": 0,
        "green": 0,
        "blue": 0 
    })

def power(draw):
    return reduce(lambda product, number: product * max(1, number), draw.values(), 1)

def part1():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:        
        total = 0
        for line in my_file:
            game_title, game = line.strip().split(":")
            _, id = game_title.split(" ")

            draw_list = draws(game)
            total += weight(draw_list, int(id))

        print(total)

def part2():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:        
        total = 0
        for line in my_file:
            _, game = line.strip().split(":")
            draw_list = draws(game)
            reduce_draw = max_draw(draw_list)

            total += power(reduce_draw)
        
        print(total)
            
# print(is_game_possible({
#     "red": 12,
#     "green": 13,
#     "blue": 14
# }))

# print(parse_draw(" 8 green, 6 blue"))

# print(is_game_possible(" 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"))
# print(is_game_possible(" 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"))

# print(reduce_draw({
#     "red": 10,
#     "green": 12,
#     "blue": 12 
# }, {
#     "red": 12,
#     "green": 10,
#     "blue": 10 
# }))

# print(power({
#     "red": 10,
#     "green": 12,
#     "blue": 12 
# }))

part1()
part2()