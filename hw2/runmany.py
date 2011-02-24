import sys
import os
from subprocess import *

iterations = 4
depth = 3
rounds = 100
hidden = 0
#hiddens = [15,30]

rounds_data = open("00_rounds_data.txt","w")

print "  rate       max"
rounds_data.write("  rate   rnd     train     valid\n")
if __name__=='__main__':
  #for hidden in hiddens:
    for i in range(iterations):
        maxVal = [0, 0, 0.0, 0.0]
        #rate = .2
        #incr = .01
        rate = 2
        incr = .1
        for d in range(depth):
            for j in range(20):
                curMaxVal = [0, 0, 0.0, 0.0]
                args = ["python", "nnfast.py", "-l", str(rate),
                        "--hidden="+str(hidden), "-n", str(rounds),
                        #"--train=training-9k.txt", "--test=test-1k.txt",
                        #"--validation=validation-1k.txt", "--num_inputs=196",
                        #"--enable-stopping",
                        "2>&1"]
                outfile = "%d_hidden%d_rate%f.txt" % (i, hidden, rate)
                outfd = open(outfile, "w")
                Popen(args, stderr=outfd,stdout=PIPE).communicate()[0]
                outfd.close()
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
                    if curMaxVal[3] < val:
                        curMaxVal = [rate, rnd, train, val]
                roundstr = "%1.4f %5d  %8s  %8s" % (curMaxVal[0], curMaxVal[1],
                                                    curMaxVal[2], curMaxVal[3])
                rounds_data.write(roundstr)
                rounds_data.flush()
                infd.close()
                if curMaxVal[3] > maxVal[3]:
                    maxVal = curMaxVal
                elif curMaxVal[3] == maxVal[3] and curMaxVal[1] <= maxVal[1]:
                    maxVal = curMaxVal
                print "%1.4f  %8s" % (curMaxVal[0], curMaxVal[3])
                rate -= incr
            rate = maxVal[0]+incr
            incr = incr*0.1

rounds_data.close()