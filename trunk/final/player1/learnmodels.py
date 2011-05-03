#!/usr/bin/python

"""
learnmodels.py

Tries to learn optimal parameters and save models for each algorithm.
"""


from string import *
from svmutil import *
from dtreeutil import *
from annutil import *
from nbayesutil import *


# SVM parameters found using libsvm tools with cross-validated grid search.
CVALS = [0.125]
GVALS = [0.125]
# DT parameter
MAXROUNDS = 50
# NN parameters
EPOCHS = 30
RESTARTS = 3
LRATE = 0.05
HIDDEN = [20]


def load(filename):
    """Load targets and data from a file delimited with '>'."""
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
    """Learn an SVM."""
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
    print 'Optimized result: %f accuracy with parameters %s' % (
                                        svm_predict(yVal, xVal, m)[1][0], mPStr)


def learn_dt(train):
    """Learn a DT committee."""
    yTrain, xTrain = load(train)

    instTrain = dt_insts(yTrain, xTrain)
    
    listTestAcc = dt_list_acc(MAXROUNDS,instTrain)
    cRoundsBest = listTestAcc.index(max(listTestAcc))
    
    m = dt_build_model(instTrain, cRoundsBest+1)
    
    dt_save_model("dt.model", m)
    print 'Optimized result: %f accuracy with parameter %d rounds' % (
                                                max(listTestAcc), cRoundsBest)


def learn_ann(train, test, validate):
    """Learn a NN."""
    yTrain, xTrain = load(train)
    yTest, xTest = load(test)
    yVal, xVal = load(validate)
    
    patTrain = ann_data(yTrain, xTrain)
    patTest = ann_data(yTest, xTest)
    patVal = ann_data(yVal, xVal)
    
    ni = len(patTrain[0][0])
    no = len(patTrain[0][1])
    
    bestNh = 0
    bestIter = 0
    bestPerf = 0
    
    for nh in HIDDEN:
        for i in xrange(RESTARTS):
            iter, perf = ann_train(patTrain, patTest, ni, nh, no, LRATE, EPOCHS)
            if perf > bestPerf:
                bestNh = nh
                bestIter = iter
                bestPerf = perf
    
    m = ann_model(patTrain, ni, bestNh, no, LRATE, bestIter)
    
    ann_save_model("ann.model", m)
    print "Optimized result: %f accuracy with parameters %d epoch %d hidden" % (
                                            m.test(patVal), bestIter, bestNh)


def learn_nbayes(train, validate):
    """Learn a Naive Bayes model."""
    yTrain, xTrain = load(train)
    yVal, xVal = load(validate)
    
    dataTrain = nbayes_data(yTrain, xTrain)
    dataVal = nbayes_data(yVal, xVal)

    m = nbayes_model(dataTrain)
    
    nbayes_save_model("nbayes.model", m)
    print "Optimized result: %f accuracy" % (nbayes_test(m, dataVal))


def main(argv):
    import optparse
    parser = optparse.OptionParser()
    parser.add_option("--svm", action="store_true", dest="svm",
                      help="run svm learning")
    parser.add_option("--dt", action="store_true", dest="dt",
                      help="run dt learning")
    parser.add_option("--ann", action="store_true", dest="ann",
                      help="run ann learning")
    parser.add_option("--nbayes", action="store_true", dest="nbayes",
                      help="run nbayes learning")
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
    if opts.ann:
        learn_ann(opts.train, opts.test, opts.validate)
    if opts.nbayes:
        learn_nbayes(opts.train, opts.validate)
    return 0


if __name__ == "__main__":
  import sys
  main(sys.argv)
