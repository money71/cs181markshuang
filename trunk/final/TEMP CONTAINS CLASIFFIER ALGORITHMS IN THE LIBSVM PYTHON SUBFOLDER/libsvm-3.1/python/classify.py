#!/usr/bin/python

from svmutil import *
from dtreeutil import *
from string import *

def get_class(data,mSVM,mDT):
    '''Run classifiers on data, which is a list of form
    [image, num_nutri_neighbors/9, num_poison_neighbors/9, x+y distance/50].'''
    
    labelSVM = round(svm_predict([0], [data], mSVM)[0][0])
    labelDT = dt_predict(data, mDT)
    
    #print "SVM says %d." % (labelSVM)
    #print "DT says %d." % (labelDT)
    
    return ((labelSVM + labelDT) / 2.0) >= 0.5

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
  
def main():
    mSVM = svm_load_model('svm.model')
    mDT = dt_load_model('dt.model')
    
    y, x = load('validate.dat')
    numTotal = len(x)
    numCorrect = 0.0
    for i in xrange(numTotal):
        if y[i] == get_class(x[i],mSVM,mDT):
            numCorrect += 1
    print "Error: %f" % (numCorrect/numTotal)


if __name__ == "__main__":
    main()