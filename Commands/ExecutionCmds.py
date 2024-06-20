from Commands.include import interp, conditional, \
     ERR, SUCCESS


def ExecuteFunction():
    if not interp.bstack:
        print("Failed to execute a function: stack is empty!")
        return ERR
    functionOrd = interp.bstack.pop()
    if functionOrd >= len(interp.files) or functionOrd < 0:
        print("Failed to execute a function: functionOrd is out of bounds!")
        return ERR
    result = interp.Execute(functionOrd)
    return result


@conditional
def ExecuteFunctionCond():
    return ExecuteFunction()


def Return():
    if not interp.bstack:
        print("Failed to return from program: stack is empty!")
        return ERR
    return interp.pop()


def nop():
    return SUCCESS
