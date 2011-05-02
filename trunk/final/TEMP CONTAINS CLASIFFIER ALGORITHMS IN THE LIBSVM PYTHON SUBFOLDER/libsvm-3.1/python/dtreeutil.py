#!/usr/bin/env python

"""
dttasks.py -- problem set tasks for the CS181 decision tree problem set
"""

import pickle
import dtree

def get_list_acc(maxRounds,listInst):
    cFold = 10
    listTestAcc = []
    for cRounds in xrange(1,maxRounds+1):
        fxnGen = build_fold_gen(cRounds,False)
        score = dtree.cv_score(fxnGen(listInst,cFold))
        print "%d rounds, %f score" % (cRounds, score)
        listTestAcc.append(score)
    return listTestAcc
    
def get_insts(y, x):
    listInst = []
    for i in xrange(len(y)):
        listInst.append(dtree.Instance(x[i], bool(y[i])))
    return listInst

def build_fold_gen(cRounds, fUseTraining):
    def yield_folds(listInst,cFold):
        for cvf in dtree.yield_boosted_folds(listInst,cFold):
            cvf.cMaxRounds = cRounds
            if fUseTraining:
                cvf.listInstTest = cvf.listInstTraining
            yield cvf
    return yield_folds

def build_model(listInst, cRounds):
    return dtree.boost(listInst, cRounds)

def dt_save_model(filename, m):
    file = open(filename, 'w')
    pickle.dump(m, file)
    file.close()

def dt_load_model(filename):
    file = open(filename, 'r')
    m = pickle.load(file)
    file.close()
    return m

def dt_predict(data, m):
    inst = dtree.Instance(data, False)
    if dtree.classify_boosted(m,inst):
        return 1
    return 0