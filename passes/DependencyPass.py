from passes.PassClasses import Pass, State, Function
import include.instructions as ins

deps = {}

# https://www.geeksforgeeks.org/python-union-two-lists/
def Union(lst1, lst2):
    lst1 = list(dict.fromkeys(lst1))
    lst2 = list(dict.fromkeys(lst2))
    final_list = list(set(lst1) | set(lst2))
    return final_list

class DependencyPass(Pass):

    name: str = "analysis-dependency"
    export: str = "analysis-dependency"
    
    requires = {
        
    }

    def run(state: State):
        state.stackEffectFuncs.append(DependencyPass.dependencyEffect)

    def dependencyEffect(stack: ins.Stack, opcode: ins.OpCode, pushVals: list[ins.StackObject], popVals: list[ins.StackObject]):

        if isinstance(opcode, ins.StoreInstruction):
            if popVals[0].name not in popVals[0].deps:
                popVals[0].deps.append(popVals[0].name)
        elif len(pushVals) == 0 or len(popVals) == 0:
            return
        elif isinstance(opcode, ins.BinarySubInstruction) and isinstance(popVals[0], int):
            return
        else:
            for popVal in popVals:
                pushVals[0].deps = Union(pushVals[0].deps, popVal.deps)
            
                





        # process variable names to strip '.___' from attribute/method calls and grab the object as a dependency
        # pop_jump_if --> if statement --> instructions inside are dependent on this statement --> assign offset movement limiter
        # for loops --> collect dependencies of loop internal and any external dependencies. These may all be moved further up as an optimization
        # list_append, list_extend and store all pop values that affect the depency list of the argument