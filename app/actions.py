"""
actions.py

Defines the Action class
"""

from enum import Enum, auto

__all__ = ["Action"]


class Action(Enum):
    """
    Used to represent the action read by the tui from user input.
    The action will be sent to main logic.
    """
    CONFIRM = auto()
    CANCEL = auto()
    SUBMIT_AMOUNT = auto()
    QUIT = auto()
    DEPOSIT = auto()
    WITHDRAW = auto()
    SHOW_BALANCE = auto()
    UP = auto()
    DOWN = auto()
