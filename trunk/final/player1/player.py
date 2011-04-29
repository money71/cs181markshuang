import common
import game_interface
from math import *

class MoveGenerator():
  '''You can keep track of state by updating variables in the MoveGenerator
  class.'''
  def __init__(self):
    self.calls = 0
    self.destX = 0
    self.destY = 0
    self.lastX = 0
    self.lastY = 0
    self.lastNutriX = 0
    self.lastNutriY = 0
    self.centerX = 0
    self.centerY = 0
    self.lastim1 = {}
    self.lastim2 = {}
    self.lastim3 = {}
    self.lastim4 = {}
    self.lastim5 = {}
    self.lastim6 = {}
    self.lastim7 = {}
    self.lastim8 = {}
    self.lastim9 = {}
    self.lastim10 = {}
    self.lastim11 = {}
    self.lastim12 = {}
    self.lastim13 = {}
    self.lastim14 = {}
    self.lastim15 = {}
    self.lastim16 = {}
    self.lastim17 = {}
    self.lastim18 = {}
    self.lastim19 = {}
    self.lastim20 = {}
    self.lastLife = 0
    self.lastPlant = game_interface.STATUS_NO_PLANT
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

  def log_last_plant(self, view):
    if self.lastPlant == game_interface.STATUS_NO_PLANT:
      self.centerX = self.lastNutriX
      self.centerY = self.lastNutriY
      mapstr = "%d %d 1\n" % (self.lastX, self.lastY)
      self.fmap.write(mapstr)
      #self.fmap.flush()
    if self.lastPlant == game_interface.STATUS_UNKNOWN_PLANT:
      imstr = " ".join(map(str, self.lastim1)) + "\n" + \
              " ".join(map(str, self.lastim2)) + "\n" + \
              " ".join(map(str, self.lastim3)) + "\n" + \
              " ".join(map(str, self.lastim4)) + "\n" + \
              " ".join(map(str, self.lastim5)) + "\n" + \
              " ".join(map(str, self.lastim6)) + "\n" + \
              " ".join(map(str, self.lastim7)) + "\n" + \
              " ".join(map(str, self.lastim8)) + "\n" + \
              " ".join(map(str, self.lastim9)) + "\n" + \
              " ".join(map(str, self.lastim9)) + "\n" + \
              " ".join(map(str, self.lastim10)) + "\n" + \
              " ".join(map(str, self.lastim11)) + "\n" + \
              " ".join(map(str, self.lastim12)) + "\n" + \
              " ".join(map(str, self.lastim13)) + "\n" + \
              " ".join(map(str, self.lastim14)) + "\n" + \
              " ".join(map(str, self.lastim15)) + "\n" + \
              " ".join(map(str, self.lastim16)) + "\n" + \
              " ".join(map(str, self.lastim17)) + "\n" + \
              " ".join(map(str, self.lastim18)) + "\n" + \
              " ".join(map(str, self.lastim19)) + "\n" + \
              " ".join(map(str, self.lastim20)) + "\n\n"
      nutri = self.lastLife < view.GetLife()
      if nutri:
        self.fnutri.write(imstr)
        #self.fnutri.flush()
        mapstr = "%d %d 2\n" % (self.lastX, self.lastY)
        self.lastNutriX = self.lastX
        self.lastNutriY = self.lastY
      else:
        self.fpois.write(imstr)
        #self.fpois.flush()
        mapstr = "%d %d 3\n" % (self.lastX, self.lastY)
      self.fmap.write(mapstr)
      #self.fmap.flush()
    

  def get_move(self, view):
    self.calls += 1
    self.log_last_plant(view)

    x = view.GetXPos()
    y = view.GetYPos()

    move = self.next_move_spiral(x, y, self.centerX, self.centerY)

    self.lastPlant = view.GetPlantInfo()
    self.lastim1 = view.GetImage()
    self.lastim2 = view.GetImage()
    self.lastim3 = view.GetImage()
    self.lastim4 = view.GetImage()
    self.lastim5 = view.GetImage()
    self.lastim6 = view.GetImage()
    self.lastim7 = view.GetImage()
    self.lastim8 = view.GetImage()
    self.lastim9 = view.GetImage()
    self.lastim10 = view.GetImage()
    self.lastim11 = view.GetImage()
    self.lastim12 = view.GetImage()
    self.lastim13 = view.GetImage()
    self.lastim14 = view.GetImage()
    self.lastim15 = view.GetImage()
    self.lastim16 = view.GetImage()
    self.lastim17 = view.GetImage()
    self.lastim18 = view.GetImage()
    self.lastim19 = view.GetImage()
    self.lastim20 = view.GetImage()
    self.lastLife = view.GetLife()
    self.lastX = view.GetXPos()
    self.lastY = view.GetYPos()

    self.log_move(view, move, True)
    return (move, True)
    #return common.get_move(view)

  def init_point_settings(self, plant_bonus, plant_penalty, observation_cost,
                          starting_life, life_per_turn):
    self.plant_bonus = plant_bonus
    self.plant_penalty = plant_penalty
    self.observation_cost = observation_cost
    self.starting_life = starting_life
    self.life_per_turn = life_per_turn
    self.lastLife = starting_life

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
