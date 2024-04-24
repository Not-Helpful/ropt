#!/usr/bin/env python3

from abc import ABC, abstractmethod
from include.instructions import OpCode
from include.ControlFlow import BasicBlock


class Pass(ABC):
    """Abstract class to denote that a class is a pass.
    This is required for a class to be discoverable by
    the plugin system."""

    @abstractmethod
    def run():
        """This is the entry point to the pass."""
        pass

class Function():
    name: str
    instructionList: list[OpCode]
    cfg: list[BasicBlock]

    def __init__(self, name, instructionList) -> None:
        self.name = name
        self.instructionList = instructionList
        self.cfg = []


class State():
    functions: list[Function]
    data: dict
    ran: list[Pass]
    stackEffectFuncs: list

    def __init__(self):
        self.data = {}
        self.ran = []
        self.modules = []
        self.stackEffectFuncs = []

    def addData(self, obj):
        if not hasattr(obj, "name"):
            raise(TypeError)
        
        self.data[obj.name] = obj