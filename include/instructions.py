#!/usr/bin/env python3

import dis

def makeInstruction(ins: dis.Instruction) -> OpCode:
    if ins.opname.__contains__("LOAD_"):
        return LoadInstruction(ins)
    if ins.opname.__contain__("STORE_"):
        return StoreInstruction(ins)
    if ins.opname == "CALL":
        return CallInstruction(ins)
    if ins.opname == "POP_TOP":
        return StackInstruction(ins)
    if ins.opname == "RETURN_VALUE":
        return ReturnInstruction(ins)


class OpCode():
    """Doc String."""
    instruction: dis.Instruction

    def __init__(self, instruction: dis.Instruction):
        self.instruction = instruction

    def get_args(self):
        return (self.instruction.arg, self.instruction.argval, self.instruction.argrepr)


class LoadInstruction(OpCode):
    """Doc String."""

    def __init__(self, instruction: dis.Instruction):
    """Doc String."""
        super(instruction)

class StoreInstruction(OpCode):
    """Doc String."""

    def __init__(self, instruction: dis.Instruction):
        super(instruction)

class CallInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super(instruction)

class StackInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super(instruction)

class ReturnInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super(instruction)
