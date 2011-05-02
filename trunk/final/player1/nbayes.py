#!/usr/bin/python

"""
nbayes.py

Naive Bayes implementation, adapted from
http://guidetodatamining.com/home/toc/chapter-5/
"""


class Bayes:
    def __init__(self, data):
        # First column of the data is the class.
        self.data = data
        self.prior = {}
        self.conditional = {}
        
    def train(self):
        """Train the bayes classifier."""
        total = 0.0
        classes = {}
        counts = {}
        
        # Determine size of a training vector
        size = len(self.data[0])
        
        # Iterate through training instances
        for instance in self.data:
            total += 1.0
            category = instance[0]
            classes.setdefault(category, 0)
            counts.setdefault(category, {})
            classes[category] += 1.0
            
            # Now process each column in instance
            col = 0
            for columnValue in instance[1:]:
                col += 1
                tmp = {}
                if col in counts[category]:
                    tmp = counts[category][col]
                if columnValue in tmp:
                    tmp[columnValue] += 1.0
                else:
                   tmp[columnValue] = 1.0
                counts[category][col] = tmp
                
        # Compute prior probabilities
        for (category, count) in classes.items():
            self.prior[category] = count / total
            
        # Compute conditional probabilities
        for (category, columns) in counts.items():
            tmp = {}
            for (col, valueCounts) in columns.items():
                tmp2 = {}
                for (value, count) in valueCounts.items():
                    tmp2[value] = count / classes[category]
                tmp[col] = tmp2
                
            # Convert tmp to vector
            tmp3 = []
            for i in range(1, size):
                tmp3.append(tmp[i])
            self.conditional[category] = tmp3
            
    def classify(self, instance):
        """Classify an instance and return its probability."""
        categories = {}
        for (category, vector) in self.conditional.items():
            prob = 1
            for i in range(len(vector)):
                colProbability = .0000001
                if instance[i] in vector[i]:
                    # get the probability for that column value
                    colProbability = vector[i][instance[i]]
                prob = prob * colProbability
            prob = prob * self.prior[category]
            categories[category]  = prob
        cat = list(categories.items())
        cat.sort(key=lambda catTuple: catTuple[1], reverse = True)
        return(cat[0])
