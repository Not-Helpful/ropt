from passes.PassClasses import Pass, State, Function
import include.instructions as ins
def prettyPrint(obj):
    if isinstance(obj, dict):
        for v in obj.keys():
            print(v, ": ", end="")
            prettyPrint(obj[v])
    if isinstance(obj, ins.StackObject):
        print(obj.deps)




class StackTestPass(Pass):

    name: str = "test-stack-pass"
    export: str = "test-stack-pass"
    
    requires = {
        "internal-stack-pass"
    }

    def run(state: State):
        funcList: list[Function] = state.functions
        for func in funcList:
            print('\n', func.name, ": ")
            for block in func.cfg:
                for instruction in block.instructions:
                    print(instruction.instruction.opname," ", instruction.instruction.offset, ": ")
                    for stack in instruction.stacks:
                        #print("[",end="")
                        #for stackobj in stack.stack:
                        #    prettyPrint(stackobj)
                        #print("]")
                        prettyPrint(stack.var_store)
                        print('\n')