#!/usr/bin/python

"""
convert.py

Convert a training file to a libSVM file
"""


import random
from string import *


def main():
    f = open("test.dat")
    o = open("test_new.dat", "w")
    
    data = []
    targets = []
    
    for line in f:
        xt, yt = split(line,'>')
        x = split(xt)
        y = eval(yt)
        for i in range(len(x)):
            x[i] = eval(x[i])
        x[-4] = x[-4]/10
        x[-5] = x[-5]/10
        data.append(x)
        targets.append(y)
    
    for i in xrange(len(targets)):
        o.write(str(targets[i])+" ")
        for j in xrange(len(data[i])):
            o.write(str(j+1)+":"+str(data[i][j])+" ")
        o.write("\n")
        
    o.close()
    f.close()


if __name__ == "__main__":
  main()
