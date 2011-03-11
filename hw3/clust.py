#!/usr/bin/env python

import random
from math import sqrt
from itertools import izip
from itertools import combinations

def dist(v1, v2):
    """Returns the Euclidean distance between instance 1 and instance 2."""
    return sqrt(sum([(v1_j-v2_j)**2 for v1_j,v2_j in izip(v1,v2)]))

def kmeans(dataset, num_clusters, initial_means=None):
    """Runs the kmeans algorithm.

    dataset: A list of instances.
    num_clusters: The number of clusters to maintain.
    initial_means: (optional) If specified, gives the indices of the data points
        which will be the initial centers of each cluster.  Must have length
        num_clusters if specified.  If not specified, then kmeans should randomly
        initial the means to random data points.

    Returns (means, error), where means is the list of mean vectors, and error is
    the mean distance from a datapoint to its cluster.
    """
    num_in = len(dataset)
    if not initial_means:
        initial_means = random.sample(xrange(num_in), num_clusters)
    u = [dataset[i] for i in initial_means]
    r = [0]*num_in
    while 1:
        diff = False
        for i, x_i in enumerate(dataset):
            dists_i = [dist(x_i,u_k) for u_k in u]
            r_i = dists_i.index(min(dists_i))
            if r[i] != r_i:
                r[i] = r_i
                diff = True
        if not diff:
            break
        for k in xrange(num_clusters):
            cluster = [dataset[i] for i in xrange(num_in) if r[i] == k]
            size = len(cluster)
            u[k] = [sum(x)/(1.0*size) for x in izip(*cluster)]
    e = sum([dist(dataset[i],u[k])**2 for i in xrange(num_in)
                                      for k in xrange(num_clusters)
                                      if r[i] == k]) / num_in
    return u, e

def parse_input(datafile, num_examples):
    data = []
    ct = 0
    for line in datafile:
        instance = line.split(",")
        instance = instance[:-1]
        data.append(map(lambda x:float(x),instance))
        ct += 1
        if not num_examples is None and ct >= num_examples:
          break
    return data

def merge_closest(clusters, dataset, d_fn):
    cmin1 = []
    cmin2 = []
    dmin = float('Inf')
    for c1,c2 in combinations(clusters, 2):
        d = d_fn(c1, c2, dataset)
        if d <= dmin:
            dmin = d
            cmin1 = c1
            cmin2 = c2
    clusters[clusters.index(cmin1)].extend(cmin2)
    clusters.remove(cmin2)
    
def min_fn(c1, c2, dataset):
    return min([dist(dataset[x],dataset[y]) for x in c1 for y in c2])

def max_fn(c1, c2, dataset):
    return max([dist(dataset[x],dataset[y]) for x in c1 for y in c2])

def mean_fn(c1, c2, dataset):
    return sum([dist(dataset[x],dataset[y]) for x in c1 for y in c2]) / (1.0*len(c1)*len(c2))

def centroid_fn(c1, c2, dataset):
    return dist([sum(a)/(1.0*len(c1)) for a in izip(*[dataset[x] for x in c1])],
                [sum(b)/(1.0*len(c2)) for b in izip(*[dataset[y] for y in c1])])

def min_hac(dataset, num_clusters):
    """Runs the min hac algorithm in dataset.  Returns a list of the clusters
  formed.
  """
    clusters = [[i] for i in xrange(len(dataset))]
    while len(clusters) != num_clusters:
        cmin1 = []
        cmin2 = []
        dmin = float('Inf')
        for c1,c2 in combinations(clusters, 2):
            d = min_fn(c1, c2, dataset)
            if d <= dmin:
                dmin = d
                cmin1 = c1
                cmin2 = c2
        clusters[clusters.index(cmin1)].extend(cmin2)
        clusters.remove(cmin2)
    return clusters

def max_hac(dataset, num_clusters):
    """Runs the max hac algorithm in dataset.  Returns a list of the clusters
  formed.
  """
    clusters = [[i] for i in xrange(len(dataset))]
    while len(clusters) != num_clusters:
        cmin1 = []
        cmin2 = []
        dmin = float('Inf')
        for c1,c2 in combinations(clusters, 2):
            d = max_fn(c1, c2, dataset)
            if d <= dmin:
                dmin = d
                cmin1 = c1
                cmin2 = c2
        clusters[clusters.index(cmin1)].extend(cmin2)
        clusters.remove(cmin2)
    return clusters

