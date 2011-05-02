import common
import game_interface
from math import *

# number of nutri plants that must be observed before distance is weighted
#towards centroid rather than origin
CENTROID_THRESH = 12

P_LEFT = .15
P_RIGHT = .15
P_FORWARD = .7

# format is single line containing 
#"IS_MULTIPLIER UNVIS_MULTIPLIER NEIGHBOR_MULTIPLIER VI_H VI_EXPLORE_WINDOW VI_NEIGHBOR_WINDOW"
#PARAM_FILE = ""
PID = "1"
PARAM_FILE = "p"+PID+".conf"

#TODO: should DECREASE with TIME. Should have some long-term bias towards center?
# SHOULD ADJUST RELATIVE TO FRAME (otherwise dist dwarfs all other weights when far fr origin,
# and is irrelevant when close
def dist_penalty(x, y, steps):
  d = sqrt(x*x + y*y)
  return -.009  * pow(d, 1.3) 
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

def point_towards_center(xi, yi, x0, y0):
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

def direction_towards_center(xi, yi, x0, y0):
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

def point_away_center(xi, yi, x0, y0):
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

def direction_away_center(xi, yi, x0, y0):
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

def point_perp_center(xi, yi, x0, y0):
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

def direction_perp_center(xi, yi, x0, y0):
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


class MoveGenerator():
  '''You can keep track of state by updating variables in the MoveGenerator
  class.'''
  def __init__(self):
    self.visited = {}     #0 signifies visited and empty
                        #1 signifies visited and unknown plant
                        #2 signifies visited and nutritious
                        #3 signifies visited and poisonous
    self.calls = 0
    self.destX = 0
    self.destY = 0
    self.lastX = 0
    self.lastY = 0
    self.lastNutriX = 0
    self.lastNutriY = 0
    self.totalNutriX = 0
    self.totalNutriY = 0
    self.numNutri = 0
    self.centroidX = 0
    self.centroidY = 0
    self.lastNutri = -20
    self.centerX = 0
    self.centerY = 0
    self.lastLife = 0
    self.lastPlant = game_interface.STATUS_NO_PLANT
    self.fdebug = open("p"+PID+".out","w")
    self.fmap = open("p"+PID+"_map.out","w")
    self.fnutri = open("p"+PID+"_nutri.out","a")
    self.fpois = open("p"+PID+"_pois.out","a")

    self.VIS_MULTIPLIER = -.5   # * life_per_turn = R_VIS
    self.UNVIS_MULTIPLIER = .05 # * plant_bonus = R_UNVIS
    self.R_NEIGHBOR_BONUS = .05  # * plant_bonus = R_NEIGHBOR_BONUS
    self.VI_H = 10
    self.VI_EXPLORE_WINDOW = 3
    self.VI_NEIGHBOR_WINDOW = 2

    if PARAM_FILE != "":
      self.read_params()

  def init_point_settings(self, plant_bonus, plant_penalty, observation_cost,
                          starting_life, life_per_turn):
    self.plant_bonus = plant_bonus
    self.plant_penalty = plant_penalty
    self.observation_cost = observation_cost
    self.starting_life = starting_life
    self.life_per_turn = life_per_turn
    self.lastLife = starting_life

    self.R_VIS = self.life_per_turn * self.VIS_MULTIPLIER
    self.R_UNVIS = self.plant_bonus * self.UNVIS_MULTIPLIER
    self.R_NEIGHBOR_BONUS = self.plant_bonus * self.NEIGHBOR_MULTIPLIER
    self.fdebug.write(str(self.R_VIS) + " " + str(self.R_UNVIS))
      
  def read_params(self):
    fparam = open(PARAM_FILE, "r")
    st = fparam.readline()
    params = st.split()
    self.VIS_MULTIPLIER = float(params[0])
    self.UNVIS_MULTIPLIER = float(params[1])
    self.NEIGHBOR_MULTIPLIER = float(params[2])
    self.VI_H = int(params[3])
    self.VI_EXPLORE_WINDOW = int(params[4])
    self.VI_NEIGHBOR_WINDOW = int(params[5])
 

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

  def next_move_spiral_smart(self, xi, yi, x0, y0):
    x_perp, y_perp = point_perp_center(xi, yi, x0, y0)
    x_perp2, y_perp2 = point_perp_center(x_perp, y_perp, x0, y0)
    x_perp_tow, y_perp_tow = point_towards_center(x_perp, y_perp, x0, y0)
    x_tow, y_tow = point_towards_center(xi, yi, x0, y0)
    x_tow2, y_tow2 = point_towards_center(x_tow, y_tow, x0, y0)

    # don't correct anything on corners. for now.
    if direction_perp_center(xi, yi, x0, y0) == \
                      direction_perp_center(x_perp, y_perp, x0, y0):
      if (x_perp, y_perp) in self.visited and self.visited[(x_perp, y_perp)] != 2:
        return direction_away_center(xi, xi, x0, y0)
    #if the square inwards of us and the square inwards of the square ahead
    # have both been visited, move out one ring
    #  the first condition is to ignore corners, because they fuck everything up
    #elif self.direction_perp_center(xi, yi, x0, y0) == \
    #                  self.direction_perp_center(x_perp, y_perp, x0, y0) \
    #        and (x_tow, y_tow) in self.visited \
    #        and (x_perp_tow, y_perp_tow) in self.visited:
    #  return self.direction_away_center(xi, xi, x0, y0)
    return direction_perp_center(xi, yi, x0, y0)
      
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
    self.fdebug.write(" (CENTR: %d %d)"%(self.centroidX, self.centroidY))
    self.fdebug.write("\n")
    #self.fdebug.flush()

