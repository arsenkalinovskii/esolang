import os.path
import glob
import random

NONE = -1
EXEC = 0
READ_STR = 1
READ_BI = 2
READ_BF = 3
SKIP = 4
RETURN = 5

X = 0
Y = 1

TOP = -1

UP = [0, -1]
DOWN = [0, 1]
RIGHT = [1, 0]
LEFT = [-1, 0]

ERR = -1
SUCCESS = 0

MEMSIZ = 65536

global self


valid_int_chars = '0123456789-'
valid_flt_chars = '0123456789-.'

MEMSIZ = 256*256

class Interpretator:

    global mode
    global bstack, istack, fstack
    global files
    global main_proc
    global pos_stack
    global memry
    global dir_stack
    global field_size_stack
    global cmds

    def __init__(self):
        self.mode = NONE
        self.files = {}
        self.bstack = []
        self.istack = []
        self.fstack = []
        self.pos_stack = list()
        self.dir_stack = list()
        self.field_stack = list()
        self.field_size_stack = list()
        self.memry = [None]*MEMSIZ
        self.cmds = {
            #######################################
            ord('r'): self.MoveRight,
            ord('l'): self.MoveLeft,
            ord('d'): self.MoveDown,
            ord('u'): self.MoveUp,
            ord('R'): self.MoveRightCond,
            ord('L'): self.MoveLeftCond,
            ord('D'): self.MoveDownCond,
            ord('U'): self.MoveUpCond,
            ord('$'): self.MoveRandom,
            ord('j'): self.Jump,
            ord('J'): self.JumpCond,
            ord('s'): self.Skip,
            ord('S'): self.SkipCond,
            #######################################
            ord('Z'): self.Return,
            ord('e'): self.ExecuteFunction,
            ord('E'): self.ExecuteFunctionCond,
            ord(" "): self.nop,
            #######################################
            ord('x'): self.FetchByte, # field
            ord('g'): self.GetByte,
            ord('0'): self.PutNumber0,
            ord('1'): self.PutNumber1,
            ord('2'): self.PutNumber2,
            ord('3'): self.PutNumber3,
            ord('4'): self.PutNumber4,
            ord('5'): self.PutNumber5,
            ord('6'): self.PutNumber6,
            ord('7'): self.PutNumber7,
            ord('8'): self.PutNumber8,
            ord('9'): self.PutNumber9,
            ord('c'): self.Write,
            ord('C'): self.WriteNBytes,
            ord('n'): self.GetBigInt,
            ord('f'): self.GetDecimal,
            ord('\"'): self.GetBytes,
            #######################################
            ord('i'): self.GetInt,
            ord('I'): self.PrintInt,
            ord('F'): self.GetDecimal,
            ord(','): self.PrintDecimal,
            ord('B'): self.GetByteFromConsole,
            ord('.'): self.PrintString,
            ord('J'): self.GetString,
            ord('Q'): self.PrintByte,
            #######################################
            ord(':'): self.DuplicateB,
            ord(';'): self.DuplicateI,
            ord('#'): self.DuplicateF,
            ord('L'): self.Swap,
            ord('+'): self.AddB,
            ord('-'): self.SubB,
            ord('*'): self.MulB,
            ord('/'): self.DivB,
            ord('%'): self.ModB,
            ord('!'): self.NotB,
            ord('='): self.EquB,
            ord('>'): self.MoreB,
            ord('<'): self.LessB,
            ord('^'): self.AndB,
            ord('v'): self.OrB,
            ord('{'): self.AddI,
            ord('}'): self.SubI,
            ord('['): self.MulI,
            ord(']'): self.DivI,
            ord('@'): self.ModI,
            ord('?'): self.EquI,
            ord('\\'): self.MoreI,
            ord('A'): self.AddF,
            ord('t'): self.SubF,
            ord('m'): self.MulF,
            ord('k'): self.DivF,
            ord('G'): self.EquF,
            ord('Y'): self.MoreF
        }


    def LoadProgram(self, path):
        self.bstack = []
        if not os.path.exists(path):
            print("Invalid path given!")
            return
        os.chdir(path)
        files = glob.glob("*.bs")
        if not files:
            print("No Befunge# programs found!")
            return
        for file in files:
            buf = open(file)
            fileord = int(buf.readline())
            buf.close()
            filename = os.path.basename(file)
            self.files[fileord] = filename
        return

    def Execute(self, functionOrd):
        if self.LoadFile(functionOrd) == ERR:
            return ERR
        while True:
            if self.mode == EXEC:
                posX, posY = tuple(self.pos_stack[-1])
                cmdsymb = self.field_stack[-1][posY][posX]
                if cmdsymb in [*self.cmds]:
                    if self.cmds[cmdsymb]() == ERR:
                        return ERR
                else:
                    return ERR
                if self.mode != EXEC:
                    self.Step()
                    continue
            elif self.mode == READ_STR:
                strbuf = ''
                while True:
                    posX, posY = tuple(self.pos_stack[-1])
                    char = chr(self.field_stack[-1][posY][posX])
                    if char == '\"':
                        break
                    strbuf += char
                    self.Step()
                for c in reversed(strbuf[:]):
                    self.bstack.append(c)
            elif self.mode == READ_BI:
                strbuf = ''
                while True:
                    posX, posY = tuple(self.pos_stack[-1])
                    char = chr(self.field_stack[-1][posY][posX])
                    if char == '\n':
                        break
                    strbuf += char
                    self.Step()
                try:
                    num = int(strbuf)
                    self.istack.append(num)
                except Exception:
                    return ERR
            elif self.mode == READ_BF:
                strbuf = ''
                while True:
                    posX, posY = tuple(self.pos_stack[-1])
                    char = chr(self.field_stack[-1][posY][posX])
                    if char == '\f':
                        break
                    strbuf += char
                    self.Step()
                try:
                    num = float(strbuf)
                    self.fstack.append(num)
                except Exception:
                    return -1
            elif self.mode == RETURN:
                self.field_stack.pop()
                self.field_size_stack.pop()
                self.pos_stack.pop()
                self.dir_stack.pop()
                if not self.field_stack:
                    break
            self.mode = EXEC
            self.Step()
        return SUCCESS


    def BeginExecute(self):
        self.mode = EXEC
        return self.Execute(0)

    def LoadFile(self, functionOrd):
        filebuf = open(self.files[functionOrd])
        filebuf.readline()
        lenY, lenX = [int(i) for i in filebuf.readline().split(' ')]
        self.field_size_stack.append([lenY, lenX])
        field = [0]*lenY
        try:
            for y in range(lenY):
                line = filebuf.readline()
                field[y] = [0]*lenX
                for x in range(lenX):
                    field[y][x] = ord(line[x])
        except Exception:
            print("Unexpected end of file! Incorrect file header!")
            return ERR
        self.field_stack.append(field)
        self.pos_stack.append([0, 0])
        self.dir_stack.append(RIGHT)
        return SUCCESS


    def Step(self):
        self.pos_stack[-1][0] += self.dir_stack[-1][0]
        self.pos_stack[-1][1] += self.dir_stack[-1][1]
        self.pos_stack[-1][0] %= self.field_size_stack[-1][1]
        self.pos_stack[-1][1] %= self.field_size_stack[-1][0]
        return

