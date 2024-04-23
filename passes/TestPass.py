#!/usr/bin/env python3

from passes.PassClasses import Pass, State
from passes.data import cfg

class TestPass(Pass):

    name = "t"
    
    requires = {
        "Control Flow Graph"
    }

    def run(state: State):
        print("Test Pass Entry Point")
        controlflow: cfg = state.data[cfg.name]


