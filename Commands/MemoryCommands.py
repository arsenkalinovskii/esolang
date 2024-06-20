from Commands.include import ERR, interp, MEMSIZ, \
    SUCCESS, READ_BF, READ_BI, READ_STR

def Write():
    if len(interp.bstack) < 3:
        print("Error occurred while trying to fetch data: not enough arguments given!")
        return ERR
    ptr = interp.bstack.pop() << 8 + interp.bstack.pop()
    val = interp.bstack.pop()
    interp.memry[ptr] = val
    return SUCCESS


def WriteNBytes():
    if len(interp.bstack) < 3:
        print("Error occurred while trying to fetch data: not enough arguments given!")
        return ERR
    ptr = interp.bstack.pop() << 8 + interp.bstack.pop()
    N = interp.bstack.pop()
    if len(interp.bstack) < N:
        print("Error occurred while trying to write data in memory: not enough arguments given!")
    for i in range(N):
        interp.memry[(ptr + i) % MEMSIZ] = interp.bstack.pop()
    return SUCCESS


def GetByte():
    if len(interp.bstack) < 2:
        print("Error occurred while trying to fetch data: not enough arguments given!")
        return ERR
    ptr = interp.bstack.pop() << 8 + interp.bstack.pop()
    interp.bstack.append(interp.memry[ptr])
    return SUCCESS


def GetBigInt():
    interp.state = READ_BI
    return SUCCESS


def GetDecimal():
    interp.state = READ_BF
    return SUCCESS


def GetBytes():
    interp.state = READ_STR
    return SUCCESS