############################################################

    def check_cond(self):
        if not self.bstack:
            return ERR
        c = self.bstack.pop()
        if not (c in [0, 1]):
            return ERR
        return c
            
    def MoveRight(self):
        self.dir_stack[TOP] = RIGHT
        return SUCCESS

    def MoveLeft(self):
        self.dir_stack[TOP] = LEFT
        return SUCCESS

    def MoveUp(self):
        self.dir_stack[TOP] = UP
        return SUCCESS

    def MoveDown(self):
        self.dir_stack[TOP] = DOWN
        return SUCCESS

    
    def MoveRightCond(self):
        cond = self.check_cond()
        if cond == ERR:
            return ERR
        if cond:
            self.MoveRight()
        return SUCCESS

    
    def MoveLeftCond(self):
        cond = self.check_cond()
        if cond == ERR:
            return ERR
        if cond:
            self.MoveLeft()
        return SUCCESS

    
    def MoveUpCond(self):
        cond = self.check_cond()
        if cond == ERR:
            return ERR
        if cond:
            self.MoveUp()
        return SUCCESS

    
    def MoveDownCond(self):
        cond = self.check_cond()
        if cond == ERR:
            return ERR
        if cond:
            self.MoveDown()
        return SUCCESS

    def MoveRandom(self):
        dirs = [UP, DOWN, RIGHT, LEFT]
        self.dir_stack[TOP] = dirs[random.randint(0, 3)]
        return SUCCESS

    def Jump(self):
        if len(self.bstack) < 2:
            print("Failed to perform jump: expected at least 2 values in stack!")
            return ERR
        x, y = self.bstack.pop(), self.bstack.pop()
        leny, lenx = self.field_size_stack[TOP][0], self.field_size_stack[TOP][1]

        x = x % lenx
        y = y % leny

        self.pos_stack[TOP] = [x, y]
        return SUCCESS

    
    def JumpCond(self):
        cond = self.check_cond()
        if cond == ERR:
            return ERR
        if cond:
            self.Jump()
        return SUCCESS

    def Skip(self):
        self.mode = SKIP
        return SUCCESS

    
    def SkipCond(self):
        cond = self.check_cond()
        if cond == ERR:
            return ERR
        if cond:
            self.Skip()
        return SUCCESS

