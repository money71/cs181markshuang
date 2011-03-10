#!/usr/bin/env python

import random
import math

def dist(v1, v2):
    """Returns the Euclidean distance between instance 1 and instance 2."""
    ret = 0
    for v1i,v2i in zip(v1,v2):
        ret += (v2i-v1i)**2
    return math.sqrt(ret)

def is_closest(vx, i_u, u):
    """
    determines whether u[i_u] is the closest of all u[*] to vector vx
    returns 1 if true, 0 if false
    """
    dists = [dist(vx,vu) for vu in u]
    minind = dists.index(min(dists))
    #print i_u, minind
    if minind == i_u:
        return 1.0
    return 0.0

def err2(u,r,dataset):
    e = 0
    for i in range(len(dataset)):
        for k in range(len(u)):
            e += (dist(dataset[i],u[k])**2.0) * r[k][i]
            #print "  i,k,err,",i,k,e
    return e


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
    if initial_means==None:
      initial_means = random.sample(range(len(dataset)), num_clusters)
    u = [dataset[i] for i in initial_means]
    r = [map(lambda vx: is_closest(vx, i_u, u), dataset) for i_u in range(num_clusters)]

    e1 = err2(u,r,dataset)
    e0 = e1 + 1
    while e0 != e1:
        print "last error",e0,"this error",e1
        r = [map(lambda vx: is_closest(vx, i_u, u), dataset) for i_u in range(num_clusters)]
        for k in range(len(u)):
            n_closest = sum(r[k])
            new_u_total = [0 for x in u[k]]
            for dim in range(len(u[k])):
                listForDim =  [dataset[i][dim] * r[k][i] for i in range(len(dataset))]
                new_u_total[dim] = sum(listForDim)
            new_u = [ui/n_closest for ui in new_u_total]
            u[k] = new_u
        e0 = e1
        e1 = err2(u,r,dataset)
    return u, e1/len(dataset)
    return


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

def eval_min(c1, c2, dataset):
    d = -1
    for cii in range(len(c1)):
        for cjj in range(len(c2)):
            dp =  dist(dataset[c1[cii]], dataset[c2[cjj]])
            if d==-1 or dp < d:
                d = dp
    return d

def eval_centroid(c1, c2, dataset):
    c1p = [0 for i in c1]
    c2p = [0 for i in c2]
    for cii in range(len(c1)):
        c1p = map(lambda i: c1p[i] + c1[i], range(len(c1p)))
    c1p = map(lambda v: v/len(c1p), c1p)
    for cjj in range(len(c2)):
        c2p = map(lambda i: c2p[i] + c2[i], range(len(c2p)))
    c2p = map(lambda v: v/len(c2p), c2p)
    return dist(c1p,c2p)

def eval_mean(c1, c2, dataset):
    d = 0
    for cii in range(len(c1)):
        for cjj in range(len(c2)):
            dp =  dist(dataset[c1[cii]], dataset[c2[cjj]])
            d += dp
    return d / len(c1)*len(c2)

def eval_max(c1, c2, dataset):
    d = -1
    for cii in range(len(c1)):
        for cjj in range(len(c2)):
            dp =  dist(dataset[c1[cii]], dataset[c2[cjj]])
            if d==-1 or dp > d:
                d = dp
    return d

def closest_two(clusters, dataset, ev):
    c1 = 0
    c2 = 1
    i1 = 0
    i2 = 0
    d = dist(dataset[clusters[c1][i1]], dataset[clusters[c2][i2]])
    for ci in range(len(clusters)):
        for cj in range(len(clusters)):
            if ci!=cj:
                dp = ev(clusters[ci],clusters[cj],dataset)
                if dp < d:
                    c1 = ci
                    c2 = cj
                    d = dp
    return c1, c2


def min_hac(dataset, num_clusters):
    """Runs the min hac algorithm in dataset.  Returns a list of the clusters
  formed.
  """
    clusters = [[i] for i in range(len(dataset))]
    while len(clusters) != num_clusters:
        i1, i2 = closest_two(clusters, dataset,eval_min)
        c1 = clusters[i1]
        c2 = clusters[i2]
        clusters.remove(c1)
        clusters.remove(c2)
        c1.extend(c2)
        clusters.append(c1)
        #print "NEW CLUSTER INDS: ",clusters
        #print
    return clusters

def max_hac(dataset, num_clusters):
    """Runs the max hac algorithm in dataset.  Returns a list of the clusters
  formed.
  """
    clusters = [[i] for i in range(len(dataset))]
    while len(clusters) != num_clusters:
        i1, i2 = closest_two(clusters, dataset,eval_max)
        c1 = clusters[i1]
        c2 = clusters[i2]
        clusters.remove(c1)
        clusters.remove(c2)
        c1.extend(c2)
        clusters.append(c1)
        #print "NEW CLUSTER INDS: ",clusters
        #print
    return clusters

def mean_hac(dataset, num_clusters):
    """Runs the mean hac algorithm in dataset.  Returns a list of the clusters
  formed.
  """
    clusters = [[i] for i in range(len(dataset))]
    while len(clusters) != num_clusters:
        i1, i2 = closest_two(clusters, dataset,eval_mean)
        c1 = clusters[i1]
        c2 = clusters[i2]
        clusters.remove(c1)
        clusters.remove(c2)
        c1.extend(c2)
        clusters.append(c1)
        #print "NEW CLUSTER INDS: ",clusters
        #print
    return clusters

def centroid_hac(dataset, num_clusters):
    """Runs the centroid hac algorithm in dataset.  Returns a list of the clusters
  formed.
  """
    clusters = [[i] for i in range(len(dataset))]
    while len(clusters) != num_clusters:
        i1, i2 = closest_two(clusters, dataset,eval_centroid)
        c1 = clusters[i1]
        c2 = clusters[i2]
        clusters.remove(c1)
        clusters.remove(c2)
        c1.extend(c2)
        clusters.append(c1)
        #print "NEW CLUSTER INDS: ",clusters
        #print
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
