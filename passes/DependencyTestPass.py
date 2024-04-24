from passes.PassClasses import Pass, State, Function

class DependencyTestPass(Pass):

    name: str = "test-dependency-pass"
    export: str = "test-dependency-pass"
    
    requires = {
        "analysis-dependency",
        "internal-stack-pass"
    }

    def run(state: State):
        funcList: list[Function] = state.functions
        for func in funcList:
            print('\n', func.name, ": ")
            for block in func.cfg:
                for ins in block.instructions:
                    print(ins.instruction.opname, ": ")
                    for stack in ins.stacks:
                        print("[",end="")
                        for stackobj in stack.stack:
                            print(stackobj.name, end=', ')
                        print("]", end="")
                        print('\n')