############################################################
    def ExecuteFunction(self):
        if not self.bstack:
            print("Failed to execute a function: stack is empty!")
            return ERR
        functionOrd = self.bstack.pop()
        if not (functionOrd in [*self.cmds]):
            print("Failed to execute a function: functionOrd is out of bounds!")
            return ERR
        result = self.Execute(functionOrd)
        return result

    
    def ExecuteFunctionCond(self):
        cond = self.check_cond()
        if cond == ERR:
            return ERR
        if cond:
            return self.ExecuteFunction()
        return SUCCESS

    def Return(self):
        if not self.bstack:
            print("Failed to return from program: stack is empty!")
            return ERR
        self.mode = RETURN
        print(self.bstack[-1])
        return self.bstack.pop()

    def nop(self):
        return SUCCESS

############################################################

    def Write(self):
        if len(self.bstack) < 3:
            print("Error occurred while trying to fetch data: not enough arguments given!")
            return ERR
        ptr = self.bstack.pop() << 8 + self.bstack.pop()
        val = self.bstack.pop()
        self.memry[ptr] = val
        return SUCCESS

    def WriteNBytes(self):
        if len(self.bstack) < 3:
            print("Error occurred while trying to fetch data: not enough arguments given!")
            return ERR
        ptr = self.bstack.pop() << 8 + self.bstack.pop()
        N = self.bstack.pop()
        if len(self.bstack) < N:
            print("Error occurred while trying to write data in memory: not enough arguments given!")
        for i in range(N):
            self.memry[(ptr + i) % MEMSIZ] = self.bstack.pop()
        return SUCCESS

    def GetByte(self):
        if len(self.bstack) < 2:
            print("Error occurred while trying to fetch data: not enough arguments given!")
            return ERR
        ptr = self.bstack.pop() << 8 + self.bstack.pop()
        self.bstack.append(self.memry[ptr])
        return SUCCESS


    def PutNumber0(self):
        self.bstack.append(0)
        return SUCCESS


    def PutNumber1(self):
        self.bstack.append(1)
        return SUCCESS


    def PutNumber2(self):
        self.bstack.append(2)
        return SUCCESS


    def PutNumber3(self):
        self.bstack.append(3)
        return SUCCESS


    def PutNumber4(self):
        self.bstack.append(4)
        return SUCCESS


    def PutNumber5(self):
        self.bstack.append(5)
        return SUCCESS


    def PutNumber6(self):
        self.bstack.append(6)
        return SUCCESS


    def PutNumber7(self):
        self.bstack.append(7)
        return SUCCESS


    def PutNumber8(self):
        self.bstack.append(8)
        return SUCCESS


    def PutNumber9(self):
        self.bstack.append(9)
        return SUCCESS


    def GetBigInt(self):
        self.mode = READ_BI
        return SUCCESS

    def GetDecimal(self):
        self.mode = READ_BF
        return SUCCESS

    def GetBytes(self):
        self.mode = READ_STR
        return SUCCESS

    def FetchByte(self):
        self.Step()
        x = self.pos_stack[-1][0]
        y = self.pos_stack[-1][1]
        byte = self.field_stack[-1][y][x]
        self.bstack.append(byte)
        return SUCCESS

