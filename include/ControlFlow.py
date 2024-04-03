from dis import Instruction
from include.instructions import OpCode, JumpInstruction

class BasicBlock():
    instructions: list[OpCode]
    name: str
    start_index: int
    end_index: int
    jump_target: list[int]

    def __init__(self, name):
        self.instructions = []
        self.name = name
        self.start_index = None
        self.end_index = None
        self.jump_target = []

    def add(self, ins: OpCode):
        self.instructions.append(ins)

        if self.start_index is None:
            self.start_index = ins.instruction.offset
        
        self.end_index = ins.instruction.offset



def createBasicBlocks(instructionList: list[OpCode]) -> list[BasicBlock]:
    BBList = []
    current = BasicBlock("Main")
    count = 1
    
    for i in instructionList:

        if i.instruction.is_jump_target:
            if len(current.instructions) != 0:
                BBList.append(current)
                current = BasicBlock(name="BB" + str(count))
                count += 1

            current.add(i)

        elif isinstance(i, JumpInstruction):
            current.add(i)
            BBList.append(current)
            current = BasicBlock(name="BB" + str(count))
            count += 1

        else:
            current.add(i)

    if current not in BBList:
        BBList.append(current)
    
    return BBList


def findJumpTargets(basicBlocks: list[BasicBlock]):

    for i, block in enumerate(basicBlocks):

        if isinstance(block.instructions[-1], JumpInstruction):

            jumpTarget = block.instructions[-1].instruction.argval

            if block.instructions[-1].isConditional():
                block.jump_target.append(i+1)
                
            for i,block in enumerate(basicBlocks):
                    if block.start_index <= jumpTarget <= block.end_index:
                        block.jump_target.append(i)
                    

