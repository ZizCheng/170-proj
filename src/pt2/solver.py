import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room, convert_dictionary
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
    
    #return greedyHappinessTraverser(G, s)
    return brute_forcer(G, s, 3)
    #return randomizedSolver(G, s, 1000)
    #return initDictionary(len(G.nodes)), 1

    pass

def greedyHappinessTraverser(G, s):
    # This algo uses a starting point of highest theoretical happiness: 1 room. 
    # Every move that the algo makes is to minimize the happiness lost by each turn.
    print("Starting")
    num_students = len(G.nodes)
    singleroom_dictionary = initDictionary(num_students)

    if is_valid_solution(singleroom_dictionary, G, s, 1):
        return singleroom_dictionary, s
    
    max_happy = 0
    numrooms = 2
    current_dictionary = {0: [i for i in range(0, num_students)]}
    found = False
    while not found:
        for k in range(2, num_students - 1):
            current_dictionary[k-1] = []
            sat = False
            cashe = {str(current_dictionary): 0}
            while not sat:
                current_dictionary = makeMove(current_dictionary, k, G, cashe)
                if current_dictionary == False:
                    sat = True
                elif is_valid_solution(convert_dictionary(current_dictionary), G, s, k):
                    found = True
                    sat = True
                    numrooms = k
                elif min(getStressList(current_dictionary, k)) > s/k or cashe.get(str(current_dictionary), 0) is k - 1:
                    sat = True
    
                    
    return convert_dictionary(current_dictionary), k

def getStressList(current_dictionary, rooms):
    stress_list = []
    for k in range(0, rooms):
        stress_list.append(calculate_stress_for_room(current_dictionary.get(k), G))
    return stress_list


import copy
def makeMove(dic, k, G, cashe):
    stress = getStressList(dic, k)
    stressSorted = stress.copy()
    stressSorted.sort()
    max_stress_value = stressSorted[len(stress)-1]
    max_stressed_room = stress.index(max_stress_value)

    min_num = cashe.get(str(dic), 0)
    if min_num == len(stress) - 1:
        return dic
    
    min_stressed_room = stress.index(stressSorted[min_num])
    maxH = -1
    maxDic = dic.copy()
    # print(stress, dic)
    for i in dic.get(max_stressed_room):
        tempdic = copy.deepcopy(dic)
        # print(tempdic, i, max_stressed_room, min_stressed_room, tempdic.get(max_stressed_room))
        tempdic.get(min_stressed_room).append(i)
        tempdic.get(max_stressed_room).remove(i)
        # print(tempdic)
        currentH = calculate_happiness(convert_dictionary(tempdic), G)
        if currentH > maxH:
            maxH = currentH
            maxDic = tempdic.copy()
    cashe[str(maxDic)] = cashe.get(str(maxDic), -1) + 1
    return maxDic


def greedySolutionFinder(G, s):
    # This algo uses a starting point of highest theoretical happiness: 1 room, and expands rooms from there trying to just find a valid solution. 
    # The pretense is that the smaller the number of rooms the more likey the solution is more optimal than a solution with +n more rooms. 

    num_students = len(G.nodes)
    singleroom_dictionary = initDictionary(max_breakout_rooms)

    if is_valid_solution(singleroom_dictionary, G, s, 1):
        return singleroom_dictionary, s
    
    max_happy = 0
    numrooms = 2
    current_dictionary = {0: [i for i in range(0, num_students)]}
    found = False

    # Go through all the rooms and find the room with the most stress. In that room, find the individual causing the most stress. Move that individual.
    while not found:
        max_stress_room = -1
        max_stress = -1
        sat = True
        for k in range(0, 2):
            if calculate_stress_for_room(current_dictionary.get(k, default=0)):
                sat = 111

    # If moving that individual puts all rooms below the budget s, then a solution is found

    # TODO: optimize happiness on a valid solution.
    return 1





def find_trivial(G, s):
    best_dictionary = initDictionary(len(G.nodes))
    if is_valid_solution(best_dictionary, G, s, 1):
        return best_dictionary, 1
    return False

def brute_forcer(G, s, depth):
    max_breakout_rooms = len(G.nodes)
    ans = find_trivial(G, s)
    if ans is True:
        return ans[0], ans[1]

    max_happy = -1
    numrooms = -1
    best = initDictionary(max_breakout_rooms)
    for k in range(2, min(depth, max_breakout_rooms+1)):
        still_going = True
        current_dictionary = initDictionary(max_breakout_rooms)
        ct = 0
        while still_going:
            if ct%1000 == 0:
                print(ct, end=", ")
            ct = ct + 1
            current_dictionary, still_going = permuteDictionary(current_dictionary, max_breakout_rooms, k)
            if is_valid_solution(current_dictionary, G, s, k):
                currhappy = calculate_happiness(current_dictionary, G)
                if currhappy > max_happy:
                    max_happy = currhappy
                    best = current_dictionary.copy()
                    numrooms = k
    print("HAPPINESS: ", max_happy)
    return best, numrooms
    
def randomizedSolver(G, s, checker_resolution):
    max_breakout_rooms = len(G.nodes)
    best_dictionary = initDictionary(max_breakout_rooms)
    if is_valid_solution(best_dictionary, G, s, 1):
        max_happy = calculate_happiness(best_dictionary, G)     
    else:
        max_happy = 0
    numrooms = -1    
    for k in range(2, max_breakout_rooms+1):
        for j in range(0, checker_resolution):
            if j%10000 is 0:
                print(str(k) + ' ' + str(j))
            current_dictionary = randomlyDictionary(max_breakout_rooms, k - 1)
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
    # print(breakout_rooms)
    # print(d)
    # print(d.get(user))
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

import glob
# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('input/small/*')
    for input_path in inputs:
        output_path = 'output/small/' + "".join(filter(str.isdigit, input_path[-6:-3])) + '.out'
        G, s = read_input_file(input_path, 100)
        D, k = solve(G, s)
        
        if is_valid_solution(D, G, s, k):
            cost_t = calculate_happiness(D, G)
            print(D, cost_t, "".join(filter(str.isdigit, input_path[-6:-3])))
            write_output_file(D, output_path)

# if __name__ == '__main__':
#     inputs = glob.glob('/input/small/*')
#     for input_path in inputs:
#         output_path = '/output/small/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         print(D)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)