############################################################

    def GetInt(self):
        try:
            val = int(input())
            self.istack.append(val)
        except ValueError:
            return ERR
        return SUCCESS

    def GetDecimal(self):
        try:
            val = float(input())
            self.fstack.append(val)
        except ValueError:
            return ERR
        return SUCCESS

    def GetByteFromConsole(self):
        try:
            val = input()
            if val.isnumeric():
                val = int(val)
            else:
                val = ord(val)
            if val > 255:
                print("Invalid input given!")
                return ERR
        except Exception:
            print("Invalid input given!")
            return ERR
        self.bstack.append(val)
        return SUCCESS

    def GetString(self):
        val = input() + '\0'
        for char in reversed(val):
            self.bstack.append(char)
        return SUCCESS

    def PrintInt(self):
        if not self.istack:
            return ERR
        print(self.istack.pop())
        return SUCCESS

    def PrintDecimal(self):
        if not self.fstack:
            return ERR
        print(self.fstack.pop())
        return SUCCESS

    def PrintByte(self):
        if not self.bstack:
            return ERR
        print(self.bstack.pop())
        return SUCCESS

    def PrintString(self):
        res_str = ''
        while self.bstack and self.bstack[-1]:
            res_str += self.bstack.pop()
        print(res_str)
        return SUCCESS
    
