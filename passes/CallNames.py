#!/usr/bin/env python3

from passes.PassClasses import Pass, State
from include.instructions import CallInstruction

class CallNames(Pass):

    name: str = "internal-call-names"
    export: str = "internal-call-names"
    
    requires = {

    }

    def run(state: State):
        print("Pass for Populating Call Function Names")
        
        for func in state.functions:
            for block in func.cfg:
                for i,ins in enumerate(block.instructions):
                    if isinstance(ins, CallInstruction):
                        dec = (ins.instruction.arg + 1)
                        if not isinstance(block.instructions[i-dec].instruction.argval, str):
                            print(block.instructions[i-dec].instruction)
                            print(i-dec, 'DEBUG')
                        ins.calls = block.instructions[i-dec].instruction.argval
                        
                        print('\n', ins.calls, '\n')



