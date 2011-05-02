#!/usr/bin/env python

"""
dtreeutil.py

Convenience functions for accessing decision trees.
"""


import pickle
import dtree

    
def dt_insts(y, x):
    """Make a list of dt instances out of targets and data."""
    listInst = []
    for i in xrange(len(y)):
        listInst.append(dtree.Instance(x[i], bool(y[i])))
    return listInst


def dt_list_acc(maxRounds, listInst):
    """Get a list of testing accuracies for each round of boosting."""
    cFold = 10
    listTestAcc = []
    for cRounds in xrange(1, maxRounds+1):
        fxnGen = dt_build_fold_gen(cRounds, False)
        score = dtree.cv_score(fxnGen(listInst, cFold))
        print "%d rounds, %f score" % (cRounds, score)
        listTestAcc.append(score)
    return listTestAcc


def dt_build_fold_gen(cRounds, fUseTraining):
    """Build cross-validated boosting committees."""
    def yield_folds(listInst, cFold):
        for cvf in dtree.yield_boosted_folds(listInst, cFold):
            cvf.cMaxRounds = cRounds
            if fUseTraining:
                cvf.listInstTest = cvf.listInstTraining
            yield cvf
    return yield_folds


def dt_build_model(listInst, cRounds):
    """Build boosted committee from instances"""
    return dtree.boost(listInst, cRounds)


def dt_save_model(filename, m):
    """Save a trained model to file."""
    file = open(filename, 'wb')
    pickle.dump(m, file)
    file.close()


def dt_load_model(filename):
    """Retrieve a trained model from file."""
    file = open(filename, 'r')
    m = pickle.load(file)
    file.close()
    return m


def dt_predict(data, m):
    """Classify an input."""
    inst = dtree.Instance(data, False)
    if dtree.classify_boosted(m, inst):
        return 1
    return 0