def mean_hac(dataset, num_clusters):
    """Runs the mean hac algorithm in dataset.  Returns a list of the clusters
  formed.
  """
    clusters = [[i] for i in xrange(len(dataset))]
    while len(clusters) != num_clusters:
        cmin1 = []
        cmin2 = []
        dmin = float('Inf')
        for c1,c2 in combinations(clusters, 2):
            d = mean_fn(c1, c2, dataset)
            if d <= dmin:
                dmin = d
                cmin1 = c1
                cmin2 = c2
        clusters[clusters.index(cmin1)].extend(cmin2)
        clusters.remove(cmin2)
    return clusters

def centroid_hac(dataset, num_clusters):
    """Runs the centroid hac algorithm in dataset.  Returns a list of the clusters
  formed.
  """
    clusters = [[i] for i in xrange(len(dataset))]
    while len(clusters) != num_clusters:
        cmin1 = []
        cmin2 = []
        dmin = float('Inf')
        for c1,c2 in combinations(clusters, 2):
            d = centroid_fn(c1, c2, dataset)
            if d <= dmin:
                dmin = d
                cmin1 = c1
                cmin2 = c2
        clusters[clusters.index(cmin1)].extend(cmin2)
        clusters.remove(cmin2)
    return clusters

def main(argv):
    import optparse
    parser = optparse.OptionParser()
    parser.add_option("--num_clusters", action="store", type=int,
                      default=4,
                      dest="num_clusters",help="number of clusters")
    parser.add_option("--num_examples", action="store", type=int,
                      default=1000,
                      dest="num_examples",help="number of examples to read in. defaults to None, which means read in all examples.")
    parser.add_option("--datafile", action="store",
                      default="adults.txt",
                      dest="datafile",help="data file")
    parser.add_option("--random_seed", action="store", type=int,
                      default=None,
                      dest="random_seed",help="the random seed to use")
    parser.add_option("--run_hac", action="store_true",
                      default=False,
                      dest="run_hac",help="if true, then run hac.  otherwise, run kmeans.")
    parser.add_option("--hac_alg", action="store",
                      default="min",
                      dest="hac_alg",
                      help="the hac algorithm to use. { min, max, mean, centroid }")
    opts, args = parser.parse_args(argv)

    if opts.run_hac:
      opts.datafile = "adults-small.txt"
      if opts.hac_alg == 'min' or opts.hac_alg == 'max':
        opts.num_examples = 200
      elif opts.hac_alg == 'mean' or opts.hac_alg == 'centroid':
        opts.num_examples = 200

    #Initialize the data
    dataset = parse_input(open(opts.datafile, "r"), opts.num_examples)
    if opts.num_examples:
      assert len(dataset) == opts.num_examples
    if opts.run_hac:
      if opts.hac_alg == 'min':
        clusters = min_hac(dataset, opts.num_clusters)
      elif opts.hac_alg == 'max': 
        clusters = max_hac(dataset, opts.num_clusters)
      elif opts.hac_alg == 'mean':
        clusters = mean_hac(dataset, opts.num_clusters)
      elif opts.hac_alg == 'centroid':
        clusters = centroid_hac(dataset, opts.num_clusters)
      # Print out the lengths of the different clusters
      # Write the results to files.
      print 'Cluster Lengths:'
      index = 0
      for c in clusters:
        print '%d ' % len(c),
        outfile = open('%s-%d.dat' % (opts.hac_alg, index), 'w')
        for pt in c:
          d = dataset[pt]
          print >> outfile, '%f %f %f' % (d[0], d[1], d[2])
        index += 1
        outfile.close()
      print ''
    else:
      print 'Running K-means for %d clusters' % opts.num_clusters
      (means, error) = kmeans(dataset, opts.num_clusters)
      print 'Total mean squared error: %f' % error



if __name__ == "__main__":
  import sys
  main(sys.argv)
