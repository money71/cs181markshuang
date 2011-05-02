#!/usr/bin/python

import common
import game_interface

import sys
from os.path import abspath, dirname 
path = dirname(abspath(__file__))
sys.path.append(path)

import classify
from math import *
from svmutil import *
from dtreeutil import *
from annutil import *
from nbayesutil import *

R_VIS = -.5
R_UNVIS = 1.0
R_NEIGHBOR_BONUS = .7

VI_H = 10
VI_EXPLORE_WINDOW = 3
VI_NEIGHBOR_WINDOW = 2

P_LEFT = .15
P_RIGHT = .15
P_FORWARD = .7

mSVM = None
mDT = None
mANN = None
mNBayes = None

def dist_penalty(x, y):
  d = sqrt(x*x + y*y)
  return -.005 * pow(d, 1.4) 
  return 0


def find_L(x, y, move):
  return find_dest(x, y, (move+1)%4)

def find_R(x, y, move):
  return find_dest(x, y, (move+3)%4)

def find_dest(x, y, move):
  if move == game_interface.RIGHT:
    return x+1, y
  if move == game_interface.DOWN:
    return x, y-1
  if move == game_interface.LEFT:
    return x-1, y
  if move == game_interface.UP:
    return x, y+1

class MoveGenerator():
  '''You can keep track of state by updating variables in the MoveGenerator
  class.'''
  def __init__(self):
    self.visited = {}     #0 signifies visited and empty
                        #1 signifies visited and unknown plant
                        #2 signifies visited and nutritious
                        #3 signifies visited and poisonous
    #self.Q = {}
    self.PI = {}
    self.R_arr = [[1 for i in range(100)] for j in range(100)]
    self.calls = 0
    self.destX = 0
    self.destY = 0
    self.lastX = 0
    self.lastY = 0
    self.lastNutriX = 0
    self.lastNutriY = 0
    self.lastNutri = -20
    self.centerX = 0
    self.centerY = 0
    self.lastLife = 0
    self.lastPlant = game_interface.STATUS_NO_PLANT
    self.lastImg = []
    self.fdebug = open("p1.out","w")
    self.fmap = open("p1_map.out","w")
    self.fnutri = open("p1_nutri.out","a")
    self.fpois = open("p1_pois.out","a")

  def next_move_spiral(self, x, y, x0, y0):
    x = x-x0
    y = y-y0
    if y > x and y > (x*-1):
      return game_interface.RIGHT
    if y <= x and y > (x*-1):
      return game_interface.DOWN
    if y < x and y <= (x*-1):
      return game_interface.LEFT
    if y >= x and y <= (x*-1):
      return game_interface.UP
    return common.get_move(view)


  def point_towards_center(self, xi, yi, x0, y0):
    x = xi-x0
    y = yi-y0
    if y > x and y > (x*-1):
      return xi, yi-1
    if y <= x and y > (x*-1):
      return xi-1, yi
    if y < x and y <= (x*-1):
      return xi, yi+1
    if y >= x and y <= (x*-1):
      return xi+1, yi

  def direction_towards_center(self, xi, yi, x0, y0):
    x = xi-x0
    y = yi-y0
    if y > x and y > (x*-1):
      return game_interface.DOWN
    if y <= x and y > (x*-1):
      return game_interface.LEFT
    if y < x and y <= (x*-1):
      return game_interface.UP
    if y >= x and y <= (x*-1):
      return game_interface.RIGHT

  def point_away_center(self, xi, yi, x0, y0):
    x = xi-x0
    y = yi-y0
    if y > x and y > (x*-1):
      return xi, yi+1
    if y <= x and y > (x*-1):
      return xi+1, yi
    if y < x and y <= (x*-1):
      return xi, yi-1
    if y >= x and y <= (x*-1):
      return xi-1, yi

  def direction_away_center(self, xi, yi, x0, y0):
    x = xi-x0
    y = yi-y0
    if y > x and y > (x*-1):
      return game_interface.UP
    if y <= x and y > (x*-1):
      return game_interface.RIGHT
    if y < x and y <= (x*-1):
      return game_interface.DOWN
    if y >= x and y <= (x*-1):
      return game_interface.LEFT
    return 0

  def point_perp_center(self, xi, yi, x0, y0):
    x = xi-x0
    y = yi-y0
    if y > x and y > (x*-1):
      return xi+1, yi
    if y <= x and y > (x*-1):
      return xi, yi-1
    if y < x and y <= (x*-1):
      return xi-1, yi
    if y >= x and y <= (x*-1):
      return xi, yi+1

  def direction_perp_center(self, xi, yi, x0, y0):
    x = xi-x0
    y = yi-y0
    if y > x and y > (x*-1):
      return game_interface.RIGHT
    if y <= x and y > (x*-1):
      return game_interface.DOWN
    if y < x and y <= (x*-1):
      return game_interface.LEFT
    if y >= x and y <= (x*-1):
      return game_interface.UP

  def next_move_spiral_smart(self, xi, yi, x0, y0):
    x_perp, y_perp = self.point_perp_center(xi, yi, x0, y0)
    x_perp2, y_perp2 = self.point_perp_center(x_perp, y_perp, x0, y0)
    x_perp_tow, y_perp_tow = self.point_towards_center(x_perp, y_perp, x0, y0)
    x_tow, y_tow = self.point_towards_center(xi, yi, x0, y0)
    x_tow2, y_tow2 = self.point_towards_center(x_tow, y_tow, x0, y0)

    # don't correct anything on corners. for now.
    if self.direction_perp_center(xi, yi, x0, y0) == \
                      self.direction_perp_center(x_perp, y_perp, x0, y0):
      if (x_perp, y_perp) in self.visited and self.visited[(x_perp, y_perp)] != 2:
        return self.direction_away_center(xi, xi, x0, y0)

      #if (not (x_tow,y_tow) in self.visited) and (not (x_tow2, y_tow2) in self.visited):
      #  return self.direction_towards_center(xi, yi, x0, y0)

    #if the square inwards of us and the square inwards of the square ahead
    # have both been visited, move out one ring
    #  the first condition is to ignore corners, because they fuck everything up
    #elif self.direction_perp_center(xi, yi, x0, y0) == \
    #                  self.direction_perp_center(x_perp, y_perp, x0, y0) \
    #        and (x_tow, y_tow) in self.visited \
    #        and (x_perp_tow, y_perp_tow) in self.visited:
    #  return self.direction_away_center(xi, xi, x0, y0)

    return self.direction_perp_center(xi, yi, x0, y0)
      
  def log_move(self, view, move, eat):
    x = view.GetXPos()
    y = view.GetYPos()
    self.fdebug.write("(%d, %d)" % (x , y))
    self.fdebug.write(" %d" % view.GetPlantInfo())
    if move == game_interface.RIGHT:
      self.destY = y
      self.destX = x + 1
      self.fdebug.write(" >")
    if move == game_interface.DOWN:
      self.destY = y -1
      self.destX = x
      self.fdebug.write(" v")
    if move == game_interface.LEFT:
      self.destY = y
      self.destX = x - 1
      self.fdebug.write(" <")
    if move == game_interface.UP:
      self.destY = y + 1
      self.destX = x
      self.fdebug.write(" ^")
    if eat:
      self.fdebug.write(" E")
    self.fdebug.write("\n")
    #self.fdebug.flush()

  #nonzero neighbors of x,y get bonus of +1
  def update_neighbor_weights(self, x, y):
    if self.R(x+1, y) != 0:
      self.set_R(x+1, y, self.R(x+1, y) + 5)
    if self.R(-+1, y) != 0:
      self.set_R(x-1, y, self.R(x-1, y) + 5)
    if self.R(x, y+1) != 0:
      self.set_R(x, y+1, self.R(x, y+1) + 5)
    if self.R(x, y-1) != 0:
      self.set_R(x, y-1, self.R(x, y-1) + 5)
    

  #also update R for neighbors of plant
