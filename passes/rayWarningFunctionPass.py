


from passes.PassClasses import Pass, State, Function
import include.instructions as ins
from include.ControlFlow import BasicBlock
import copy


class RayWarningFunction(Pass):

    name: str = "ray-warning-fixup"
    export: str = "ray-warning-fixup"
    
    requires = {
        "analysis-dependency",
        "internal-call-names"
    }

    def run(state: State):
        state.stackEffectFuncs.append(RayWarningFunction.fixUpReturnDeps)


    def fixUpReturnDeps(stack: ins.Stack, opcode: ins.OpCode, pushVals: list[ins.StackObject], popVals: list[ins.StackObject]):
        if isinstance(opcode, ins.CallInstruction):
            pushVals[0].deps.append(pushVals[0].name + "$" + str(opcode.instruction.offset))