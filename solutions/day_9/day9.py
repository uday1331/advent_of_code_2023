import os

def next_num(histories):
    if not any(histories): return 0

    next_history = [history - histories[index] for index, history in enumerate(histories[1:])]

    return histories[-1] + next_num(next_history)

def prev_num(histories):
    if not any(histories): return 0

    next_history = [history - histories[index] for index, history in enumerate(histories[1:])]

    return histories[0] - prev_num(next_history)

def history(history_line):
    return [int(num) for num in history_line.split(" ")]

def part1(histories):
    return sum([next_num(history) for history in histories])

def part2(histories):
    return sum([prev_num(history) for history in histories])

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        lines = [line.rstrip() for line in my_file]
        histories = [history(line) for line in lines]

        print(part1(histories))
        print(part2(histories))

        