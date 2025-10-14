"""
actions.py

Defines the Action class

menu_state -> UP -> menu_state
menu_state -> DOWN -> menu_state
menu_state -> CONFIRM -> input_state/quit_state
menu_state -> wihdraw/balance -> input_state
menu_state -> QUIT -> quit_state

input_state -> CANCEL -> menu_state
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
    QUIT = auto()
    DEPOSIT = auto()
    WITHDRAW = auto()
    SHOW_BALANCE = auto()
    UP = auto()
    DOWN = auto()
