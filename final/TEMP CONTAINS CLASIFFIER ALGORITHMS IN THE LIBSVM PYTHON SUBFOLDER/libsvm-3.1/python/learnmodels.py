#!/usr/bin/python

from svmutil import *
from dtreeutil import *
from string import *


CVALS = [8,16,32,64,128,256,512,1024]
GVALS = [.5,.1,.05,.01,.005,.001,.0005,.0001,.00005,.00001]
MAXROUNDS = 30

def load(filename):
    data = []
    targets = []
    
    file = open(filename, 'r')
    
    for line in file:
        xt, yt = split(line,'>')
        x = split(xt)
        y = eval(yt)
        for i in range(len(x)):
            x[i] = eval(x[i])
        data.append(x)
        targets.append(y)
    
    return targets, data

def learn_svm(train, test, validate):
    yTrain, xTrain = load(train)
    yTest, xTest = load(test)
    yVal, xVal = load(validate)
    
    m = None
    mAcc = 0
    mPStr = ''
    for c in CVALS:
        for g in GVALS:
            pStr = "-c " + str(c) + " -g " + str(g)
            mTmp = svm_train(yTrain, xTrain, pStr)
            mTmpAcc = svm_predict(yTest, xTest, mTmp)[1][0]
            if mTmpAcc > mAcc:
                m = mTmp
                mAcc = mTmpAcc
                mPStr = pStr
    
    svm_save_model("svm.model", m)
    print "Optimized result: %f accuracy with parameters %s" % (
                                        svm_predict(yVal, xVal, m)[1][0], mPStr)

def learn_dt(train):
    yTrain, xTrain = load(train)

    instTrain = get_insts(yTrain, xTrain)
    
    listTestAcc = get_list_acc(MAXROUNDS,instTrain)
    cRoundsBest = listTestAcc.index(max(listTestAcc))
    
    m = build_model(instTrain, cRoundsBest+1)
    
    dt_save_model("dt.model", m)
    print "Optimized result: %f accuracy with parameter %d rounds" % (
                                                max(listTestAcc), cRoundsBest)

def main(argv):
    import optparse
    parser = optparse.OptionParser()
    parser.add_option("--svm", action="store_true", dest="svm",
                      help="run svm learning")
    parser.add_option("--dt", action="store_true", dest="dt",
                      help="run dt learning")
    parser.add_option("--train", action="store", dest="train",
                      default="train.dat",
                      help="file containing training instances")
    parser.add_option("--test", action="store", dest="test",
                      default="test.dat",
                      help="file containing testing instances")
    parser.add_option("--validate", action="store", dest="validate",
                      default="validate.dat",
                      help="file containing validation instances")
    opts, args = parser.parse_args(argv)
    if opts.svm:
        learn_svm(opts.train, opts.test, opts.validate)
    if opts.dt:
        learn_dt(opts.train)
    return 0


if __name__ == "__main__":
  import sys
  main(sys.argv)