############################################################

    
    def byte_check_for_two_args(self):
        if len(self.bstack) >= 2:
            return True
        else:
            return ERR
    
    def byte_check_for_single_arg(self):
        if self.bstack:
            return True
        else:
            return ERR


    def int_check_for_two_args(self):
        if len(self.istack) >= 2:
            return True
        else:
            return ERR
    

    def flt_check_for_two_args(self):
        if len(self.fstack) >= 2:
            return True
        else:
            return ERR

    def DuplicateB(self):
        if not self.bstack:
            return SUCCESS
        self.bstack.append(self.bstack[-1])
        return SUCCESS


    def DuplicateI(self):
        if not self.istack:
            return SUCCESS
        self.istack.append(self.istack[-1])
        return SUCCESS


    def DuplicateF(self):
        if not self.fstack:
            return SUCCESS
        self.fstack.append(self.fstack[-1])
        return SUCCESS


    def Swap(self):
        if self.byte_check_for_two_args() == ERR:
            return ERR
        temp = self.bstack[-1]
        self.bstack[-1] = self.bstack[-2]
        self.bstack[-2] = temp
        return SUCCESS


    def AddB(self):
        if self.byte_check_for_two_args() == ERR:
            return ERR
        x, y = self.bstack.pop(), self.bstack.pop()
        self.bstack.append((x + y) % 256)
        return SUCCESS

    
    def SubB(self):
        if self.byte_check_for_two_args() == ERR:
            return ERR
        x, y = self.bstack.pop(), self.bstack.pop()
        self.bstack.append((x - y) % 256)
        return SUCCESS

    
    def MulB(self):
        if self.byte_check_for_two_args() == ERR:
            return ERR
        x, y = self.bstack.pop(), self.bstack.pop()
        self.bstack.append(x * y % 256)
        return SUCCESS

    
    def DivB(self):
        if self.byte_check_for_two_args() == ERR:
            return ERR
        x, y = self.bstack.pop(), self.bstack.pop()
        if y == 0:
            return ERR
        self.bstack.append(x // y)
        return SUCCESS

    
    def ModB(self):
        if self.byte_check_for_two_args() == ERR:
            return ERR
        x, y = self.bstack.pop(), self.bstack.pop()
        if y == 0:
            return ERR
        self.bstack.append(x % y)
        return SUCCESS

    
    def NotB(self):
        if self.byte_check_for_single_arg() == ERR:
            return ERR
        x = self.bstack.pop()
        self.bstack.append(~x % 256)
        return SUCCESS

    
    def EquB(self):
        if self.byte_check_for_two_args() == ERR:
            return ERR
        x, y = self.bstack.pop(), self.bstack.pop()
        self.bstack.append(int(x == y))
        return SUCCESS

    
    def MoreB(self):
        if self.byte_check_for_two_args() == ERR:
            return ERR
        x, y = self.bstack.pop(), self.bstack.pop()
        self.bstack.append(int(x > y))
        return SUCCESS

    
    def LessB(self):
        if self.byte_check_for_two_args() == ERR:
            return ERR
        x, y = self.bstack.pop(), self.bstack.pop()
        self.bstack.append(int(x < y))
        return SUCCESS

    
    def AndB(self):
        if self.byte_check_for_two_args() == ERR:
            return ERR
        x, y = self.bstack.pop(), self.bstack.pop()
        self.bstack.append(int(x & y))
        return SUCCESS

    
    def OrB(self):
        if self.byte_check_for_two_args() == ERR:
            return ERR
        x, y = self.bstack.pop(), self.bstack.pop()
        self.bstack.append(int(x | y))
        return SUCCESS

    
    def AddI(self):
        if self.int_check_for_two_args() == ERR:
            return ERR
        x, y = self.istack.pop(), self.istack.pop()
        self.istack.append(x + y)
        return SUCCESS

    
    def SubI(self):
        if self.int_check_for_two_args() == ERR:
            return ERR
        x, y = self.istack.pop(), self.istack.pop()
        self.istack.append(x - y)
        return SUCCESS

    
    def MulI(self):
        if self.int_check_for_two_args() == ERR:
            return ERR
        x, y = self.istack.pop(), self.istack.pop()
        self.istack.append(x * y)
        return SUCCESS

    
    def DivI(self):
        if self.int_check_for_two_args() == ERR:
            return ERR
        x, y = self.istack.pop(), self.istack.pop()
        if y == 0:
            return ERR
        self.istack.append(x // y)
        return SUCCESS

    
    def ModI(self):
        if self.int_check_for_two_args() == ERR:
            return ERR
        x, y = self.istack.pop(), self.istack.pop()
        if y == 0:
            return ERR
        self.istack.append(x % y)
        return SUCCESS

    
    def EquI(self):
        if self.int_check_for_two_args() == ERR:
            return ERR
        x, y = self.istack.pop(), self.istack.pop()
        self.bstack.append(x == y)
        return SUCCESS

    
    def MoreI(self):
        if self.int_check_for_two_args() == ERR:
            return ERR
        x, y = self.istack.pop(), self.istack.pop()
        self.bstack.append(x > y)
        return SUCCESS

    
    def AddF(self):
        if self.flt_check_for_two_args() == ERR:
            return ERR
        x, y = self.fstack.pop(), self.fstack.pop()
        self.fstack.append(x + y)
        return SUCCESS

    
    def SubF(self):
        if self.int_check_for_two_args() == ERR:
            return ERR
        x, y = self.fstack.pop(), self.fstack.pop()
        self.fstack.append(x - y)
        return SUCCESS

    
    def MulF(self):
        if self.int_check_for_two_args() == ERR:
            return ERR
        x, y = self.fstack.pop(), self.fstack.pop()
        self.fstack.append(x * y)
        return SUCCESS

    
    def DivF(self):
        if self.int_check_for_two_args() == ERR:
            return ERR
        x, y = self.fstack.pop(), self.fstack.pop()
        self.fstack.append(x / y)
        return SUCCESS

    
    def EquF(self):
        if self.int_check_for_two_args() == ERR:
            return ERR
        x, y = self.fstack.pop(), self.fstack.pop()
        self.bstack.append(x == y)
        return SUCCESS

    
    def MoreF(self):
        if self.int_check_for_two_args() == ERR:
            return ERR
        x, y = self.fstack.pop(), self.fstack.pop()
        self.bstack.append(x > y)
        return SUCCESS
    
    
InterpretatorInstance = Interpretator()