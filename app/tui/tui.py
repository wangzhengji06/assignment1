"""
tui.py

Used for interface creation with blessed
"""

from contextlib import contextmanager

from blessed import Terminal
from __future__ import annotations
from ..actions import Action
from ..render_spec import RenderSpec

__all__ = ['TUI']


class TUI:
    """
    Governs the session of the terminal
    Can read from user input
    Can draw from RenderSpec
    """

    def __init__(self) -> None:
        """
        will initialize the terminal
        """
        self._term = Terminal()

    @contextmanager
    def session(self):
        """
        Full screen context manager
        """
        with self._term.fullscreen(), \
                self._term.cbreak(), self._term.hidden_cursor():
            print(self._term.home + self._term.clear, end="")
            try:
                yield
            finally:
                print(self._term.normal + self._term.clear + self._term.home,
                      end="")

    def read(self, timeout: float = 0.05) -> None | Action | str:
        """
        Return Action, or text.
        """
        k = self._term.inkey(timeout=timeout)
        if not k:
            return None
        if k.is_sequence:
            match k.name:
                case "KEY_UP":
                    return Action.UP
                case "KEY_DOWN":
                    return Action.DOWN
                case "KEY_ENTER" | "KEY_RETURN":
                    return Action.CONFIRM
                case ""




