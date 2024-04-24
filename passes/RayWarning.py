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
        print("The ray.get call at line: " + str(getOffset) + " has been determined data independent from one or more remote call: ")
        print("ray.get call: \n")

        print('PLACEHOLDER\n')
        # print line
        print("Consider moving the following remote calls above the ray.get to improve parallelism and program execution efficiency.")
        print("For more information visit the Ray documentation: ", end="")
        print("https://docs.ray.io/en/latest/ray-core/tips-for-first-time.html#tip-1-delay-ray-get")
        
        print("remote calls:")
        for r in remotes:
            print(r.instruction.positions.lineno)
            print('PLACEHOLDER\n')
