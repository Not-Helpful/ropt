#!/usr/bin/env python3

from passes.PassClasses import Pass

class TestPass(Pass):

    name = "Test Pass"

    def run():
        print("Test Pass Entry Point")
