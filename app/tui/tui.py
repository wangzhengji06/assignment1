"""
tui.py

Used for interface creation with blessed
"""

from enum import Enum
from blessed import Terminal
from ..actions import Action

_term = Terminal()


def show_menus() -> Action:
    """
    This function takes Action enum class and output the options.
    Would return Action to pass for the next step
    """
