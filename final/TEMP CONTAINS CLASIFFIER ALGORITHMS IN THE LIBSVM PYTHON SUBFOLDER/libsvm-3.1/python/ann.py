#!/usr/bin/python

"""
ann.py

Implements artificial neural networks, modified from open-domain code by Neil
Schemenauer <nas@arctrix.com>.
"""


import math
import random
import string


def rand(a, b):
    """Calculate a random number where:  a <= rand < b."""
    return (b - a) * random.random() + a


def make_matrix(I, J, fill=0.0):
    """Make a matrix of size I, J"""
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m


class NN:
    def __init__(self, ni, nh, no):
        """Initialize with ni inputs, nh hidden, and no outputs."""
        # Number of input, hidden, and output nodes
        self.ni = ni + 1        # +1 for bias node
        self.nh = nh
        self.no = no

        # Activations for nodes
        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no
        
        # Create weights
        self.wi = make_matrix(self.ni, self.nh)
        self.wo = make_matrix(self.nh, self.no)
        # Set them to random vaules
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] = rand(-0.01, 0.01)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = rand(-0.01, 0.01)

        # Last change in weights for momentum
        self.ci = make_matrix(self.ni, self.nh)
        self.co = make_matrix(self.nh, self.no)

    def update(self, inputs):
        """Feed inputs forward through NN."""
        if len(inputs) != (self.ni - 1):
            raise ValueError('wrong number of inputs')

        # Input activations
        for i in range(self.ni - 1):
            self.ai[i] = inputs[i]

        # Hidden activations
        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = 1.0 / (1.0 + math.exp(-sum))

        # Output activations
        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = 1.0 / (1.0 + math.exp(-sum))

        return self.ao[:]

    def back_propagate(self, targets, N, M):
        """Backpropogate errors from target values."""
        if len(targets) != self.no:
            raise ValueError('wrong number of target values')

        # Calculate error terms for output
        outputDeltas = [0.0] * self.no
        for k in range(self.no):
            ao = self.ao[k]
            outputDeltas[k] = ao * (1-ao) * (targets[k] - ao)

        # Calculate error terms for hidden
        hiddenDeltas = [0.0] * self.nh
        for j in range(self.nh):
            sum = 0.0
            for k in range(self.no):
                sum = sum + outputDeltas[k] * self.wo[j][k]
            hiddenDeltas[j] = self.ah[j] * (1 - self.ah[j]) * sum

        # Update output weights
        for j in range(self.nh):
            for k in range(self.no):
                change = outputDeltas[k] * self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N * change + M * self.co[j][k]
                self.co[j][k] = change

        # Update input weights
        for i in range(self.ni):
            for j in range(self.nh):
                change = hiddenDeltas[j] * self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N * change + M * self.ci[i][j]
                self.ci[i][j] = change

        # Calculate error
        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5 * (targets[k] - self.ao[k])**2
        return error

    def test(self, patterns):
        """Return accuracy of test data."""
        hits = 0
        for p in patterns:
            hits = hits + self.compare(p[1], self.update(p[0]))
        hitRate = (100.0 * hits) / len(patterns)
        return hitRate

    def compare(self, targets, activations):
        """Compare NN output with label."""
        matches = 0
        for n in range(len(targets)):
            error = abs(targets[n] - activations[n])
            if error < 0.5:
                matches += 1
        if matches == self.no:
            return 1
        return 0

    def weights(self):
        """Print NN weights."""
        print 'Input weights:'
        for i in range(self.ni):
            print(self.wi[i])
        print '\n'
        print 'Output weights:'
        for j in range(self.nh):
            print(self.wo[j])

    def train(self, patterns, iterations=1000, N=0.5, M=0.1, testPatterns=None):
        """Train the NN and also test each iteration if testing data given."""
        # N: learning rate
        # M: momentum factor
        perf = []
        for i in xrange(iterations):
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error = error + self.back_propagate(targets, N, M)
            if testPatterns:
                rate = self.test(testPatterns)
                print 'Epoch %d: %f' % (i, rate)
                perf.append(rate)
        return perf


def demo():
    """Learn XOR."""
    pat = [[[0,0], [0]],
           [[0,1], [1]],
           [[1,0], [1]],
           [[1,1], [0]]]

    # Create a network with two input, two hidden, and one output nodes
    n = NN(2, 2, 1)
    # Train it with some patterns
    n.train(pat)
    # Test it
    print n.test(pat)


if __name__ == '__main__':
    demo()
