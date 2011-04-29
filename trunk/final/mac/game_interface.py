# This file was automatically generated by SWIG (http://www.swig.org).
# Version 2.0.2
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.
# This file is compatible with both classic and new-style classes.

from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_game_interface', [dirname(__file__)])
        except ImportError:
            import _game_interface
            return _game_interface
        if fp is not None:
            try:
                _mod = imp.load_module('_game_interface', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _game_interface = swig_import_helper()
    del swig_import_helper
else:
    import _game_interface
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


class SwigPyIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SwigPyIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SwigPyIterator, name)
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _game_interface.delete_SwigPyIterator
    __del__ = lambda self : None;
    def value(self): return _game_interface.SwigPyIterator_value(self)
    def incr(self, n = 1): return _game_interface.SwigPyIterator_incr(self, n)
    def decr(self, n = 1): return _game_interface.SwigPyIterator_decr(self, n)
    def distance(self, *args): return _game_interface.SwigPyIterator_distance(self, *args)
    def equal(self, *args): return _game_interface.SwigPyIterator_equal(self, *args)
    def copy(self): return _game_interface.SwigPyIterator_copy(self)
    def next(self): return _game_interface.SwigPyIterator_next(self)
    def __next__(self): return _game_interface.SwigPyIterator___next__(self)
    def previous(self): return _game_interface.SwigPyIterator_previous(self)
    def advance(self, *args): return _game_interface.SwigPyIterator_advance(self, *args)
    def __eq__(self, *args): return _game_interface.SwigPyIterator___eq__(self, *args)
    def __ne__(self, *args): return _game_interface.SwigPyIterator___ne__(self, *args)
    def __iadd__(self, *args): return _game_interface.SwigPyIterator___iadd__(self, *args)
    def __isub__(self, *args): return _game_interface.SwigPyIterator___isub__(self, *args)
    def __add__(self, *args): return _game_interface.SwigPyIterator___add__(self, *args)
    def __sub__(self, *args): return _game_interface.SwigPyIterator___sub__(self, *args)
    def __iter__(self): return self
SwigPyIterator_swigregister = _game_interface.SwigPyIterator_swigregister
SwigPyIterator_swigregister(SwigPyIterator)

class Vector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Vector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Vector, name)
    __repr__ = _swig_repr
    def iterator(self): return _game_interface.Vector_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _game_interface.Vector___nonzero__(self)
    def __bool__(self): return _game_interface.Vector___bool__(self)
    def __len__(self): return _game_interface.Vector___len__(self)
    def pop(self): return _game_interface.Vector_pop(self)
    def __getslice__(self, *args): return _game_interface.Vector___getslice__(self, *args)
    def __setslice__(self, *args): return _game_interface.Vector___setslice__(self, *args)
    def __delslice__(self, *args): return _game_interface.Vector___delslice__(self, *args)
    def __delitem__(self, *args): return _game_interface.Vector___delitem__(self, *args)
    def __getitem__(self, *args): return _game_interface.Vector___getitem__(self, *args)
    def __setitem__(self, *args): return _game_interface.Vector___setitem__(self, *args)
    def append(self, *args): return _game_interface.Vector_append(self, *args)
    def empty(self): return _game_interface.Vector_empty(self)
    def size(self): return _game_interface.Vector_size(self)
    def clear(self): return _game_interface.Vector_clear(self)
    def swap(self, *args): return _game_interface.Vector_swap(self, *args)
    def get_allocator(self): return _game_interface.Vector_get_allocator(self)
    def begin(self): return _game_interface.Vector_begin(self)
    def end(self): return _game_interface.Vector_end(self)
    def rbegin(self): return _game_interface.Vector_rbegin(self)
    def rend(self): return _game_interface.Vector_rend(self)
    def pop_back(self): return _game_interface.Vector_pop_back(self)
    def erase(self, *args): return _game_interface.Vector_erase(self, *args)
    def __init__(self, *args): 
        this = _game_interface.new_Vector(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(self, *args): return _game_interface.Vector_push_back(self, *args)
    def front(self): return _game_interface.Vector_front(self)
    def back(self): return _game_interface.Vector_back(self)
    def assign(self, *args): return _game_interface.Vector_assign(self, *args)
    def resize(self, *args): return _game_interface.Vector_resize(self, *args)
    def insert(self, *args): return _game_interface.Vector_insert(self, *args)
    def reserve(self, *args): return _game_interface.Vector_reserve(self, *args)
    def capacity(self): return _game_interface.Vector_capacity(self)
    __swig_destroy__ = _game_interface.delete_Vector
    __del__ = lambda self : None;
Vector_swigregister = _game_interface.Vector_swigregister
Vector_swigregister(Vector)

UP = _game_interface.UP
LEFT = _game_interface.LEFT
DOWN = _game_interface.DOWN
RIGHT = _game_interface.RIGHT
STATUS_UNKNOWN_PLANT = _game_interface.STATUS_UNKNOWN_PLANT
STATUS_NO_PLANT = _game_interface.STATUS_NO_PLANT
STATUS_NUTRITIOUS_PLANT = _game_interface.STATUS_NUTRITIOUS_PLANT
STATUS_POISONOUS_PLANT = _game_interface.STATUS_POISONOUS_PLANT
class GameInterface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, GameInterface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, GameInterface, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _game_interface.new_GameInterface(*args)
        try: self.this.append(this)
        except: self.this = this
    def StartGame(self): return _game_interface.GameInterface_StartGame(self)
    def ExecuteMoves(self, *args): return _game_interface.GameInterface_ExecuteMoves(self, *args)
    def GetPlayer1View(self): return _game_interface.GameInterface_GetPlayer1View(self)
    def GetPlayer2View(self): return _game_interface.GameInterface_GetPlayer2View(self)
    __swig_destroy__ = _game_interface.delete_GameInterface
    __del__ = lambda self : None;
GameInterface_swigregister = _game_interface.GameInterface_swigregister
GameInterface_swigregister(GameInterface)

class PlayerView(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, PlayerView, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, PlayerView, name)
    __repr__ = _swig_repr
    def GetLife(self): return _game_interface.PlayerView_GetLife(self)
    def GetXPos(self): return _game_interface.PlayerView_GetXPos(self)
    def GetYPos(self): return _game_interface.PlayerView_GetYPos(self)
    def GetRound(self): return _game_interface.PlayerView_GetRound(self)
    def GetImage(self): return _game_interface.PlayerView_GetImage(self)
    def GetPlantInfo(self): return _game_interface.PlayerView_GetPlantInfo(self)
    def __init__(self): 
        this = _game_interface.new_PlayerView()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _game_interface.delete_PlayerView
    __del__ = lambda self : None;
PlayerView_swigregister = _game_interface.PlayerView_swigregister
PlayerView_swigregister(PlayerView)


def curses_init():
  return _game_interface.curses_init()
curses_init = _game_interface.curses_init

def curses_close():
  return _game_interface.curses_close()
curses_close = _game_interface.curses_close

def curses_draw_board(*args):
  return _game_interface.curses_draw_board(*args)
curses_draw_board = _game_interface.curses_draw_board

def curses_center_cursor():
  return _game_interface.curses_center_cursor()
curses_center_cursor = _game_interface.curses_center_cursor

def curses_init_round(*args):
  return _game_interface.curses_init_round(*args)
curses_init_round = _game_interface.curses_init_round

def curses_declare_winner(*args):
  return _game_interface.curses_declare_winner(*args)
curses_declare_winner = _game_interface.curses_declare_winner

def curses_debug(*args):
  return _game_interface.curses_debug(*args)
curses_debug = _game_interface.curses_debug


