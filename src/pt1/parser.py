

def getParams(filename) :
    n = 0
    stress_budget = 0
    data = []
    with open("input/" + filename) as f:
        n = f.readline
        stress_budget = f.readline
        for i in range (0, n):
            student = f.readline
            data.append(student.split(" "))
    # We can check that the file has been automatically closed.
    f.closed
    return n, stress_budget, data
