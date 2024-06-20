X = 0
Y = 1
TOP = -1

UP = [0, -1]
DOWN = [0, 1]
RIGHT = [1, 0]
LEFT = [-1, 0]

NONE = -1
EXEC = 0
READ_STR = 1
READ_BI = 2
READ_BF = 3
SKIP = 4

ERR = -1
SUCCESS = 0

MEMSIZ = 65536

global interp

def conditional(func):
    def inner(*args, **kwargs):
        if interp.bstack and interp.bstack.pop() == 1:
            func(*args, **kwargs)
        else:
            def returnError():
                return ERR
            return returnError(*args, **kwargs)
    return inner
