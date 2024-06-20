from Commands.include import ERR, interp, SUCCESS


def GetInt():
    try:
        val = int(input())
        interp.istack.push(val)
    except ValueError:
        return ERR
    return SUCCESS


def GetDecimal():
    try:
        val = float(input())
        interp.fstack.push(val)
    except ValueError:
        return ERR
    return SUCCESS


def GetByte():
    val = input()[0]
    interp.bstack.push(val)
    return SUCCESS


def GetString():
    val = input() + '\0'
    for char in reversed(val):
        interp.bstack.push(char)
    return SUCCESS


def PrintInt():
    if not interp.istack:
        return ERR
    print(interp.istack.pop())
    return SUCCESS


def PrintDecimal():
    if not interp.fstack:
        return ERR
    print(interp.fstack.pop())
    return SUCCESS


def PrintByte():
    if not interp.bstack:
        return ERR
    print(interp.bstack.pop())
    return SUCCESS


def PrintString():
    res_str = ''
    while interp.bstack and interp.bstack[-1]:
        res_str += chr(interp.bstack)
    print(res_str)
    return SUCCESS