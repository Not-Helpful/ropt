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
                            if block.instructions[-1].instruction.opname == "JUMP_BACKWARD":
                                offset = block.instructions[-1].instruction.argval
                            else:
                                offset = instruction.instruction.offset
                            retVal = 'GLOBAL_NULL + ray_get_RETURN$' + str(instruction.instruction.offset)
                            # We scan ahead for all remote calls
                            remotes = RayWarning.checkForRemotes(func.cfg, offset, retVal)
                            if remotes:
                                RayWarning.printWarning(instruction.instruction.positions.lineno, remotes, state.source)

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
                                if instruction not in remoteOffsets:
                                    remoteOffsets.append(instruction)
        
        return remoteOffsets

    def printWarning(getOffset, remotes: list[ins.OpCode], source):
        remotesInLoop = []
        Lines = []

        for r in remotes:
            if r.instruction.positions.lineno < getOffset:
                remotesInLoop.append(r)
                remotes.remove(r)

        file1 = open(source, 'r')
        Lines = file1.readlines()

        print("\nThe ray.get call at line: " + str(getOffset) + " has been determined \ndata independent from one or more remote calls: ")
        print("ray.get call: \n")

        print("\n")
        for i in range(7):
            print('\t', ((getOffset-3)+i), ':\t', Lines[(getOffset - 3) + i], end='')
        # print line
        print('\n')

        if remotes:
            print("Consider moving the following remote call(s) above the ray.get \nto improve parallelism and program execution efficiency.")
        
            print("remote calls:")
            for r in remotes:
                print("\n")
                for i in range(7):
                    print('\t', ((r.instruction.positions.lineno-3)+i), ':\t', Lines[(r.instruction.positions.lineno - 3) + i], end='')
                print("\n")
        if remotesInLoop:
            print("\nConsider moving the ray.get call out of the loop \nto improve parallelism and program execution efficiency.\n")

        print("For more information visit the Ray documentation: ", end="")
        print("\nhttps://docs.ray.io/en/latest/ray-core/tips-for-first-time.html#tip-1-delay-ray-get")

