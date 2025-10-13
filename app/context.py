"""
context.py

Provide property for state to use
"""
from __future__ import annotations
from typing import Protocol, Optional, Tuple

__all__ = ["AppView"]


class AppView(Protocol):
    """
    Used to expose runtime information to state of the core
    """
    @property
    def balance(self) -> int:
        """
        Return the back account balance.
        """

    def format_amount(self, amount: int) -> str:
        """
        Return a humann-readable amount string.
        """

    def deposit(self, amount: int) -> None:
        """
        Apply a deposit.
        """

    def withdraw(self, amount: int) -> Tuple[bool, Optional[str]]:
        """
        Apply a withdraw.
        """
