import random


f= open("1.txt","w+")
f.write("x,y\n")
for i in range(100000):
     f.write(" %f\n" % (random.uniform(0,1)))
f.close() 
