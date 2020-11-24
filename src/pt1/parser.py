

def getParams(filename) :
    n = 0
    stress_budget = 0
    data = []
    with open(filename) as f:
        read_data = int(f.readline)
        stress_budget = float(f.readline)
        for i in range (0, n):
            student = f.readline
            data.append(student.split(" "))
    # We can check that the file has been automatically closed.
    f.closed
    data = convertDataToInts(data)
    return n, stress_budget, data

def convertDataToInts(data):
    for i in data:
        track = 0
        for e in len(i):
            if track <= 1:
                i[e] = int(i[e])
            else:
                i[e] = float(i[e])
            track += 1
    return data
    