#return 2 for nutri, 3 for pois, 0 for no plant, 1 for eaten plant
  def log_last_plant(self, view):
    if self.lastPlant == game_interface.STATUS_NO_PLANT:
      self.centerX = self.lastNutriX
      self.centerY = self.lastNutriY
      mapstr = "%d %d 1\n" % (self.lastX, self.lastY)
      self.fmap.write(mapstr)
      return 0
      #self.fmap.flush()
    if self.lastPlant == game_interface.STATUS_UNKNOWN_PLANT:
      nutri = self.lastLife < view.GetLife()
      if nutri:
        mapstr = "%d %d 2\n" % (self.lastX, self.lastY)
        self.lastNutriX = self.lastX
        self.lastNutriY = self.lastY
        self.fmap.write(mapstr)
        return 2
        #self.visited[(self.lastX, self.lastY)] = 2
        #self.update_neighbor_weights(self.lastX, self.lastY)
      else:
        mapstr = "%d %d 3\n" % (self.lastX, self.lastY)
        self.fmap.write(mapstr)
        return 3
        #self.visited[(self.lastX, self.lastY)] = 3
      #self.fmap.flush()
    return 1

  def log_dup_move(self,view):
    if (view.GetXPos(), view.GetYPos()) in self.visited:
      self.fdebug.write("1\n")
    else:
      self.fdebug.write("0\n")

  def log_last_move(self,view):
    if view.GetXPos() != self.destX or view.GetYPos() != self.destY:
      self.fdebug.write("1\n")
    else:
      self.fdebug.write("0\n")

  def set_R(self, xi, yi, v):
    self.R_arr[xi+50][yi+50] = v
    return

  def get_num_nutri_neighbors(self, xi, yi, window=1, includeDiag = True, includeSelf = True):
    r=0
    for neighbor in self.get_neighbors((xi, yi), window, includeDiag, includeSelf):
      if neighbor in self.visited and self.visited[neighbor] == 2:
        r+=1
    return r

  def get_num_pois_neighbors(self, xi, yi, window=1, includeDiag = True, includeSelf = True):
    r=0
    for neighbor in self.get_neighbors((xi, yi), window, includeDiag, includeSelf):
      if neighbor in self.visited and self.visited[neighbor] == 3:
        r+=1
    return r
  
  def get_num_vis_neighbors(self, xi, yi, window=1, includeDiag = True, includeSelf = True):
    r=0
    for neighbor in self.get_neighbors((xi, yi), window, includeDiag, includeSelf):
      if neighbor in self.visited:
        r+=1
    return r

  def R(self,xi, yi):
    # if we already visited it, penalize
    if (xi, yi) in self.visited:
      r = R_VIS
    else:
      r = R_UNVIS
      r += R_NEIGHBOR_BONUS * self.get_num_nutri_neighbors(xi, yi, VI_NEIGHBOR_WINDOW, True, True)
      r += dist_penalty(xi, yi)
    return r

  def get_neighbors(self,center,window, includeDiag = True, includeSelf = False):
    x, y = center
    neighbors = []
    for xi in range(x - window, x + window + 1):
      for yi in range(y - window, y + window + 1):
        if      (includeSelf or ((xi!=x) and (yi!=y))) \
            and (includeDiag or (abs(x-xi) + abs(y-yi)) <= window):
          neighbors.append((xi, yi))
    return neighbors

  def VI(self, center, steps=VI_H, window=VI_EXPLORE_WINDOW):
    V = {}
    Q = {}
    PI = {}
    
    states = self.get_neighbors(center, window + 1, True, True)
    states_window = self.get_neighbors(center, window)
    actions = (game_interface.UP, game_interface.LEFT, 
               game_interface.RIGHT, game_interface.DOWN)

    # intialize value of each state to 0
    for k in range(steps+1):
      PI[k] = {}
      V[k] = {}
      Q[k] = {}
      for s in states:
        PI[k][s] = -1
        V[k][s] = 0.0
        Q[k][s] = {}

    for k in range(1,steps+1):
      # update Q, pi, and V
      for s in states_window:
        for a in actions:
          summand= P_LEFT    * V[k-1][find_L(s[0], s[1], a)] + \
                   P_FORWARD * V[k-1][find_dest(s[0], s[1], a)] + \
                   P_RIGHT   * V[k-1][find_R(s[0], s[1], a)]

          # update Q
          Q[k][s][a] = self.R(s[0],s[1]) + summand

        # given current state, store the action that maximizes V in pi and the corresponding value in V
        PI[k][s] = actions[0]
        for a in actions:
          if V[k][s] <= Q[k][s][a]:
            V[k][s] = Q[k][s][a]
            PI[k][s] = a
    return PI[steps], Q[steps][center]
    

  def EMax_rec(self, state, H):
    x = state[0]
    y = state[1]
    if H == 0:
      return self.R(x, y)

    actions = (game_interface.UP, game_interface.LEFT, 
               game_interface.RIGHT, game_interface.DOWN)
    #notConverged = True
    # intialize value of each state to 0
    #for s in states:
    #  V[s] = 0
    #  Q[s] = {}

    #for i in range(H):
      # store values from previous iteration
    #  for s in states:
    #    V_prime[s] = V[s]
      # update Q, pi, and V
    #  for s in states:
    maxVal = -1000
    maxAction = 0
    for a in actions:
      sum = P_LEFT    * self.EMax_rec(find_L(x, y, a), H-1) + \
            P_FORWARD * self.EMax_rec(find_dest(x, y, a), H-1) + \
            P_RIGHT   * self.EMax_rec(find_R(x, y, a), H-1)
      if sum > maxVal:
        maxVal = sum
        maxAction = a
    self.PI[state] = maxAction
    return self.R(x,y) + maxVal
    

  def get_move(self, view):
    self.calls += 1
    last_plant = self.log_last_plant(view)
