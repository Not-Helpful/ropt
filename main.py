#!/usr/bin/env python3


from passes import passlist
from passes.PassClasses import State
from include import instructions as ins
from include import ControlFlow as cf
import dis

state = State()

def passEngine():
    #TODO Make generic
    passname = "t"

    sourcecode = './explore/functioncall.py'
    infile = open(sourcecode, "r")
    sourcecode = infile.read()

    instructionList = dis.get_instructions(sourcecode)
    instructions = []

    for instruction in instructionList:
        a = ins.makeInstruction(instruction)
        # print(a)
        instructions.append(a)
    
    BB = cf.createBasicBlocks(instructions)
    cf.findJumpTargets(BB)

    for block in BB:
        print('\n', block.name, ": ")

        for opcode in block.instructions:
            print(opcode.instruction.offset, ' ', opcode.instruction.opname, ' ', opcode.instruction.argval)

        print('Jump Targets: ')

        for b in block.jump_target:
            print(b, ' ')
    
    print('\n')

    for p in passlist:
        if p.name == passname:
            passToBeRun = p
            break

    runPass(passToBeRun)
    print(state.data)

def runPass(passToRun):
    dep = getDependentPasses(passToRun)
    for p in dep:
        runPass(p)
    passToRun.run(state)

def getDependentPasses(passToBeRun):
    dependentPasses = []
    for p in passlist:
        if hasattr(p, "export"):
            if p.export in passToBeRun.requires:
                dependentPasses.append(p)
    return dependentPasses

if __name__ == "__main__":
    passEngine()




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