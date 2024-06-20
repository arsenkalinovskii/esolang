from Commands import ExecutionCmds, IOCommands,\
    MovementCmds, StackCommands, MemoryCommands

global cmds

cmds = {
#######################################
    ord('r'): MovementCmds.MoveRight,
    ord('l'): MovementCmds.MoveLeft,
    ord('d'): MovementCmds.MoveDown,
    ord('u'): MovementCmds.MoveUp,
    ord('R'): MovementCmds.MoveRightCond,
    ord('L'): MovementCmds.MoveLeftCond,
    ord('D'): MovementCmds.MoveDownCond,
    ord('U'): MovementCmds.MoveUpCond,
    ord('$'): MovementCmds.MoveRandom,
    ord('j'): MovementCmds.Jump,
    ord('J'): MovementCmds.JumpCond,
    ord('s'): MovementCmds.Skip,
    ord('S'): MovementCmds.SkipCond,
#######################################
    0x27: ExecutionCmds.Return,
    ord('e'): ExecutionCmds.ExecuteFunction,
    ord('E'): ExecutionCmds.ExecuteFunctionCond,
    0: ExecutionCmds.nop,
#######################################
    ord('g'): MemoryCommands.GetByte,
    ord('c'): MemoryCommands.Write,
    ord('C'): MemoryCommands.WriteNBytes,
    ord('n'): MemoryCommands.GetBigInt,
    ord('f'): MemoryCommands.GetDecimal,
    ord('\"'): MemoryCommands.GetBytes,
#######################################
    ord('i'): IOCommands.GetInt,
    ord('I'): IOCommands.PrintInt,
    ord('F'): IOCommands.GetDecimal,
    ord(','): IOCommands.PrintDecimal,
    ord('B'): IOCommands.GetByte,
    ord('.'): IOCommands.PrintString,
    2: IOCommands.GetString,
    3: IOCommands.PrintByte,
#######################################
    ord('+'): StackCommands.AddB,
    ord('-'): StackCommands.SubB,
    ord('*'): StackCommands.MulB,
    ord('/'): StackCommands.DivB,
    ord('%'): StackCommands.ModB,
    ord('!'): StackCommands.NotB,
    ord('='): StackCommands.EquB,
    ord('>'): StackCommands.MoreB,
    ord('<'): StackCommands.LessB,
    ord('^'): StackCommands.AndB,
    ord('v'): StackCommands.OrB,
    ord('{'): StackCommands.AddI,
    ord('}'): StackCommands.SubI,
    ord('['): StackCommands.MulI,
    ord(']'): StackCommands.DivI,
    ord('@'): StackCommands.ModI,
    ord('?'): StackCommands.EquI,
    ord('\\'): StackCommands.MoreI,
    ord('0'): StackCommands.AddF,
    ord('t'): StackCommands.SubF,
    ord('m'): StackCommands.MulF,
    ord('k'): StackCommands.DivF,
    ord('G'): StackCommands.EquF,
    ord('Y'): StackCommands.MoreF
}