#return value of 1 signals plant we've seen before, so don't log it
    if last_plant == 2 or last_plant==3:
      self.visited[(self.lastX, self.lastY)] = last_plant

    if last_plant == 2:
      self.lastNutri = self.calls - 1
        
    self.log_dup_move(view)

    x = view.GetXPos()
    y = view.GetYPos()

    #self.set_R(x,y,0)

    #move = self.next_move_spiral_smart(x, y, self.centerX, self.centerY)
    #self.EMax_rec((x,y), 5)
    #move = self.PI[(x,y)]
    #move = game_interface.UP
    #self.destX = x
    #self.destY = y+1

    self.lastPlant = view.GetPlantInfo()
    self.visited[(x, y)] = view.GetPlantInfo()

    if self.calls < 15 or (self.lastNutriX==0 and self.lastNutriY ==0):
      move = self.next_move_spiral_smart(x, y, self.centerX, self.centerY)
    else:
      if self.lastNutri + 5 > self.calls:
        PI, Q = self.VI((x,y))
        #PI, Q = self.VI((self.lastNutriX,self.lastNutriY))
      else:
        PI, Q = self.VI((x,y))
      move = PI[(x, y)]


    self.lastX = view.GetXPos()
    self.lastY = view.GetYPos()
    
    if view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT:
        self.lastImg = list(view.GetImage())
        data = self.lastImg
        data.append(self.lastX)
        data.append(self.lastY)
        data.append(self.get_num_nutri_neighbors(self.lastX, self.lastY))
        data.append(self.get_num_pois_neighbors(self.lastX, self.lastY))
        data.append(self.get_num_vis_neighbors(self.lastX, self.lastY))
        
        print data

        #self.log_move(view, move, True)
        return (move, classify.get_class(data, self.mSVM, self.mDT, self.mANN, self.mNBayes))
        #return common.get_move(view)
    
    return (move, False)

  def init_point_settings(self, plant_bonus, plant_penalty, observation_cost,
                          starting_life, life_per_turn):
    self.plant_bonus = plant_bonus
    self.plant_penalty = plant_penalty
    self.observation_cost = observation_cost
    self.starting_life = starting_life
    self.life_per_turn = life_per_turn
    self.lastLife = starting_life
  
  def init_models(self, mSVM, mDT, mANN, mNBayes):
    self.mSVM = mSVM
    self.mDT = mDT
    self.mANN = mANN
    self.mNBayes = mNBayes

move_generator = MoveGenerator()

def get_move(view):
  '''Returns a (move, bool) pair which specifies which move to take and whether
  or not the agent should try and eat the plant in the current square.  view is
  an object whose interface is defined in python_game.h.  In particular, you can
  ask the view for observations of the image at the current location.  Each
  observation comes with an observation cost.
  '''
  return move_generator.get_move(view)

def init_point_settings(plant_bonus, plant_penalty, observation_cost,
                        starting_life, life_per_turn):
  '''Called before any moves are made.  Allows you to make customizations based
  on the specific scoring parameters in the game.'''
  
  mSVM = svm_load_model(path+'/svm.model')
  mDT = dt_load_model(path+'/dt.model')
  mANN = ann_load_model(path+'/ann.model')
  mNBayes = nbayes_load_model(path+'/nbayes.model')
  move_generator.init_models(mSVM, mDT, mANN, mNBayes)
  move_generator.init_point_settings(plant_bonus, plant_penalty, observation_cost, starting_life, life_per_turn)
