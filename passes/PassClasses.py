#!/usr/bin/env python3

from abc import ABC, abstractmethod


class Pass(ABC):
    """Abstract class to denote that a class is a pass.
    This is required for a class to be discoverable by
    the plugin system."""

    @abstractmethod
    def run():
        """This is the entry point to the pass."""
        pass

class PassData(ABC):
    
    @abstractmethod
    def run():
        pass

class Module(ABC):
    def __init__():
        pass

    def getByteCode():
        pass

class State():
    modules: list[Module]
    data: dict
    ran: list[Pass]

    def __init__(self):
        self.data = {}
        self.ran = []
        self.modules = []

    def addData(self, obj):
        if not hasattr(obj, "name"):
            raise(TypeError)
        
        self.data[obj.name] = obj