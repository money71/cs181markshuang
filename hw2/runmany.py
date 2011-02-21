import sys
import os
from subprocess import *

iterations = 2

rounds = 16

hiddens = [0]

rates = [.2, .3, .4, .5, .8, 1.0, 1.2, 1.5]

rounds_data = open("rounds_data.txt","w")


print "  rate  rnds  hide  corr  total"
rounds_data.write("  rate  rnd   hide    train      valid\n")
if __name__=='__main__':
  for i in range(iterations):
    for hidden in hiddens:
      for rate in rates:
        thisargs =  ["python","nn.py", "-l", str(rate),"--hidden="+str(hidden),\
                     "-n",str(rounds),"2>&1"]
        outfile = "full_rounds%d_hidden%d_rate%f_%d.txt" % (rounds, hidden, rate, i)
        outfd = open(outfile, "w")
        output = Popen(thisargs, stderr=outfd,stdout=PIPE).communicate()[0]
        outfd.close()
        tok = output.split()
        print "%5.2f %5d %5d %5s %5s" % (rate, rounds, hidden, tok[4], tok[7])
        infile = outfile
        infd = open(infile, "r")
        infd.readline()
        infd.readline()
        infd.readline()
        rnd = 0
        for line in infd:
          rnd += 1
          tok = line.split(": ")
          train = tok[1].split(',')[0]
          val   = tok[2]
          roundstr = "%5.2f %5d %5d %10s %10s" % (rate, rnd, hidden, train, val)
          rounds_data.write(roundstr)
          rounds_data.flush()
        infd.close()

rounds_data.close()

