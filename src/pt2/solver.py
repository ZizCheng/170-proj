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
    #return brute_forcer_w_efficient_casheing(G, s, 3)
    #return greedyStressTraverser(G, s)
    #return greedyHappinessTraverser(G, s)
    #return brute_forcer(G, s, 4)
    #return randomizedSolver(G, s, 1000)
    #return initDictionary(len(G.nodes)), 1
    return happ(G, s)

    pass

def greedyHappinessTraverser(G, s):
    # This algo uses a starting point of highest theoretical happiness: 1 room. 
    # Every move that the algo makes is to minimize the happiness lost by each turn.
    print("Starting")
    num_students = len(G.nodes)
    singleroom_dictionary = initDictionary(num_students)

    if is_valid_solution(singleroom_dictionary, G, s, 1):
        return singleroom_dictionary, s
    
    max_happy = -1
    numrooms = 2
    current_dictionary = {0: [i for i in range(0, num_students)]}
    found = False
    while not found:
        for k in range(2, num_students - 1):
            
            current_dictionary[k-1] = []
            sat = False
            cashe = {str(current_dictionary): 0}
            while not sat:
                current_dictionary = makeHMove(current_dictionary, k, G, cashe)
 
                if is_valid_solution(convert_dictionary(current_dictionary), G, s, k):
                    found = True
                    sat = True
                    numrooms = k
                elif min(getStressList(current_dictionary, k)) > s/k or cashe.get(str(current_dictionary), 0) is k - 1:
                    sat = True
    
                    
    return convert_dictionary(current_dictionary), k

def getStressList(current_dictionary, rooms, G):
    stress_list = {}
    for k in range(0, rooms):
        stress_list[k] = calculate_stress_for_room(current_dictionary.get(k), G)
    return stress_list


import copy
def makeHMove(dic, k, G, cashe):
    stress = getStressList(dic, k, G)
    invLookup = {}
    for k,v in stress.items():
        try:
            invLookup[v].append(k)
        except KeyError:
            invLookup[v]=[k]
    keysSorted = list(stress.keys())
    stressSorted = list(stress.values())
    #print(invLookup)

    min_num = cashe.get(str(dic), 0)
    if min_num == k - 1:
        cashe[str(dic)] = cashe.get(str(dic), -1) + 1
        return dic
    
    listofmins = invLookup.get(min(stressSorted))

    for i in range(0, k):
        if not dic.get(i):
            listofmins = [i]
            break
    

    maxH = -1
    maxDic = dic.copy()
    # print(stress, dic)
    for min_stressed_room in listofmins:
        for max_stressed_room in invLookup.get(max(stressSorted)):
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


def greedyStressTraverser(G, s):
    # This algo uses a starting point of highest theoretical happiness: 1 room, and expands rooms from there trying to just find a valid solution. 
    # The pretense is that the smaller the number of rooms the more likey the solution is more optimal than a solution with +n more rooms. 

    print("Starting stress traverser")
    num_students = len(G.nodes)
    singleroom_dictionary = initDictionary(num_students)

    if is_valid_solution(singleroom_dictionary, G, s, 1):
        return singleroom_dictionary, s
    
    max_happy = -1
    numrooms = 2
    
    found = False
    while not found:
        for k in range(2, num_students - 1):
            current_dictionary = {0: [i for i in range(0, num_students)]}
            for i in range (1, k):
                current_dictionary[i] = []
            sat = False
            cashe = {str(current_dictionary): 0}
            while not sat:
                current_dictionary = makeSMove(current_dictionary, k, G, cashe)
 
                if is_valid_solution(convert_dictionary(current_dictionary), G, s, k):
                    found = True
                    sat = True
                    numrooms = k
                elif min(getStressList(current_dictionary, k)) > s/k or cashe.get(str(current_dictionary), 0) is k - 1:
                    sat = True
    
                    
    return convert_dictionary(current_dictionary), k


def makeSMove(dic, k, G, cashe):
    stress = getStressList(dic, k, G)
    invLookup = {}
    for k,v in stress.items():
        try:
            invLookup[v].append(k)
        except KeyError:
            invLookup[v]=[k]
    keysSorted = list(stress.keys())
    stressSorted = list(stress.values())
    #print(invLookup)

    min_num = cashe.get(str(dic), 0)
    if min_num == k - 1:
        cashe[str(dic)] = cashe.get(str(dic), -1) + 1
        return dic
    
    listofmins = invLookup.get(min(stressSorted))

    for i in range(0, k):
        if not dic.get(i):
            listofmins = [i]
            break
    

    maxS = 99999999999
    maxDic = dic.copy()
    # print(stress, dic)
    for min_stressed_room in listofmins:
        for max_stressed_room in invLookup.get(max(stressSorted)):
            for i in dic.get(max_stressed_room):
                tempdic = copy.deepcopy(dic)
                # print(tempdic, i, max_stressed_room, min_stressed_room, tempdic.get(max_stressed_room))
                tempdic.get(min_stressed_room).append(i)
                tempdic.get(max_stressed_room).remove(i)
                # print(tempdic)
                currentSMax = calculate_stress_for_room(tempdic.get(max_stressed_room), G)
                currentSMin = calculate_stress_for_room(tempdic.get(min_stressed_room), G)
                if currentSMax < maxS:
                    maxS = currentSMax
                    maxDic = tempdic.copy()
    cashe[str(maxDic)] = cashe.get(str(maxDic), -1) + 1
    return maxDic

