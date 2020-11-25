import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import sys
import random
from math import floor

def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    
    randomizedSolver(G, s, 10000)

    
    pass

def brute_forcer(G, s):
    max_breakout_rooms = len(G.nodes)
    best_dictionary = initDictionary(max_breakout_rooms)
    if is_valid_solution(best_dictionary, G, s, 1):
        max_happy = calculate_happiness(best_dictionary, G)
    else:
        max_happy = 0
    numrooms = 0
    current_dictionary = best_dictionary
    for k in range(2, max_breakout_rooms+1):
        still_going = True
        current_dictionary = initDictionary(max_breakout_rooms)
        while still_going:
            current_dictionary, still_going = permuteDictionary(current_dictionary, max_breakout_rooms, k)
            if is_valid_solution(current_dictionary, G, s, k):
                currhappy = calculate_happiness(current_dictionary, G)
                if currhappy > max_happy:
                    max_happy = currhappy
                    best_dictionary = current_dictionary
                    numrooms = k
        print(max_happy)
    return best_dictionary, numrooms
    
def randomizedSolver(G, s, checker_resolution):
    max_breakout_rooms = len(G.nodes)
    best_dictionary = initDictionary(max_breakout_rooms)
    if is_valid_solution(best_dictionary, G, s, 1):
        max_happy = calculate_happiness(best_dictionary, G)
        
    else:
        max_happy = 0
    numrooms = 0    
    for k in range(2, max_breakout_rooms+1):
        for j in range(0, checker_resolution):
            if j%10000 is 0:
                print(str(k) + ' ' + str(j))
            current_dictionary = randomlyDictionary(max_breakout_rooms, k)
            if is_valid_solution(current_dictionary, G, s, k):
                currhappy = calculate_happiness(current_dictionary, G)
                if currhappy > max_happy:
                    max_happy = currhappy
                    best_dictionary = current_dictionary
                    numrooms = k
        print(max_happy)
    return best_dictionary, numrooms

def initDictionary(num):
    d = {}
    for i in range(0, num):
        d[i] = 0
    return d
    
def randomlyDictionary(num, breakout_rooms):
    d = {}
    for i in range(0, num):
        d[i] = floor(random.random()*breakout_rooms)
    return d

def permuteDictionary(d, num, breakout_rooms):
    permuted = False
    user = 0
    print(breakout_rooms)
    print(d)
    print(d.get(user))
    while not permuted and user < num:
        if int(d.get(user)) == breakout_rooms:
            d[user] = 0
            user += 1
        else:
            d[user] = int(d.get(user)) + 1
            permuted = True
    return d, permuted
        

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G, s = read_input_file(path)
#     D, k = solve(G, s)
#     assert is_valid_solution(D, G, s, k)
#     print("Total Happiness: {}".format(calculate_happiness(D, G)))
#     write_output_file(D, 'out/test.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)
