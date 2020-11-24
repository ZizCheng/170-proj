import random

def inputGen (num_students):
    print(num_students, end='\n')
    print(random.random()*100, end='\n')
    for i in range(0, num_students):
        for j in range(0, num_students):
            if i is not j:
                print(i, end=' ')
                print(j, end=' ')
                print(random.random()*100, end=' ')
                print(random.random()*100, end='\n')
