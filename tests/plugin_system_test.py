#!/usr/bin/env python3

import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from passes import passlist
import pytest


def test_passlist_exists():
    assert(isinstance(passlist, list))

def test_TestPass_is_in_passlist():
    from passes.TestPass import TestPass
    assert(TestPass in passlist)

def test_AbstractPass_is_not_in_passlist():
    from passes.PassClasses import Pass
    assert(Pass not in passlist)
