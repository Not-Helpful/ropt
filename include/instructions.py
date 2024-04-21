#!/usr/bin/env python3

import dis

class Stack():
    stack: list

    def __init__(self):
        self.stack = []

    def push(self, arg):
        self.stack.insert(0, arg)

    def pop(self):
        if(len(self.stack) == 0):
            print('Stack is empty. Cannot pop.')
        else:
            return self.stack.pop(0)
        
    def peek(self):
        return self.stack[0]
    
    def clear(self):
        self.stack.clear()


class OpCode():
    """Doc String."""
    instruction: dis.Instruction

    def __init__(self, instruction: dis.Instruction):
        self.instruction = instruction
        self.stacks = []

    def get_args(self):
        return (self.instruction.arg, self.instruction.argval, self.instruction.argrepr)
    
    def stack_effect(self, stack):
        print('Implement me: stack_effect')


class LoadInstruction(OpCode):
    """Doc String."""

    def __init__(self, instruction: dis.Instruction):
        """Doc String."""
        super().__init__(instruction)

    def stack_effect(self, stack):
        stack.push(self.instruction.argrepr)

class StoreInstruction(OpCode):
    """Doc String."""

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

    def stack_effect(self, stack):
        stack.pop()

class CallInstruction(OpCode):
    calls: str

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)
        self.calls = None

    def stack_effect(self, stack):
        numVals = self.instruction.argval

        for i in range(numVals):
            stack.pop(0)

class PopInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction, popCount: int):
        super().__init__(instruction)
        self.popCount = popCount

    def stack_effect(self, stack):
        for i in range(self.popCount):
            stack.pop(0)

class PushInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction, pushCount: int, pushVal: str):
        super().__init__(instruction)
        self.pushCount = pushCount
        self.pushVal = pushVal   

    def stack_effect(self, stack):
        for i in range(self.pushCount):
            stack.push(self.pushVal)

class ReturnInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

    def stack_effect(self, stack):
        if self.instruction.opname == "RETURN_VALUE":
            stack.pop()
        elif self.instruction.opname == "RETURN_CONST":
            pass
        else:
            print ("Implement me: stack_effect")

class ResumeInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

    def stack_effect(self, stack):
        pass

class ImportInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)
    
    def stack_effect(self, stack):

        if self.instruction.opname == "IMPORT_NAME":
            stack.pop()
            stack.pop()
            stack.push(self.instruction.argrepr)
        elif self.instruction.opname == "IMPORT_FROM":
            stack.pop()
            stack.push(self.instruction.argrepr)
        else:
            print('Implement me: stack_effect')

class MakeInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)
    
    def stack_effect(self, stack):
        consumedInd = self.instruction.argval

        if consumedInd == 0:
            stack.push(stack.pop())
        else:
            print("MakeInstruction.stack_effect: Implement Me")

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
    
    def stack_effect(self, stack, willJump:bool):
        if (self.isConditional()):
            match willJump:
                case True:
                    if self.instruction.opname.startswith("POP_JUMP"):
                        stack.pop()
                case False:
                    if self.instruction.opname == "FOR_ITER":
                        stack.push("FOR_ITER_next")
                    elif self.instruction.opname.startswith("POP_JUMP"):
                        stack.pop()
                    else:
                        pass
        else:
            pass



class DataInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

    def stack_effect(self, stack):
        if self.instruction.opname.startswith("BUILD_"):
            for i in range(self.instruction.argval):
                stack.pop()
            stack.push(self.instruction.opname.removeprefix("BUILD_") + "_OBJECT")
        elif self.instruction.opname == "LIST_APPEND":
            stack.pop()
        elif self.instruction.opname == "LIST_EXTEND":
            stack.pop()

class CompareInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

    def stack_effect(self, stack):
        stack.pop()
        stack.pop()
        stack.push("COMPAREOP_VALUE")
        

class BinaryOPInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

    def stack_effect(self, stack):
        stack.pop()
        stack.pop()
        stack.push("BINARYOP_VALUE")


def makeInstruction(ins: dis.Instruction) -> OpCode:
    if ins.opname.__contains__("LOAD_"):
        return LoadInstruction(ins)
    elif ins.opname.__contains__("STORE_"):
        return StoreInstruction(ins)
    elif ins.opname == "CALL":
        return CallInstruction(ins)
    elif ins.opname == "POP_TOP":
        return PopInstruction(ins, 1)
    elif ins.opname == "END_FOR":
        return PopInstruction(ins, 2)
    elif ins.opname == "PUSH_NULL":
        return PushInstruction(ins, 1, 'None')
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
    