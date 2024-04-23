from passes.PassClasses import Pass, State, Function

deps = {}

class DependencyPass(Pass):

    name: str = "internal-dependency-pass"
    export: str = "internal-dependency-pass"
    
    requires = {
        "internal-stack-pass"
    }

    def run(state: State):
        funcList: list[Function] = state.functions

        for func in funcList:
            for block in func.cfg:
                for ins in block.instructions:
                    if ins.instruction.opname.__contains__("LOAD"):
                        pass
                    # process variable names to strip '.___' from attribute/method calls and grab the object as a dependency
                    # pop_jump_if --> if statement --> instructions inside are dependent on this statement --> assign offset movement limiter
                    # for loops --> collect dependencies of loop internal and any external dependencies. These may all be moved further up as an optimization
                    # list_append, list_extend and store all pop values that affect the depency list of the argument