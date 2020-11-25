import networkx as nx
from parse import write_input_file, write_output_file, read_output_file
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room
import sys
import random
from math import floor, log, ceil
import collections
from solver import solve

fileName = "20c2"
n = 20

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
        randomness = int(random.random()*log(len(students), 2))
        for i in range(min(len(students), expected_students_per_room + randomness)):
            D[students.pop()] = roomnum
        roomnum += 1
    return D, roomnum
    
getRand = lambda x, y : round(random.random() * (y - x) + x, 3)
goodRandStr = lambda : getRand(0.6, 0.2)
badRandStr = lambda : getRand(0.9, 0.4)
goodRandHap = lambda : getRand(100, 60)
badRandHap = lambda : getRand(80, 40)

def setEdgeWeights(G, D):
    roomstress = {}
    for i in range(n):
        for j in range(n):
            if i is not j:
                if D.get(i) == D.get(j):
                    G[i][j]['happiness'] = goodRandHap()
                    G[i][j]['stress'] = goodRandStr()
                else:
                    G[i][j]['happiness'] = badRandHap()
                    G[i][j]['stress'] = badRandStr()
    return G

def getMaxStressBud(G, D, numRooms):
    l = {}
    room_to_student = {}
    for k, v in D.items():
        room_to_student.setdefault(v, []).append(k)
    sm = 0
    for k, v in room_to_student.items():
        room_stress = calculate_stress_for_room(v, G)
        sm = max(sm, room_stress)
    return round(ceil(sm*numRooms) + random.random()*1, 3)


s = 1000
kF = 2
while s > 100:
    G = nx.Graph()
    G = initG(G)
    D, numRooms = createRoomMapping()
    G = setEdgeWeights(G, D)
    print()
    s = getMaxStressBud(G, D, numRooms)
    D = collections.OrderedDict(sorted(D.items()))
    print("Stress: " + str(s))
    print(calculate_happiness(D, G))
    if s < 100:
        writeInputOutput(G, s, D)
        read_output_file("output/"+ fileName+ ".out", G, s)
        solve(G, s)

