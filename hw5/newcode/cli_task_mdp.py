import sys
import time
import random
import throw
import mdp
import modelbased
import modelfree
import darts 

import unittest
from tfutils import tftask

num_games = 10
#epochs = [25,35,50]
epochs = [25, 35, 10]

class SimpleThrow(tftask.ChartTask):
    def get_name(self):
        return "Darts Warm-Up"
    
    def get_priority(self):
        return 1
    def get_description(self):
        return ("Use your MDP to play games of darts")
    
    def task(self):
        throw.init_board()
        throw.use_simple_thrower()
        y1= darts.test(1, "mdp")
        
        throw.init_board()
        throw.use_simple_thrower()
        y2=darts.test(5, "mdp")         
        
        throw.init_board()
        throw.use_simple_thrower()
        y3=darts.test(10, "mdp")        
                        
        listNames = ["1 game", "5 games", "10 games"]
        listData = [y1, y2, y3]
        chart = {"chart": {"defaultSeriesType": "column"},
                 "xAxis": {"categories": listNames},
                 "yAxis": {"title": {"text": "#Throws"}},
                 "title": {"text": "Average #throws to finish vs. #games"}, 
                 "series": [ {"name": "Average policy performance", 
                                    "data": listData} ] }
        return chart

def mb(strategy):
    print "strategy, epochs, num_games, result"
    throw.NUM_WEDGES = 8
    throw.wedges = [ 4, 6, 2, 7, 1, 8, 3, 5 ]
    throw.START_SCORE = 100
    throw.init_board()
    random.seed()
    throw.init_thrower()
    listNames = map(lambda x: "Epoch "+`x`, epochs);
    y = []
    #y= map(lambda x: modelbased.modelbased(darts.GAMMA, x, num_games,2), epochs);
    for e in epochs:
        yp = modelbased.modelbased(darts.GAMMA, e, num_games,strategy);
        print "%1d  %2d  %2d  %2d" % (strategy, e, num_games, yp)
        y.append(yp)
    listData = y
    return y, epochs

class QLearning(tftask.ChartTask):
    def get_name(self):
        return "Q-Learning"
    
    def get_priority(self):
        return 4
    def get_description(self):
        return ("Strategies 1 & 2")
    
    def task(self):
        throw.NUM_WEDGES = 8
        throw.wedges = [ 4, 6, 2, 7, 1, 8, 3, 5 ]
        throw.START_SCORE = 100
        throw.init_board()
        random.seed()
        throw.init_thrower()
        
         
        num_games=10
        modelfree.ACTIVE_STRATEGY = 1;  
        y1=  darts.test(num_games, "modelfree")
        modelfree.ACTIVE_STRATEGY = 2;  
        y2=  darts.test(num_games, "modelfree")
        listNames = ["Strategy 1","Strategy 2"]
        y= [y1, y2]
        listData = y
        
        chart = {"chart": {"defaultSeriesType": "line"},
                 "xAxis": {"categories": listNames},
                 "yAxis": {"title": {"text": "#Throws"}},
                 "title": {"text": "Average #throws to finish vs. #games"}, 
                 "series": [ {"name": "Average policy performance", 
                              "data": listData} ] }
        return chart


def main(argv):
    mb(2)
    exit()

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))

