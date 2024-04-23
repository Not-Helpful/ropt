
from passes.PassClasses import Pass, State, Function
from include.instructions import CallInstruction, JumpInstruction, Stack
from include.ControlFlow import BasicBlock
import copy

class StackPass(Pass):

    name: str = "internal-stack-pass"
    export: str = "internal-stack-pass"
    
    requires = {

    }

    def run(state: State):
        funcList: list[Function] = state.functions
        for func in funcList:
            StackPass.computeStack(Stack(), 0, func.cfg)
            
    
    def computeStack(stack: Stack, index, basicBlockList: list[BasicBlock]):

        for block in basicBlockList:
            if index > block.end_index:
                continue
            for instruction in block.instructions:
            
                if instruction.instruction.opname == "JUMP_BACKWARD":
                    instruction.stack_effect(stack, False)
                    backstack = copy.deepcopy(stack)
                    instruction.stacks.append(backstack)
                    # May cause strange behavior
                    return

                elif isinstance(instruction, JumpInstruction):
                    match instruction.isConditional():
                        case True:
                            jumpstack = copy.deepcopy(stack)
                            instruction.stack_effect(jumpstack, True)
                            instruction.stacks.append(jumpstack)
                            StackPass.computeStack(copy.deepcopy(jumpstack), instruction.get_jump_target(), basicBlockList)

                            instruction.stack_effect(stack, False)
                            nojumpStack = copy.deepcopy(stack)
                            instruction.stacks.append(nojumpStack)
                        case False:
                            instruction.stack_effect(stack, True)
                            jumpstack = copy.deepcopy(stack)
                            instruction.stacks.append(jumpstack)
                            StackPass.computeStack(copy.deepcopy(jumpstack), instruction.get_jump_target(), basicBlockList)
                            return
                else:
                    instruction.stack_effect(stack)
                    elseStack = copy.deepcopy(stack)
                    instruction.stacks.append(elseStack)
