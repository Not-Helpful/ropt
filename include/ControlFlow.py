from dis import Instruction
from include.instructions import OpCode, JumpInstruction

class BasicBlock():
    instructions: list[OpCode]
    name: str

    def __init__(self, name):
        self.instructions = []
        self.name = name

    def add(self, ins: Instruction):
        self.instructions.append(ins)


def createBasicBlocks(instructionList: list[OpCode]) -> list[BasicBlock]:
    BBList = []
    current = BasicBlock("Main")
    count = 0
    
    for i in instructionList:

        if isinstance(i, JumpInstruction):
            current.add(i)
            BBList.append(current)
            current = BasicBlock(name="BB" + str(count))
            count += 1

        elif i.instruction.is_jump_target:
            if len(current.instructions) != 0:
                BBList.append(current)
                current = BasicBlock(name="BB" + str(count))
                count += 1

            current.add(i)

        else:
            current.add(i)

    if current not in BBList:
        BBList.append(current)
    
    return BBList