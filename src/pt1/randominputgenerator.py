import random

def inputGen (num_students, filename):
    f = open("input/" + filename, 'w')
    f.write(str(num_students) + '\n')
    f.write(str(round(random.random()*100, 3)) + '\n')
    for i in range(0, num_students):
        for j in range(0, num_students):
            if i is not j:
                f.write(str(i) + ' ' + str(j) + ' ' + str(round(random.random()*100, 3)) +' ' +str(round(random.random()*100, 3)) + '\n')
    
    
    