def find_trivial(G, s):
    best_dictionary = initDictionary(len(G.nodes))
    if is_valid_solution(best_dictionary, G, s, 1):
        return best_dictionary, 1
    return False

def brute_forcer(G, s, depth):
    max_breakout_rooms = len(G.nodes)
    ans = find_trivial(G, s)
    if ans:
        return ans[0], ans[1]

    max_happy = -1
    numrooms = -1
    best = initDictionary(max_breakout_rooms)
    print("starting")
    for k in range(3, min(depth, max_breakout_rooms+1)):
        still_going = True
        current_dictionary = initDictionary(max_breakout_rooms)
        ct = 0
        while still_going:
            if ct%1000 == 0:
                print(current_dictionary)
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


def smallerSearchSpace(G, s):
    # Get rid of the trivial solution
    
    ans = find_trivial(G, s)
    if ans:
        return ans[0], ans[1]

    #Set up the maxes
    max_breakout_rooms = len(G.nodes)
    max_happy = -1
    numrooms = -1
    best_dictionary = {0: [i for i in range(max_breakout_rooms)]}
    found = False
    print("Searching")
    for k in range(max_breakout_rooms):
        
        search = createSearchList(G, s, k)

        if is_valid_solution(current_dictionary, G, s, k):
            found = True
            currhappy = calculate_happiness(current_dictionary, G)
            if currhappy > max_happy:
                max_happy = currhappy
                best = current_dictionary.copy()
                numrooms = k


class Node:

    def __init__(self, data):

        self.list = []
        self.data = data


    def PrintTree(self):
        print(self.data)

class s_list:

    def __init__(self, data, remaining):

        self.students = data
        self.remaining = remaining

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def printS(self):
        print(self.students, self.remaining)

def searchListHelper(G, s, k, student, remaining, studentList):
    # create the pairings for ind i
    changeMade = False
    for i in remaining:
        s_i = student + [i]
        s_i.sort()
        cp = remaining.copy()
        cp.remove(i)

        if s_list(tuple(s_i), cp) not in studentList:
            if calculate_stress_for_room(s_i, G) < s/k:
                changeMade = True
                studentList.append(s_list(tuple(s_i), cp))
                searchListHelper(G, s, k, s_i, cp, studentList)
    return studentList, changeMade

def createSearchTree(G, s, k):
    initialNode = Node("initial")

    allStudents = list(range(len(G.nodes)))
    allStudents.reverse()
    student = [allStudents.pop()]
    
    studentList = [s_list(tuple(student), allStudents)]
    searchList, changes = searchListHelper(G, s, k, student, allStudents, studentList)
    
    for i in searchList:
        tempNode = Node(i)
        initialNode.list.append(tempNode)
    
    # too long
    # populator(G, s, k, initialNode)
        
    return initialNode
    
def populator(G, s, k, parentNode):
    if k <= 0:
        return
    for childNode in parentNode.list:
            remainingStudents = childNode.data.remaining.copy()
            if not remainingStudents:
                return 
            singleStudent = [remainingStudents.pop()]
            studentList = [s_list(tuple(singleStudent), remainingStudents)]
            searchList, changes = searchListHelper(G, s, k, singleStudent, remainingStudents, studentList)
            for i in searchList:
                print(childNode.data.printS(), i.printS())
                tempNode = Node(i)
                childNode.list.append(tempNode)
                populator(G, s, k-1, childNode)
    return

def searchDicHelper(G, s, k, student, remaining, studentSet):
    # create the pairings for ind i
    for i in remaining:
        s_i = student + [i]
        s_i.sort()
        if tuple(s_i) not in studentSet:
            if calculate_stress_for_room(s_i, G) < s/k:
                studentSet.add(tuple(s_i))
                cp = remaining.copy()
                cp.remove(i)
                searchDicHelper(G, s, k, s_i, cp, studentSet)
    return studentSet

def createSearchDic(G, s, k):
    print("creating search Dic")
    sDic = {}
    for i in range(len(G.nodes())):
        allStudents = list(range(len(G.nodes)))
        allStudents.reverse()
        student = [i]
        allStudents.remove(i)
        studentSet = {tuple(student)}
        searchSet = searchDicHelper(G, s, k, student, allStudents, studentSet)
        sDic[i]  = searchSet
    return sDic

def smallerSubSpaceK(G, s, k):
    print("Starting")
    searchDic = createSearchDic(G, s, k)
    allStud = [i for i in range(len(G.nodes))]
    retList = []
    
    lens = [len(searchDic.get(i)) for i in range(len(G.nodes))]
    start = lens.index(min(lens))
    print(lens)
    print("Starting a search at depth: ", k, " W init len", min(lens))
    


    count = 0
    for i in searchDic.get(start):
        count += 1
        print("count, ", count)
        ans = {0: list(i)}
        used = list(i)
        notused = [x for x in allStud if x not in i]
        rm = 1
        r = searchHelper(G, s, rm, k, notused.copy(), used.copy(), searchDic, ans.copy())
        if r:
            retList.append(r)
    print("Finished Search")
    return retList





