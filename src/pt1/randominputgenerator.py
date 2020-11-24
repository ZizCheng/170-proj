import random

def inputGen (num_students, filename):
    f = open(filename, 'w')
    f.write(str(num_students) + '\n')
    f.write(str(random.random()*100) + '\n')
    for i in range(0, num_students):
        for j in range(0, num_students):
            if i is not j:
                f.write(str(i) + ' ' + str(j) + ' ' + str(random.random()*100) +' ' +str(random.random()*100) + '\n')
    
    
    
