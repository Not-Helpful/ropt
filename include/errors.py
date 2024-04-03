#!/usr/bin/env python3
class JumpInstructionIsNotLastInstruction(Exception):
    def __init__(self, message, instruction, basicblock):
        super().__init__(message)
