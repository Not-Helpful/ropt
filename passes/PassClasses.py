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
