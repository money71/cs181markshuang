#! /usr/bin/python
# driver.py

# imports
from __future__ import division
from optparse import OptionParser
import sys
import os

from util import *
from dataset import DataSet
from hmm import *
from classify import *

import sys

def main(argv=None):
    if argv is None:
        argv = sys.argv

    usage = "usage: %prog [options] N datafile (pass -h for more info)"
    parser = OptionParser(usage)
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="Print extra debugging info")

    (options, args) = parser.parse_args(argv[1:])
    if len(args) != 2:
        print "ERROR: Missing arguments"
        parser.print_usage()
        sys.exit(1)
        
    num_states = int(args[0])
    filename = args[1]
    filename = normalize_filename(filename)
    dataset = DataSet(filename)
    category_seqs = split_into_categories(dataset)
    boston_seqs = category_seqs["boston"]
    
    model = HMM(range(num_states), dataset.outputs)
    ll = model.learn_from_observations(boston_seqs, False, True)
    
    print "Number of hidden states: ", num_states
    print "Log Likelihood: ", (ll[-1])
    
    return 0

if __name__ == "__main__":
    sys.exit(main())