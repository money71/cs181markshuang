#!/usr/bin/python

"""
annutil.py

Convenience functions for accessing neural networks.
"""


import pickle
import ann
from itertools import *


def ann_data(y,x):
    """Takes target, data values and returns formatted list for NN training."""
    pat = []
    for b,a in izip(y,x):
        pat.append([a,[b]])
    return pat


def ann_train(patTrain, patTest, ni, nh, no, N, iterations):
    """Train NN for iterations and return the best performing iteration."""
    n = ann.NN(ni,nh,no)
    perf = n.train(patTrain, iterations, N, 0, patTest)
    bestPerf = max(perf)
    return perf.index(bestPerf), bestPerf


def ann_model(patTrain, ni, nh, no, N, iterations):
    """Train NN and return the trained network."""
    n = ann.NN(ni,nh,no)
    n.train(patTrain, iterations, N, 0)
    return n


def ann_save_model(filename, m):
    """Save a trained model to file."""
    file = open(filename, 'wb')
    pickle.dump(m, file)
    file.close()


def ann_load_model(filename):
    """Retrieve a trained model from file."""
    file = open(filename, 'r')
    m = pickle.load(file)
    file.close()
    return m


def ann_predict(data, m):
    """Classify an input."""
    return round(m.update(data)[0])
