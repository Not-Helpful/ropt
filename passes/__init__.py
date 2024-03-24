#!/usr/bin/env python3
import inspect
from passes.PassClasses import Pass
import importlib

passlist = []

# https://stackoverflow.com/questions/73186008/how-to-list-all-classes-and-methods-functions-in-a-package-with-a-full-folder
def recusive_module_search(module):
    members = inspect.getmembers(module)

    for name, member in members:
        if inspect.ismodule(member):
            # Dont go too deep :)
            if member is module:
                recusive_module_search(member)
        elif inspect.isfunction(member):
            pass
        elif inspect.isclass(member):
            if issubclass(member, Pass) and not inspect.isabstract(member):
                #file = inspect.getfile(member)
                # TODO: Convert to logging statement
                #print(file, function_signature_string(member), "class")
                passlist.append(member)


def function_signature_string(member):
    parameters = inspect.signature(member).parameters
    return member.__name__ + "(" + ', '.join(str(x) for x in parameters.values()) + ")"


# https://stackoverflow.com/questions/1057431/how-to-load-all-modules-in-a-folder
from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]



for module in __all__:
    recusive_module_search(importlib.import_module("passes." + module))
