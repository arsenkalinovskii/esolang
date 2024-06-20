import random
from Commands.include import TOP, UP, DOWN, ERR, \
    RIGHT, LEFT, SKIP, conditional, interp, \
    SUCCESS

def MoveRight():
    interp.dir_stack[TOP] = RIGHT
    return SUCCESS


def MoveLeft():
    interp.dir_stack[TOP] = LEFT
    return SUCCESS


def MoveUp():
    interp.dir_stack[TOP] = UP
    return SUCCESS


def MoveDown():
    interp.dir_stack[TOP] = DOWN
    return SUCCESS


@conditional
def MoveRightCond():
    MoveRight()
    return SUCCESS


@conditional
def MoveLeftCond():
    MoveLeft()
    return SUCCESS


@conditional
def MoveUpCond():
    MoveUp()
    return SUCCESS


@conditional
def MoveDownCond():
    MoveDown()
    return SUCCESS


def MoveRandom():
    dirs = [UP, DOWN, RIGHT, LEFT]
    interp.dir_stack[TOP] = dirs[random.randint(0, 3)]
    return SUCCESS


def Jump():
    if len(interp.bstack) < 2:
        print("Failed to perform jump: expected at least 2 values in stack!")
        return ERR
    x, y = interp.bstack.pop(), interp.bstack.pop()
    leny, lenx = len(interp.field_stack[TOP]),\
                 len(interp.field_stack[TOP][0])

    x = x % lenx
    y = y % leny

    interp.pos_stack[TOP] = [x, y]
    return SUCCESS


@conditional
def JumpCond():
    Jump()
    return SUCCESS


def Skip():
    interp.mode = SKIP
    return SUCCESS


@conditional
def SkipCond():
    Skip()
    return SUCCESS

