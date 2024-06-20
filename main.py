import os

from Interpretator import InterpretatorInstance

InterpretatorInstance.LoadProgram(os.path.dirname(
    os.path.realpath(__file__)
))
print(InterpretatorInstance.BeginExecute())