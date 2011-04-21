import random
import throw
import darts
 
# The default player aims for the maximum score, unless the
# current score is less than the number of wedges, in which
# case it aims for the exact score it needs. 
#  
# You may use the following functions as a basis for 
# implementing the Q learning algorithm or define your own 
# functions.

ACTIVE_STRATEGY=1;

actions = darts.get_actions()
states = darts.get_states()

gamma = .5
learning_rate = .1
num_games = 50000

def start_game():
    num_throws_this = 1
    last_action = throw.location(throw.INNER_RING, throw.NUM_WEDGES)
    return(last_action)

def update_counts(score):
    last_delta = score - last_state
    update_T(last_state, last_action, last_delta)

def get_target(score):
    num_throws_this += 1

    if score <= throw.NUM_WEDGES: return throw.location(throw.SECOND_PATCH, score)
    return(throw.location(throw.INNER_RING, throw.NUM_WEDGES))


# Exploration/exploitation strategy one.
def ex_strategy_one(s,game_no):
  eps = float(throw.START_SCORE - s) / throw.START_SCORE
  if(random.random()<eps):
    return 0
  return 1


# Exploration/exploitation strategy two.
def ex_strategy_two(s,game_no):
  eps = float(num_games - game_no) / num_games
  eps += .1
  if(random.random()<eps):
    return 1
  return 0


# The Q-learning algorithm:
def Q_learning():
    return

def bestAction(Q, s):
    vb = Q[s][0]
    ib = 0
    for i in range(len(Q[s])):
        if Q[s][i] > vb:
            #print i,Q[s][i], "better than",ib,vb 
            vb = Q[s][i]
            ib = i
    return ib

def maxQ(Q, s):
    mq = Q[s][bestAction(Q,s)]
    #print "MaxQ = ", mq
    return mq

def newQ(Q, s, a_i, s_prime, gamma, lr):
    r = s-s_prime
    oldQ = Q[s][a_i]
    deltaQ = (r + gamma*maxQ(Q, s_prime)) - oldQ
    newQ = oldQ + lr * deltaQ
    #print "s=",s,"a=",a_i,"sp=",s_prime,"oldQ=",oldQ,"deltaQ=",deltaQ,"newQ=",newQ
    return newQ





# Implement a model-based reinforcement learning algorithm. 
# Given num_games (the number of games to play), store the
# learned transition probabilities in T.
def modelfree(gamma, learning_rate, num_games, strategy_idx):
    actions = darts.get_actions()
    states = darts.get_states()

    pi_star = {}
    g = 0
    num_actions = {}
    num_transitions = {}
    T_matrix = {}
    Q = {}
    num_iterations = 0
    
    
    # Initialize all arrays to 0 except the policy, which should be assigned a random action for each state.
    for s in states:
        pi_star[s] = random.randint(0, len(actions)-1)
        num_actions[s] = {}
        Q[s] = {}
        num_transitions[s] = {}
        T_matrix[s] = {}
        
        for a in range(len(actions)):
            Q[s][a] = 1.0
            num_actions[s][a] = 0

        for s_prime in states:
            num_transitions[s][s_prime] = {}
            T_matrix[s][s_prime] = {}
            for a in range(len(actions)):
                num_transitions[s][s_prime][a] = 0
                T_matrix[s][s_prime][a] = 0


    # play num_games games, updating policy after every EPOCH_SIZE number of throws
    for g in range(1, num_games + 1):
    
        # run a single game
        s = throw.START_SCORE
        throws = 0
        explores = 0
        exploits = 0
        while s > 0:

            num_iterations += 1
            throws += 1
                
            # The following two statements implement two exploration-exploitation
            # strategies. Comment out the strategy that you wish not to use.
                        
            if(strategy_idx==1):
                to_explore = ex_strategy_one(s,g)
            else:
                to_explore = ex_strategy_two(s,g)
                
            if to_explore:
                # explore
                a = random.randint(0, len(actions)-1)
                action = actions[a]
                explores += 1
            else:
                # exploit
                a = bestAction(Q, s)
                action = actions[a]
                exploits += 1
    
            
            #print "a", a, "action",action
            # Get result of throw from dart thrower; update score if necessary
            loc = throw.throw(action) 
            delta =  throw.location_to_score(loc)
            s_prime = s - delta
            if s_prime < 0:
                s_prime = s

                
            # Update experience:
            # increment number of times this action was taken in this state;
            # increment number of times we moved from this state to next state on this action.

            num_actions[s][a] += 1
            num_transitions[s][s_prime][a] += 1

            this_lr = 1 / num_actions[s][a]
            Q[s][a] = newQ(Q, s, a, s_prime, gamma, this_lr)

            # Next state becomes current state 
            s = s_prime

            # Update our learned MDP and optimal policy after every EPOCH_SIZE throws, 
            # using infinite-horizon value iteration. 
                
        #print "Game",g,"took",throws,"throws (explore ratio %1.4f)" % (float(explores)/(explores+exploits))
        print g,throws,"%1.4f" % (float(explores)/(explores+exploits))
    avg = float(num_iterations)/float(num_games)
    return avg


def mf(strategy):

    #print "strategy, num_games, result"
    throw.NUM_WEDGES = 8
    throw.wedges = [ 4, 6, 2, 7, 1, 8, 3, 5 ]
    throw.START_SCORE = 100
    throw.init_board()
    random.seed()
    throw.init_thrower()
    a = modelfree(gamma, learning_rate, num_games, strategy)
    #print "%1d  %2d  %2d" % (strategy, num_games, a)
    return a

if __name__ == "__main__":
    
    mf(2)

    #a = modelfree(gamma, learning_rate, epoch_size, num_games, strategy_idx)