#return 2 for nutri, 3 for pois, 0 for no plant, 1 for eaten plant
  def log_last_plant(self, view):
    if self.lastPlant == game_interface.STATUS_NO_PLANT:
      self.centerX = self.lastNutriX
      self.centerY = self.lastNutriY
      mapstr = "%d %d 1\n" % (self.lastX, self.lastY)
      self.fmap.write(mapstr)
      return 0
    if self.lastPlant == game_interface.STATUS_UNKNOWN_PLANT:
      nutri = self.lastLife < view.GetLife()
      if nutri:
        mapstr = "%d %d 2\n" % (self.lastX, self.lastY)
        self.lastNutriX = self.lastX
        self.lastNutriY = self.lastY
        self.totalNutriX += self.lastX
        self.totalNutriY += self.lastY
        self.numNutri += 1
        self.centroidX = self.totalNutriX / self.numNutri
        self.centroidY = self.totalNutriY / self.numNutri
        self.fmap.write(mapstr)
        return 2
      else:
        mapstr = "%d %d 3\n" % (self.lastX, self.lastY)
        self.fmap.write(mapstr)
        return 3
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

  def get_num_empty_neighbors(self, xi, yi, window=1, includeDiag = True, includeSelf = True):
    r=0
    for neighbor in self.get_neighbors((xi, yi), window, includeDiag, includeSelf):
      if not (neighbor in self.visited):
        r+=1
    return r

  def get_neighbors(self,center,window, includeDiag = True, includeSelf = True):
    x, y = center
    neighbors = []
    for xi in range(x - window, x + window + 1):
      for yi in range(y - window, y + window + 1):
        if      (includeSelf or ((xi!=x) or (yi!=y))) \
            and (includeDiag or (abs(x-xi) + abs(y-yi)) <= window):
          neighbors.append((xi, yi))
    return neighbors

  def R(self,xi, yi, current_time, clusterMode):
    # if we already visited it, penalize
    if (xi, yi) in self.visited:
      r = self.R_VIS
    else:
      r = self.R_UNVIS
      r += self.R_NEIGHBOR_BONUS * self.get_num_nutri_neighbors(xi, yi, self.VI_NEIGHBOR_WINDOW, False, False)
      if not clusterMode:
        if self.numNutri > CENTROID_THRESH:
          r += dist_penalty(xi - self.centroidX, yi - self.centroidY, current_time)
        else:
          r += dist_penalty(xi, yi, current_time)
####################################### HACK ALERT ########################################
      else:
        r -= .1 * dist_penalty(xi - self.centroidX, yi - self.centroidY, current_time)
    return r

# NOTE: this is not the best version of VI because it assumes that
# states reached the same way are identical. for our purposes, they aren't..
# the value of a state will change depending on what neighbors are visited.
#cluster mode: when this is TRUE, no distance penalties are assessed
  def VI(self, center, steps, window, current_time, clusterMode = False):
    V = {}
    Q = {}
    PI = {}

    if clusterMode:
      window = window+1/2
    
    states = self.get_neighbors(center, window + 1, True, True)
    states_window = self.get_neighbors(center, window, False, True)
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
          Q[k][s][a] = self.R(s[0],s[1], current_time, clusterMode) + summand

        # given current state, store the action that maximizes V in pi and the corresponding value in V
        PI[k][s] = actions[0]
        for a in actions:
          if V[k][s] <= Q[k][s][a]:
            V[k][s] = Q[k][s][a]
            PI[k][s] = a
    return PI[steps], Q[steps][center]
    
  def get_move(self, view):
    self.calls += 1
    last_plant = self.log_last_plant(view)
#return value of 1 signals plant we've seen before, so don't log it
    if last_plant == 2 or last_plant==3:
      self.visited[(self.lastX, self.lastY)] = last_plant

    if last_plant == 2:
      self.lastNutri = self.calls - 1
        
    x = view.GetXPos()
    y = view.GetYPos()

    self.lastPlant = view.GetPlantInfo()
    self.visited[(x, y)] = view.GetPlantInfo()

    if (self.lastNutriX==0 and self.lastNutriY ==0):
      move = self.next_move_spiral_smart(x, y, self.centerX, self.centerY)
    elif self.lastNutri + self.VI_EXPLORE_WINDOW + 1 > self.calls:
      PI, Q = self.VI((self.lastNutriX,self.lastNutriY), self.VI_H, self.VI_EXPLORE_WINDOW, self.calls, True)
      move = PI[(x, y)]
    else:
      PI, Q = self.VI((x,y), self.VI_H, self.VI_EXPLORE_WINDOW, self.calls, False)
      move = PI[(x, y)]

    self.lastX = view.GetXPos()
    self.lastY = view.GetYPos()
    self.lastLife = view.GetLife()

    self.log_move(view, move, True)
    return (move, True)

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
  move_generator.init_point_settings(plant_bonus, plant_penalty, observation_cost, starting_life, life_per_turn)
