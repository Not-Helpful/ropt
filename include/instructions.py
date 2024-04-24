#!/usr/bin/env python3

import dis
import copy

class StackObject():
    name: str
    deps: list[str]
    ref: bool
    
    def __init__(self, name: str, deps:list[str]):
        self.name = name
        self.deps = deps
    
    def __init__(self, name: str):
        self.name = name
        self.deps = []


class Stack():
    stack: list[StackObject]
    var_store: dict
    varCounter: int

    def __init__(self):
        self.stack = []
        self.var_store = {}
        self.varCounter = 0

    def push(self, arg):
        self.stack.insert(0, arg)

    def pop(self):
        if(len(self.stack) == 0):
            print('Stack is empty. Cannot pop.')
        else:
            return self.stack.pop(0)
        
    def peek(self, num):
        return self.stack[num-1]
    
    def clear(self):
        self.stack.clear()

    def callFuncs(self, funcs, opcode, pushVals, popVals):
        for func in funcs:
            func(self, opcode, pushVals, popVals)


class OpCode():
    """Doc String."""
    instruction: dis.Instruction

    def __init__(self, instruction: dis.Instruction):
        self.instruction = instruction
        self.stacks = []

    def get_args(self):
        return (self.instruction.arg, self.instruction.argval, self.instruction.argrepr)
    
    def stack_effect(self, stack, funcs):
        print('Implement me: stack_effect')


class LoadInstruction(OpCode):
    """Doc String."""

    def __init__(self, instruction: dis.Instruction):
        """Doc String."""
        super().__init__(instruction)

    def stack_effect(self, stack, funcs):
        pushVals = []
        popVals = []

        # LOAD_ATTR --> UNION
        if self.instruction.opname == "LOAD_ATTR":
            popVals.append(stack.pop())
            attr = popVals[0].name + '.' + self.instruction.argrepr
            pushVals.append(StackObject(attr))
            stack.callFuncs(funcs, self, pushVals, popVals)
            stack.push(pushVals[0])

        # LOAD_GLOBAL --> NOOP
        elif self.instruction.opname == "LOAD_GLOBAL":
            val = "GLOBAL_" + self.instruction.argrepr
            if val in stack.var_store.keys():
                pushVals.append(stack.var_store[val])
            else:
                pushVals.append(StackObject("GLOBAL_" + self.instruction.argrepr))    
            stack.callFuncs(funcs, self, pushVals, popVals)
            stack.push(pushVals[0])

        # NOOP
        else:
            if self.instruction.argrepr in stack.var_store.keys():
                pushVals.append(stack.var_store[self.instruction.argrepr])
            else:
                pushVals.append(StackObject('CONST_' + self.instruction.argrepr))
            stack.callFuncs(funcs, self, pushVals, popVals)
            stack.push(pushVals[0])

        

class StoreInstruction(OpCode):
    """Doc String."""

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

    # DESTROY
    def stack_effect(self, stack, funcs):
        pushVals = []
        popVals = []

        popVals.append(stack.pop())

        newVar = copy.deepcopy(popVals[0])
        newVar.name = self.instruction.argrepr
        popVals[0] = newVar
        stack.var_store[self.instruction.argrepr] = newVar

        stack.callFuncs(funcs, self, pushVals, popVals)


class CallInstruction(OpCode):
    calls: str

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)
        self.calls = None

    # UNION
    def stack_effect(self, stack, funcs):
        pushVals = []
        popVals = []
        numVals = self.instruction.argval

        for i in range(numVals+1):
            popVals.append(stack.pop())
            print('popVals: ', popVals[i].name)

        
        print(self.instruction.offset)
        print(popVals)
        pushVals.append(StackObject(popVals[-1].name + '_RETURN'))
        stack.callFuncs(funcs, self, pushVals, popVals)
        
        stack.push(pushVals[0])

class PopInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction, popCount: int):
        super().__init__(instruction)
        self.popCount = popCount

    # NOOP
    def stack_effect(self, stack, funcs):
        popVals = []
        pushVals = []

        for i in range(self.popCount):
            popVals.append(stack.pop())
        stack.callFuncs(funcs, self, pushVals, popVals)

class PushInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction, pushCount: int, pushVal: str):
        super().__init__(instruction)
        self.pushCount = pushCount
        self.pushVal = pushVal   

    # NOOP
    def stack_effect(self, stack, funcs):
        popVals = []
        pushVals = []

        for i in range(self.pushCount):
            pushVals.append(StackObject(self.pushVal))
            stack.callFuncs(funcs, self, pushVals, popVals)
            stack.push(pushVals[i])

class ReturnInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

    # NOOP (for now)
    def stack_effect(self, stack, funcs):
        popVals = []
        pushVals = []

        if self.instruction.opname == "RETURN_VALUE":
            popVals.append(stack.pop())
            stack.callFuncs(funcs, self, pushVals, popVals)
        elif self.instruction.opname == "RETURN_CONST":
            pass
        else:
            print ("Implement me: stack_effect")

class ResumeInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

    # NOOP
    def stack_effect(self, stack, funcs):
        popVals = []
        pushVals = []
        stack.callFuncs(funcs, self, pushVals, popVals)
        pass

class ImportInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)
    
    # UNION
    def stack_effect(self, stack, funcs):
        popVals = []
        pushVals = []

        if self.instruction.opname == "IMPORT_NAME":
            popVals.append(stack.pop())
            popVals.append(stack.pop())
            pushVals.append(StackObject(self.instruction.argrepr))
            stack.callFuncs(funcs, self, pushVals, popVals)
            stack.push(pushVals[0])
        elif self.instruction.opname == "IMPORT_FROM":
            popVals.append(stack.pop())
            pushVals.append(StackObject(self.instruction.argrepr))
            stack.callFuncs(funcs, self, pushVals, popVals)
            stack.push(pushVals[0])
        else:
            print('Implement me: stack_effect')

class MakeInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)
    
    def stack_effect(self, stack, funcs):
        popVals = []
        pushVals = []
        consumedInd = self.instruction.argval

        if consumedInd == 0:
            pass
        else:
            print("MakeInstruction.stack_effect: Implement Me")

class IterInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)



class JumpInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

    def isConditional(self):
        if self.instruction.opname == "JUMP_ABSOLUTE" or self.instruction.opname == "JUMP_FORWARD" or self.instruction.opname == "JUMP_BACKWARD":
            return False
        else:
            return True
    
    def stack_effect(self, stack, funcs, willJump:bool):
        popVals = []
        pushVals = []

        if (self.isConditional()):
            match willJump:
                case True:   
                    if self.instruction.opname == "FOR_ITER":
                        pushVals.append(StackObject("FOR_ITER_NONE"))
                        stack.callFuncs(funcs, self, pushVals, popVals)
                        stack.push(pushVals[0])    
                    if self.instruction.opname.startswith("POP_JUMP"):
                        popVals.append(stack.pop())
                        stack.callFuncs(funcs, self, pushVals, popVals)
                        return
                case False:
                    # UNION
                    if self.instruction.opname == "FOR_ITER":
                        popVals.append(stack.peek(0))
                        pushVals.append(StackObject("FOR_ITER_next"))
                        stack.callFuncs(funcs, self, pushVals, popVals)
                        stack.push(pushVals[0])
                    elif self.instruction.opname.startswith("POP_JUMP"):
                        popVals.append(stack.pop())
                        stack.callFuncs(funcs, self, pushVals, popVals)
                    else:
                        return
        else: 
            return

    def get_jump_target(self):
            return self.instruction.argval
    



class DataInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

    def stack_effect(self, stack: Stack, funcs):
        popVals = []
        pushVals = []

        if self.instruction.opname.startswith("BUILD_"):
            #UNION
            if self.instruction.opname.__contains__("LIST"):
                pushVals.append(StackObject('list' + str(stack.varCounter)))
                pushVals[0].list = []
                for i in range(self.instruction.argval):
                    popVals.append(copy.deepcopy(stack.pop()))
                    pushVals[0].list.append(popVals[i])
                stack.callFuncs(funcs, self, pushVals, popVals)
                stack.push(pushVals[0])
                stack.varCounter = stack.varCounter + 1

            else:
                # UNION
                for i in range(self.instruction.argval):
                    popVals.append(copy.deepcopy(stack.pop()))
                    pushVals.append(StackObject(self.instruction.opname.removeprefix("BUILD_") + "_OBJECT"))
                    stack.callFuncs(funcs, self, pushVals, popVals)
                    stack.push(pushVals[i])

        # UNION
        elif self.instruction.opname == "LIST_APPEND":
            popVals.append(copy.deepcopy(stack.pop()))
            pushVals.append(stack.peek(self.instruction.argval))
            stack.callFuncs(funcs, self, pushVals, popVals)
        # UNION
        elif self.instruction.opname == "LIST_EXTEND":
            print('UNSUPPORTED OPERATION: LIST_EXTEND')
            popVals.append(copy.deepcopy(stack.pop()))
            pushVals.append(stack.peek(self.instruction.argval))
            stack.callFuncs(funcs, self, pushVals, popVals)
        # UNION    
        elif self.instruction.opname == "GET_ITER":
            popVals.append(copy.deepcopy(stack.pop()))
            pushVals.append(StackObject("iter(" + popVals[0].name + ")"))
            stack.callFuncs(funcs, self, pushVals, popVals)
            stack.push(pushVals[0])
        
        

class CompareInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

    # UNION
    def stack_effect(self, stack, funcs):
        popVals = []
        pushVals = []

        popVals.append(stack.pop())
        popVals.append(stack.pop())
        pushVals.append(StackObject("COMPAREOP_VALUE"))
        stack.callFuncs(funcs, self, pushVals, popVals)
        stack.push(pushVals[0])
        

class BinaryOPInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

    # UNION
    def stack_effect(self, stack, funcs):
        popVals = []
        pushVals = []

        popVals.append(stack.pop())
        popVals.append(stack.pop())
        pushVals.append(StackObject("BINARYOP_VALUE"))
        stack.callFuncs(funcs, self, pushVals, popVals)
        stack.push(pushVals[0])

class BinarySubInstruction(OpCode):

    def __init__(self, instruction: dis.Instruction):
        super().__init__(instruction)

    def stack_effect(self, stack, funcs):
        popVals = []
        pushVals = []

        popVals.append(stack.pop()) # key
        popVals.append(stack.pop()) # container
        
        # SPECIAL CASE NOOP
        if(isinstance(popVals[0], int)):
            listElement = copy.deepcopy(popVals[1].list[int(popVals[0])])
            listElement.name = popVals[1].name + '[' + popVals[0].name + ']'
            pushVals.append(listElement)
            stack.callFuncs(funcs, self, pushVals, popVals)
            stack.push(pushVals[0])
        
        # UNION
        else:
            listElement = StackObject(popVals[1].name + '[' + popVals[0].name + ']')
            pushVals.append(listElement)
            stack.callFuncs(funcs, self, pushVals, popVals)
            stack.push(pushVals[0])


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
    elif ins.opname == "BINARY_SUBSCR":
        return BinarySubInstruction(ins)
    else:
        print(ins)
        raise NotImplementedError
        #TODO Custom error
    