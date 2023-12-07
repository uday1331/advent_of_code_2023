import os

from collections import Counter
from enum import IntEnum
from functools import cmp_to_key

CardRank = IntEnum('CardRank', ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'])
CardRankWithJoker = IntEnum('CardRankWithJoker', ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A'])
TypeRank = IntEnum('TypeRank', ['High', 'Pair', '2Pair', '3Kind', 'FullHouse', '4Kind', '5Kind'])

def rank_hand_counter(counter):
    key_count = len(counter.keys())
    _, max_count = counter.most_common(1)[0]

    if max_count == 5: return TypeRank['5Kind']
    if max_count == 4: return TypeRank['4Kind']
    if max_count == 3 and key_count == 2: return TypeRank['FullHouse']
    if max_count == 3: return TypeRank['3Kind']
    if max_count == 2 and key_count == 3: return TypeRank['2Pair']
    if max_count == 2: return TypeRank['Pair']

    return TypeRank['High']

def rank_hand_with_joker(hand):
    if len(hand) != 5: return

    counter = Counter(hand)

    joker_count = counter["J"]
    if len(counter) == 1: return rank_hand_counter(counter)
    
    del counter["J"]
    max_rank, _ = counter.most_common(1)[0]
    counter[max_rank] += joker_count

    return rank_hand_counter(counter)

def rank_hand(hand):
    if len(hand) != 5: return

    counter = Counter(hand)
    return rank_hand_counter(counter)

def compare(hand1, hand2):
    type_rank1, type_rank2 = rank_hand(hand1), rank_hand(hand2)
    if type_rank1 != type_rank2:
        return type_rank1 - type_rank2
    
    for card1, card2 in zip(hand1, hand2):
        if card1 != card2:
            return CardRank[card1] - CardRank[card2]

    return 0

def compare_with_joker(hand1, hand2):
    type_rank1, type_rank2 = rank_hand_with_joker(hand1), rank_hand_with_joker(hand2)
    if type_rank1 != type_rank2:
        return type_rank1 - type_rank2
    
    for card1, card2 in zip(hand1, hand2):
        if card1 != card2:
            return CardRankWithJoker[card1] - CardRankWithJoker[card2]

    return 0

def plays(data_lines):
    return [line.split(" ") for line in data_lines]

def part1(play_list):
    play_list = plays(file_lines)
    play_comparator = lambda play1, play2: compare(play1[0], play2[0])

    total_winnings = 0
    for rank, (_, bet) in enumerate(sorted(play_list, key = cmp_to_key(play_comparator)), 1):
        total_winnings += (rank * int(bet))  
    
    return total_winnings

def part2(play_list):
    play_list = plays(file_lines)
    play_comparator = lambda play1, play2: compare_with_joker(play1[0], play2[0])

    total_winnings = 0
    for rank, (_, bet) in enumerate(sorted(play_list, key = cmp_to_key(play_comparator)), 1):
        total_winnings += (rank * int(bet))  
    
    return total_winnings

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as my_file:
        file_lines = [line.rstrip() for line in my_file]

        play_list = plays(file_lines)
        
        print(part1(play_list))
        print(part2(play_list))

        # print(int(rank_hand("AAAAA")))

# rank hand
# print(rank_hand("AAAAA"))
# print(rank_hand("AAAAB"))
# print(rank_hand("AAABB"))
# print(rank_hand("AAABC"))
# print(rank_hand("AABBC"))
# print(rank_hand("AABCD"))
# print(rank_hand("ABCDE"))

# compare
# print(compare("AAAAA", "AAAAB"))
# print(compare("AKQJT", "TJQKA"))

# rank hand with joker
# print(rank_hand_with_joker("AAAJJ"))
# print(rank_hand_with_joker("AAABJ"))
# print(rank_hand_with_joker("AABCJ"))
# print(rank_hand_with_joker("JABCD"))
# print(rank_hand_with_joker("JJJJJ"))

# 249659293