def searchHelper(G, s, rm, k, notused, used, searchDic, ans):
    returnList = []
    if not notused:
        return [ans]
    if rm <= k-1:
        newest = notused[-1]
        for j in searchDic.get(newest):            
            clear = True
            for x in j:
                if x in used:
                    clear = False
            if clear:
                usedcp = used.copy()
                notusedcp = notused.copy()
                anscp = copy.deepcopy(ans)

                usedcp.extend(j)
                notusedcp = [x for x in notused if x not in j]
                anscp[rm] = list(j)
                # print(used,notused)
                # print(ans, rm)
                ret = searchHelper(G, s, rm + 1, k, notusedcp, usedcp, searchDic, anscp)
                if ret:
                    returnList.append(ret)
        return returnList
    else:
        return False

                
def happ(G, s):
    for k in range(2, len(G.nodes())):
        print("iter: ", k)
        si, d = smallerSubSpaceKHappinessTraversed(G, s, k)
        if d:
            return convert_dictionary(si), k
    return False, False
        
def smallerSubSpaceKHappinessTraversed(G, s, k):
    print("Starting")
    notused = list(range(len(G.nodes)))
    # s_i = createSearchDicNotComplete(G, s, k, list(range(len(G.nodes))))
  
    
    print("Starting a search at depth: ", k)
    
    rm = 0
    used = []
    ans = {}
    while notused and rm < k:
        s_i = createSearchDicNotComplete(G, s, k, notused)
        ans[rm] = list(s_i).copy()
        used.extend(list(s_i).copy())
        notused = [x for x in notused if x not in used]
        rm = rm + 1
        
        

    print("Finished Search")
    done = True
    if notused:
        done = False

    return ans, done




def searchHelper(G, s, rm, k, notused, used, searchDic, ans):
    returnList = []
    if not notused:
        return [ans]
    if rm <= k-1:
        newest = notused[-1]
        for j in searchDic.get(newest):            
            clear = True
            for x in j:
                if x in used:
                    clear = False
            if clear:
                usedcp = used.copy()
                notusedcp = notused.copy()
                anscp = copy.deepcopy(ans)

                usedcp.extend(j)
                notusedcp = [x for x in notused if x not in j]
                anscp[rm] = list(j)
                # print(used,notused)
                # print(ans, rm)
                ret = searchHelper(G, s, rm + 1, k, notusedcp, usedcp, searchDic, anscp)
                if ret:
                    returnList.append(ret)
        return returnList
    else:
        return False


def searchDicHelperNotComplete(G, s, k, student, remaining, studentSet):
    # create the pairings for ind i
    maxH = -1
    maxcpRemain = []
    maxi = -1
    maxs_i = [-1]
    s_i = tuple(student)
    for i in remaining:
        s_i = student + [i]
        s_i.sort()
        if tuple(s_i) not in studentSet:
            if calculate_stress_for_room(s_i, G) < s/k:
                currH = calculate_happiness(convert_dictionary({0: s_i}), G)
                if currH > maxH:
                    maxs_i = s_i
                    maxcpRemain = remaining.copy()
                    maxi = i
                    maxH = currH
    if maxH >= 0:
        s_i = tuple(s_i)
        studentSet.add(s_i)
        maxcpRemain.remove(maxi)
        d_s_i, d_mH = searchDicHelperNotComplete(G, s, k, maxs_i, maxcpRemain, studentSet)
        if d_mH > maxH:
            s_i = d_s_i
            maxH = d_mH
        return s_i, maxH
    else:
        return tuple(student), 0

def createSearchDicNotComplete(G, s, k, inputlist):
    sDic = {}
    maxH = -1
    parsi = -1
    maxHind = -1
    maxsi = ()
    for i in inputlist:
        allStudents = inputlist.copy()
        allStudents.sort()
        allStudents.reverse()
        student = [i]
        allStudents.remove(i)
        studentSet = {tuple(student)}
        s_i, hap = searchDicHelperNotComplete(G, s, k, student, allStudents, studentSet)
        if hap > maxH:
            maxsi = s_i
            maxH = hap
            maxHind = i
        sDic[i]  = studentSet

    return maxsi     


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

def runner(input_path):
    
    output_path = 'output/large/' + "".join(filter(str.isdigit, input_path[-6:-3])) + '.out'
    G, s = read_input_file(input_path, 100)
    D, k = solve(G, s)
    if D and k:
        if is_valid_solution(D, G, s, k):
            cost_t = calculate_happiness(D, G)
            print(D, cost_t, "".join(filter(str.isdigit, input_path[-6:-3])))
            write_output_file(D, output_path)

import glob
import multiprocessing.dummy as mp 
# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('input/large/*')
    p=mp.Pool(12)
    p.map(runner,inputs) # range(0,1000) if you want to replicate your example
    p.close()
    p.join()
    for i in inputs:
        runner(i)

    
    

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
