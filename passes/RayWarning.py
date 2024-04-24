from passes.PassClasses import Pass, State, Function
import include.instructions as ins
from include.ControlFlow import BasicBlock
import copy


class RayWarning(Pass):

    name: str = "ray-warning"
    export: str = "ray-warning"
    
    requires = {
        "analysis-dependency",
        "internal-call-names",
        "ray-warning-fixup"
    }

    def run(state: State):
        for func in state.functions:
            for block in func.cfg:
                for instruction in block.instructions:
                    if hasattr(instruction, "calls"):
                        if instruction.calls == "ray_get":
                            retVal = 'GLOBAL_NULL + ray_get_RETURN$' + str(instruction.instruction.offset)
                            # We scan ahead for all remote calls
                            remotes = RayWarning.checkForRemotes(func.cfg, instruction.instruction.offset, retVal)
                            if remotes:
                                RayWarning.printWarning(instruction.instruction.positions.lineno, remotes)

    def checkForRemotes(cfg: list[BasicBlock], offset, retVal) -> list[ins.OpCode]:
        remoteOffsets = []
        for block in cfg:
            if offset > block.end_index:
                continue
            for instruction in block.instructions:
                if offset > instruction.instruction.offset:
                    continue
                if isinstance(instruction, ins.CallInstruction):
                    if instruction.calls.__contains__("remote"):
                        for stack in instruction.stacks:
                            if retVal not in stack.stack[0].deps:
                                print('DEBUG: ', stack.stack[0].deps)
                                print(instruction.instruction)
                                remoteOffsets.append(instruction)
        
        return remoteOffsets

    def printWarning(getOffset, remotes: list[ins.OpCode]):
        print("The remote calls at line numbers:")
        for r in remotes:
            print(r.instruction.positions.lineno)
        print("are data independent with the get call at line: " + str(getOffset))
        print("You can safely move these remote calls above the get")
        print("For more information on this warning, checkout [LINK]")