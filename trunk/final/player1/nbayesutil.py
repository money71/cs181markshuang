#!/usr/bin/python

"""
nbayesutil.py

Convenience functions for accessing naive bayes.
"""


import pickle
import nbayes
from itertools import *


def nbayes_data(y, x):
    """Generate data that nbayes can read from targets, data."""
    data = []
    for yi, xi in izip(y,x):
        xi.insert(0, yi)
        data.append(xi)
    return data


def nbayes_model(data):
    """Train a naive bayes model."""
    m = nbayes.Bayes(data)
    m.train()
    return m


def nbayes_save_model(filename, m):
    """Save a trained model to file."""
    file = open(filename, 'wb')
    pickle.dump(m, file)
    file.close()


def nbayes_load_model(filename):
    """Retrieve a trained model from file."""
    file = open(filename, 'r')
    m = pickle.load(file)
    file.close()
    return m


def nbayes_test(m, data):
    """Return classification accuracy on data."""
    numTotal = len(data)
    numCorrect = 0.0
    for i in xrange(numTotal):
        if data[i][0] == nbayes_predict(data[i][1:], m):
            numCorrect += 1
    return numCorrect/numTotal


def nbayes_predict(instance, m):
    """Classify an input."""
    return m.classify(instance)[0]
