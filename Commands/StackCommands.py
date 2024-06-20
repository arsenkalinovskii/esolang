from Commands.include import ERR, interp, SUCCESS


def conditional(func):
    def inner(*args, **kwargs):
        if interp.cond:
            func(*args, **kwargs)
    return inner


def byte_two_arg(func):
    def inner(*args, **kwargs):
        if len(interp.bstack >= 2):
            func(*args, **kwargs)
        else:
            return ERR
    return inner


def byte_one_arg(func):
    def inner(*args, **kwargs):
        if len(interp.bstack >= 1):
            func(*args, **kwargs)
        else:
            return ERR
    return inner


def int_two_arg(func):
    def inner(*args, **kwargs):
        if len(interp.istack >= 2):
            func(*args, **kwargs)
        else:
            return ERR
    return inner


def flt_two_arg(func):
    def inner(*args, **kwargs):
        if len(interp.fstack >= 2):
            func(*args, **kwargs)
        else:
            return ERR
    return inner


@byte_two_arg
def AddB():
    x, y = interp.bstack.pop(), interp.bstack.pop()
    interp.bstack.push((x + y) % 256)
    return SUCCESS


@byte_two_arg
def SubB():
    x, y = interp.bstack.pop(), interp.bstack.pop()
    interp.bstack.push((x - y) % 256)
    return SUCCESS


@byte_two_arg
def MulB():
    x, y = interp.bstack.pop(), interp.bstack.pop()
    interp.bstack.push(x * y % 256)
    return SUCCESS


@byte_two_arg
def DivB():
    x, y = interp.bstack.pop(), interp.bstack.pop()
    if y == 0:
        return ERR
    interp.bstack.push(x // y)
    return SUCCESS


@byte_two_arg
def ModB():
    x, y = interp.bstack.pop(), interp.bstack.pop()
    if y == 0:
        return ERR
    interp.bstack.push(x % y)
    return SUCCESS


@byte_one_arg
def NotB():
    x = interp.bstack.pop()
    interp.bstack.push(~x % 256)
    return SUCCESS


@byte_two_arg
def EquB():
    x, y = interp.bstack.pop(), interp.bstack.pop()
    interp.bstack.push(x == y)
    return SUCCESS


@byte_two_arg
def MoreB():
    x, y = interp.bstack.pop(), interp.bstack.pop()
    interp.bstack.push(x > y)
    return SUCCESS


@byte_two_arg
def LessB():
    x, y = interp.bstack.pop(), interp.bstack.pop()
    interp.bstack.push(x < y)
    return SUCCESS


@byte_two_arg
def AndB():
    x, y = interp.bstack.pop(), interp.bstack.pop()
    interp.bstack.push(x & y)
    return SUCCESS


@byte_two_arg
def OrB():
    x, y = interp.bstack.pop(), interp.bstack.pop()
    interp.bstack.push(x | y)
    return SUCCESS


@int_two_arg
def AddI():
    x, y = interp.istack.pop(), interp.istack.pop()
    interp.istack.push(x + y)
    return SUCCESS


@int_two_arg
def SubI():
    x, y = interp.istack.pop(), interp.istack.pop()
    interp.istack.push(x - y)
    return SUCCESS


@int_two_arg
def MulI():
    x, y = interp.istack.pop(), interp.istack.pop()
    interp.istack.push(x*y)
    return SUCCESS


@int_two_arg
def DivI():
    x, y = interp.istack.pop(), interp.istack.pop()
    if y == 0:
        return ERR
    interp.istack.push(x // y)
    return SUCCESS


@int_two_arg
def ModI():
    x, y = interp.istack.pop(), interp.istack.pop()
    if y == 0:
        return ERR
    interp.istack.push(x % y)
    return SUCCESS


@int_two_arg
def EquI():
    x, y = interp.istack.pop(), interp.istack.pop()
    interp.bstack.push(x == y)
    return SUCCESS


@int_two_arg
def MoreI():
    x, y = interp.istack.pop(), interp.istack.pop()
    interp.bstack.push(x > y)
    return SUCCESS


@flt_two_arg
def AddF():
    x, y = interp.fstack.pop(), interp.fstack.pop()
    interp.fstack.push(x + y)
    return SUCCESS


@flt_two_arg
def SubF():
    x, y = interp.fstack.pop(), interp.fstack.pop()
    interp.fstack.push(x - y)
    return SUCCESS


@flt_two_arg
def MulF():
    x, y = interp.fstack.pop(), interp.fstack.pop()
    interp.fstack.push(x * y)
    return SUCCESS


@flt_two_arg
def DivF():
    x, y = interp.fstack.pop(), interp.fstack.pop()
    interp.fstack.push(x / y)
    return SUCCESS


@flt_two_arg
def EquF():
    x, y = interp.fstack.pop(), interp.fstack.pop()
    interp.bstack.push(x == y)
    return SUCCESS


@flt_two_arg
def MoreF():
    x, y = interp.fstack.pop(), interp.fstack.pop()
    interp.bstack.push(x > y)
    return SUCCESS