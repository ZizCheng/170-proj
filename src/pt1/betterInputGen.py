import networkx as nx
from parse import write_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room
import sys
import random
from math import floor, log
import collections

fileName = "50"
n = 50

def writeInputOutput(G, s, D):
    write_input_file(G, s, "input/" + fileName + ".in")
    write_output_file(D, "output/" + fileName + ".out")
    return

def initG(G):
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(n):
            if i != j:
                G.add_node(j)
                G.add_edge(i, j, happiness = 0, stress = 0)
    return G

def createRoomMapping():
    D = {}
    students = list(range(n))
    random.shuffle(students)
    expected_students_per_room = round(kF*log(len(students), 2))
    roomnum = 0
    while students:
        randomness = int(random.random()*0.5*log(len(students), 2))
        for i in range(min(len(students), expected_students_per_room + randomness)):
            D[students.pop()] = roomnum
        roomnum += 1
    return D, roomnum
    
getRand = lambda x, y : round(random.random() * (y - x) + x, 3)
goodRandStr = lambda : getRand(20, 0)
badRandStr = lambda : getRand(30, 15)
goodRandHap = lambda : getRand(100, 70)
badRandHap = lambda : getRand(85, 50)

def setEdgeWeights(G, D):
    roomstress = {}
    for i in range(n):
        for j in range(n):
            if i is not j:
                if D.get(i) == D.get(j):
                    G[i][j]['happiness'] = goodRandHap()
                    G[i][j]['stress'] = badRandStr()
                else:
                    G[i][j]['happiness'] = badRandHap()
                    G[i][j]['stress'] = goodRandStr()
    return G

def getMaxStress(G, D, numRooms):
    l = {}
    for i in range(n):
        for j in range(i, n):
            if i is not j:
                if D.get(i) == D.get(j):
                    l[D.get(i)] = l.get(D.get(i), 0) + G[i][j]['stress']
    return round(max(l.values()), 3)


s = 1000
kF = 0.5
while s > 100:
    G = nx.Graph()
    G = initG(G)
    D, numRooms = createRoomMapping()
    G = setEdgeWeights(G, D)
    s = getMaxStress(G, D, numRooms)
    D = collections.OrderedDict(sorted(D.items()))
    print("Stress: " + str(s))
    print(calculate_happiness(D, G))
    if s < 100:
        writeInputOutput(G, s, D)

