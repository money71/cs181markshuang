#!/usr/bin/python

"""
classify.py

Classify data instances from trained models.
"""


from string import *
from svmutil import *
from dtreeutil import *
from annutil import *
from nbayesutil import *


def get_class(data, mSVM, mDT, mANN, mNBayes):
    """Run classifiers on data, which is a list of form
    [image, x % 10, y % 10, #n_nghbrs, #p_nghbrs, #xplr_nghbrs].
    """
    labelSVM = round(svm_predict([0], [data], mSVM)[0][0])
    labelDT = dt_predict(data, mDT)
    labelANN = ann_predict(data, mANN)
    labelNBayes = nbayes_predict(data, mNBayes)
    
    return (0.4*labelSVM + 0.1*labelDT + 0.2*labelANN + 0.3*labelNBayes) >= 0.5


def load(filename):
    """Load targets and data from a file delimited with '>'."""
    data = []
    targets = []
    
    file = open(filename, 'r')
    
    for line in file:
        xt, yt = split(line, '>')
        x = split(xt)
        y = eval(yt)
        for i in range(len(x)):
            x[i] = eval(x[i])
        data.append(x)
        targets.append(y)
    
    return targets, data


def main():
    """Run classification over a validation set to test performance."""
    mSVM = svm_load_model('svm.model')
    mDT = dt_load_model('dt.model')
    mANN = ann_load_model('ann.model')
    mNBayes = nbayes_load_model('nbayes.model')
    
    y, x = load('validate.dat')
    numTotal = len(x)
    numCorrect = 0.0
    for i in xrange(numTotal):
        if y[i] == get_class(x[i], mSVM, mDT, mANN, mNBayes):
            numCorrect += 1
    print 'Error: %f' % (numCorrect / numTotal)


if __name__ == "__main__":
    main()
