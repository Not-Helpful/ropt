#!/usr/bin/env python3

import dis

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
        super().__init__(instruction)

class StoreInstruction(OpCode):
    """Doc String."""

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

class CallInstruction(OpCode):
    calls: str

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)
        self.calls = None

class StackInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

class ReturnInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

class ResumeInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

class ImportInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

class MakeInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

class IterInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

class JumpInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

    def isConditional(self):
        if self.instruction.opname == "JUMP_ABSOLUTE" or self.instruction.opname == "JUMP_FORWARD":
            return False
        else:
            return True

class DataInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

class CompareInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

class BinaryOPInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)


def makeInstruction(ins: dis.Instruction) -> OpCode:
    if ins.opname.__contains__("LOAD_"):
        return LoadInstruction(ins)
    elif ins.opname.__contains__("STORE_"):
        return StoreInstruction(ins)
    elif ins.opname == "CALL":
        return CallInstruction(ins)
    elif ins.opname == "POP_TOP":
        return StackInstruction(ins)
    elif ins.opname == "END_FOR":
        return StackInstruction(ins)
    elif ins.opname == "PUSH_NULL":
        return StackInstruction(ins)
    elif ins.opname.__contains__("RETURN_"):
        return ReturnInstruction(ins)
    elif ins.opname == "RESUME":
        return ResumeInstruction(ins)
    elif ins.opname.__contains__("IMPORT_"):
        return ImportInstruction(ins)
    elif ins.opname == "MAKE_FUNCTION":
        return MakeInstruction(ins)
    elif ins.opname == "FOR_ITER":
        return JumpInstruction(ins)
    elif ins.opname.__contains__("JUMP_"):
        return JumpInstruction(ins)
    elif ins.opname.__contains__("ITER"):
        return DataInstruction(ins)
    elif ins.opname == "COMPARE_OP":
        return CompareInstruction(ins)
    elif ins.opname == "BINARY_OP":
        return BinaryOPInstruction(ins)
    elif ins.opname.__contains__("LIST"):
        return DataInstruction(ins)
    else:
        print(ins)
        raise NotImplementedError
        #TODO Custom error
    