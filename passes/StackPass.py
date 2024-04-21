
from passes.PassClasses import Pass, State
from include.instructions import CallInstruction, JumpInstruction, Stack
from include.ControlFlow import BasicBlock
import copy

class StackPass(Pass):

    name: str = "internal-stack-pass"
    export: str = "internal-stack-pass"
    
    requires = {

    }

    def run(state: State):
        pass
    
    def computeStack(self, stack: Stack, index, basicBlockList: list[BasicBlock]) -> list[Stack]:

        for block in basicBlockList:
            if index > block.end_index:
                continue
            for instruction in block.instructions:
                if instruction.isinstance(JumpInstruction):
                    # TODO: 
                    # jump_target_offset pass
                    jumpstack = copy.deepcopy(stack)
                    instruction.stack_effect(jumpstack, True)
                    instruction.stacks.extend(jumpstack)
                    self.computeStack(jumpstack, instruction.jump_target_offset, basicBlockList)
                    
                    instruction.stack_effect(stack, False)
                    instruction.stacks.extend(stack)
                
                else:
                    instruction.stack_effect(stack)
                    instruction.stacks.extend(stack)