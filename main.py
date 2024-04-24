#!/usr/bin/env python3


from passes import passlist
from passes.PassClasses import State, Function
from include import instructions as ins
from include import ControlFlow as cf
import dis
import importlib
import inspect

state = State()

def constructControlFlowGraph(instructionList: list[ins.OpCode]):
    BB=cf.createBasicBlocks(instructionList)
    cf.findJumpTargets(BB)
    return BB

def runInternalPasses():
    print("Running Internal Passes")
    
    for p in passlist:
        if p.name.__contains__("internal"):
            runPass(p)

def passEngine():
    #TODO Make generic
    passname = "t"

    sourcecode = './explore/testing.py'
    pyPath = 'explore.testing'

    funcList = getFuncList(sourcecode, pyPath)
    # printFuncList(funcList)
    
    for func in funcList:
        func.cfg = constructControlFlowGraph(func.instructionList)
        # printCFG(func)

    state.functions = funcList

    runInternalPasses()

    for func in state.functions:
        printCFG(func)

    for p in passlist:
        if p.name == passname:
            passToBeRun = p
            break

    runPass(passToBeRun)
    # print(state.data)

def runAllPasses():
    sourcecode = './explore/testing.py'
    pyPath = 'explore.testing'

    funcList = getFuncList(sourcecode, pyPath)
    state.source = sourcecode
    # printFuncList(funcList)
    
    for func in funcList:
        func.cfg = constructControlFlowGraph(func.instructionList)
        printCFG(func)

    state.functions = funcList

    runInternalPasses()

    for p in passlist:
        runPass(p)

    

def getFuncList(pathname, pyPath) -> list[Function]:
    
    funcList = []

    infile = open(pathname, "r")
    sourcecode = infile.read()

    instructionList = dis.get_instructions(sourcecode)
    instructions = []

    for instruction in instructionList:
        a = ins.makeInstruction(instruction)
        # print(a)
        instructions.append(a)

    funcList.append(Function("Top Level", instructions))
    
    members = inspect.getmembers(importlib.import_module(pyPath))

    for name, member in members:
        if inspect.isfunction(member):
            instructionList = dis.get_instructions(member)
            instructions = []

            for instruction in instructionList:
                a = ins.makeInstruction(instruction)
                # print(a)
                instructions.append(a)

            funcList.append(Function( member.__name__, instructions))

    infile.close()
    return funcList

def printFuncList(funcList: list[Function]):

    for func in funcList:
        print("\n" + func.name + ": ")
        print("\nInstructions:\n")
        print(func.instructionList)

def printCFG(func):
    blocks = func.cfg
    print(func.name + ":")
    for block in blocks:
        print('\n', block.name, ": ")

        for opcode in block.instructions:
            if(isinstance(opcode, ins.CallInstruction)):
                print(opcode.instruction.offset, ' ', opcode.instruction.opname, ' ', opcode.calls )
            
            else:
                print(opcode.instruction.offset, ' ', opcode.instruction.opname, ' ', opcode.instruction.argval )


        print('Jump Targets: ')

        for b in block.jump_target:
            print(b, ' ')
    
    print('\n')

def runPass(passToRun):
    if passToRun not in state.ran:    
        dep = getDependentPasses(passToRun)
        for p in dep:
            runPass(p)
        passToRun.run(state)
        state.ran.append(passToRun)

def getDependentPasses(passToBeRun):
    dependentPasses = []
    for p in passlist:
        if hasattr(p, "export"):
            if (p.export in passToBeRun.requires) and (p not in state.ran):
                dependentPasses.append(p)
    return dependentPasses


if __name__ == "__main__":
    runAllPasses()
    # passEngine()


#TODO:
    # 1. wrapper classes
        # a. convert instruction to wrapper class
    # 2. Instructions in function/basicblock form
    # 3. cfg
    # 4. replace instructions

#StoreIteration()
#instruction = store fast or store const
    
#TODO: 
    #1. Read chapters 11 and 12 of dragon book