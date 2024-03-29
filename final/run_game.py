import player1.player
import player2.player
import game_interface
import random
import signal
import sys
import time
import traceback
from optparse import OptionParser

class TimeoutException(Exception):
  def __init__(self):
    pass

def get_move(view, cmd, options, player_id):
  def timeout_handler(signum, frame):
    raise TimeoutException()
  signal.signal(signal.SIGALRM, timeout_handler)
  signal.alarm(1)
  try: 
    (mv, eat) = cmd(view)
    # Clear the alarm.
    signal.alarm(0)
  except TimeoutException:
    # Return a random value
    # Should probably log this to the interface
    (mv, eat) = (random.randint(0, 4), False)
    error_str = 'Error in move selection (%d).' % view.GetRound()
    if options.display:
      game_interface.curses_debug(player_id, error_str)
    else:
      print error_str
  return (mv, eat)

def check_if_game_over_single_player(l1, l2, options, game, rounds):
  if options.display:
    game_interface.curses_init_round(game)
  if l1 <= 0:
    debug_str = 'Single player mode: lasted %d rounds' % rounds
    # Need to end the game
    if options.display:
      game_interface.curses_debug(1, debug_str)
    else:
      print debug_str
    sys.stdin.read(1)
    if options.display:
      game_interface.curses_close()
    return True
  return False

def check_if_game_over(l1, l2, options, game, rounds):
  if options.single_player_mode:
    return check_if_game_over_single_player(l1, l2, options, game, rounds)
  if l1 > 0 and l2 > 0:
    return False
  if options.display:
    game_interface.curses_init_round(game)
    winner = 0
    if l1 < l2:
      winner = 2
    elif l1 > l2:
      winner = 1
    game_interface.curses_declare_winner(winner)
  else:
    if l1 == l2:
      print 'Tie, remaining life: %d v. %d' % (l1, l2)
    elif l1 < l2:
      print 'Player 2 wins: %d v. %d' % (l1, l2)
    else:
      print 'Player 1 wins: %d v. %d' % (l1, l2)
  # Wait for input
  sys.stdin.read(1)
  if options.display:
    game_interface.curses_close()
  return True

def run(options):
  game = game_interface.GameInterface(options.plant_bonus,
                                      options.plant_penalty,
                                      options.observation_cost,
                                      options.starting_life,
                                      options.life_per_turn)
  # Give the players a chance to customize according to the parameters of the
  # game.
  player1.player.init_point_settings(options.plant_bonus, options.plant_penalty,
                                     options.observation_cost, options.starting_life,
                                     options.life_per_turn)
  player2.player.init_point_settings(options.plant_bonus, options.plant_penalty,
                                     options.observation_cost, options.starting_life,
                                     options.life_per_turn)
  player1_view = game.GetPlayer1View()
  player2_view = game.GetPlayer2View()

  if options.display:
    if game_interface.curses_init() < 0:
      return
    game_interface.curses_draw_board(game)
  
  # Keep running until one player runs out of life.
  while True:
    (mv1, eat1) = get_move(player1_view, player1.player.get_move, options, 1)
    (mv2, eat2) = get_move(player2_view, player2.player.get_move, options, 2)
    # Players might have exhausted all of their energy eating.
    l1 = player1_view.GetLife()
    l2 = player2_view.GetLife()
    if check_if_game_over(l1, l2, options, game, player1_view.GetRound()):
      break

    game.ExecuteMoves(mv1, eat1, mv2, eat2)
    if options.display:
      game_interface.curses_draw_board(game)
      game_interface.curses_init_round(game)
    else:
      print mv1, eat1, mv2, eat2
      print player1_view.GetLife(), player2_view.GetLife()

    # Players might have exhausted all of their energy eating.
    l1 = player1_view.GetLife()
    l2 = player2_view.GetLife()
    if check_if_game_over(l1, l2, options, game, player1_view.GetRound()):
      break

def main(argv):
  parser = OptionParser()
  parser.add_option("-d", action="store", dest="display", default=1, type=int,
                    help="whether to display the GUI board")
  parser.add_option("--plant_bonus", dest="plant_bonus", default=20,
                    help="bonus for eating a nutritious plant",type=int)
  parser.add_option("--plant_penalty", dest="plant_penalty", default=10,
                    help="penalty for eating a poisonous plant",type=int)
  parser.add_option("--observation_cost", dest="observation_cost", default=1,
                    help="cost for getting an image for a plant",type=int)
  parser.add_option("--starting_life", dest="starting_life", default=100,
                    help="starting life",type=int)
  parser.add_option("--life_per_turn", dest="life_per_turn", default=1,
                    help="life spent per turn",type=int)
  parser.add_option("--single_player_mode", action="store_true", dest="single_player_mode",
                    help="if specified, run in single player mode. Ignore player 2.")
  (options, args) = parser.parse_args()

  try:
    run(options)
  except KeyboardInterrupt:
    if options.display:
      game_interface.curses_close()
  except:
    game_interface.curses_close()
    traceback.print_exc(file=sys.stdout)

if __name__ == '__main__':
  main(sys.argv)
