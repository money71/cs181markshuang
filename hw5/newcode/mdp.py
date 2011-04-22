

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
  #print throw.location_to_score(a)
  delta = s - s_prime
  p = 0.0
  probs = [.1, .2, .4, .2, .1]
  
  throw.init_board()
  
  if delta > 3*throw.NUM_WEDGES or delta < 0:
    return 0
  
  for ri in range(5):
    for wi in range(5):
      wedge_num = throw.wedges[(throw.angles[a.wedge] - 2 + wi) %
                               throw.NUM_WEDGES]
      ring_num = a.ring - 2 + ri;
      if ring_num > 6:
        ring_num = 6
      if ring_num < 0:
        ring_num = ring_num*(-1)
      
      points = throw.location_to_score(throw.location(ring_num, wedge_num))
      if points == delta:
        p += probs[ri]*probs[wi]
  return p


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
  print PI
  #print Q[0]
  #print Q[1]
  #print Q[2]
  #print Q[3]
  #print Q[4]
  #print Q[5]
  #print Q[6]
  #print Q[7]
  #print Q[8]
  #print Q[9]
        
  
