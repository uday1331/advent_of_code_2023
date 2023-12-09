import os 
from math import lcm

direction_to_index = {"L": 0, "R": 1}

def find_target(graph, instructions, index, node, target_fn):
    step_count = 0
    while not target_fn(node):
        step_count += 1

        instruction = instructions[index]
        instruction_index = direction_to_index[instruction]
        node = graph[node][instruction_index]

        index = (index + 1) % len(instructions)
    
    return step_count

def node(node_line):
    node, neighbors = node_line.split(" = ")
    neighborLeft, neighborRight = neighbors[1: -1].split(", ")

    return (node, (neighborLeft, neighborRight))

def graph(node_lines):
    network_graph = {}

    for node_line in node_lines:
        key, value = node(node_line)
        network_graph[key] = value
    
    return network_graph

def part1(network, instructions):
    return find_target(network, instructions, 0, "AAA", lambda node: node == "ZZZ")

def part2(network, instructions):
    start_nodes = [node for node in network.keys() if node[-1] == "A"]
    z_occurances = [find_target(network, instructions, 0, node, lambda node: node[-1] == "Z") for node in start_nodes]
    
    return lcm(*z_occurances)

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        lines = [line.rstrip() for line in my_file]

        instructions, graph_lines = lines[0], lines[2:]
        network = graph(graph_lines)

        # print(part1(network, instructions))
        print(part2(network, instructions))