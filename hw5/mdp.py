

# Components of a darts player. #

# 
 # Modify the following functions to produce a player.
 # The default player aims for the maximum score, unless the
 # current score is less than or equal to the number of wedges, in which
 # case it aims for the exact score it needs.  You can use this
 # player as a baseline for comparison.
 #

from random import *
import throw
import darts

# make pi global so computation need only occur once
PI = {}
EPSILON = .001


# actual
def start_game(gamma):

  infiniteValueIteration(gamma)
  #for ele in PI:
    #print "score: ", ele, "; ring: ", PI[ele].ring, "; wedge: ", PI[ele].wedge
  
  return PI[throw.START_SCORE]

def get_target(score):
  return PI[score]

# define transition matrix/ function
def T(a, s, s_prime):
#CENTER, INNER_RING, FIRST_PATCH, MIDDLE_RING, SECOND_PATCH, OUTER_RING, MISS = range(7)
  print throw.location_to_score(a)
  delta = s - s_prime
  wedge_probs = [.1, .2, .4, .2, .1]
  wedge_nums  = [ ((a.wedge - 2) % throw.NUM_WEDGES),\
                  ((a.wedge - 1) % throw.NUM_WEDGES),\
                  ((a.wedge    ) % throw.NUM_WEDGES),\
                  ((a.wedge + 1) % throw.NUM_WEDGES),\
                  ((a.wedge + 2) % throw.NUM_WEDGES)]
  ring_probs = [.1, .2, .4, .2, .1]
  ring_nums  = [ abs(a.ring - 2), \
                   abs(a.ring - 1), \
                   a.ring, \
                   a.ring + 1, \
                   a.ring + 2]
  scores = [[0 for i in range(5)] for j in range(5)]
  prob = 0.0
  print "target: w=",a.wedge,"r=",a.ring
  print "s=",s,"sp=",s_prime
  print "wedges: ", wedge_nums
  print "rings: ", ring_nums
  
  for w in range(5):
    for r in range(5):
      score = throw.location_to_score(throw.location(ring_nums[r], wedge_nums[w]))
      if score == delta:
        p = wedge_probs[w] * ring_probs[r]
        print prob, " + ", p
        prob += p
  return prob


def infiniteValueIteration(gamma):
  # takes a discount factor gamma and convergence cutoff epislon
  # returns

  V = {}
  Q = {}
  V_prime = {}
  
  states = darts.get_states()
  actions = darts.get_actions()

  notConverged = True

  # intialize value of each state to 0
  for s in states:
    V[s] = 0
    Q[s] = {}

  # until convergence is reached
  while notConverged:

    # store values from previous iteration
    for s in states:
      V_prime[s] = V[s]

    # update Q, pi, and V
    for s in states:
      for a in actions:

        # given current state and action, sum product of T and V over all states
        summand = 0
        for s_prime in states:
          summand += T(a, s, s_prime)*V_prime[s_prime]

        # update Q
        Q[s][a] = darts.R(s, a) + gamma*summand

      # given current state, store the action that maximizes V in pi and the corresponding value in V
      PI[s] = actions[0]
      for a in actions:
        if V[s] <= Q[s][a]:
          V[s] = Q[s][a]
          PI[s] = a

    notConverged = False
    for s in states:
      if abs(V[s] - V_prime[s]) > EPSILON:
        notConverged = True
        
  
