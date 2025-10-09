"""
core.py

Implement the app class that deal with action and account.
"""
from __future__ import annotations
from typing import Optional, Tuple
from .context import AppView
from .domain import BankAccount
from .states import State
from .actions import Action
from .render_spec import RenderSpec

__all__ = ["App"]


class App(AppView):
    """
    Used to talk to Action and BankAccount. Leave the tui to state.
    """

    def __init__(self, state: State) -> None:
        self._account = BankAccount()
        self.state = state
        self.state.on_enter()

    @property
    def balance(self) -> int:
        """
        Return the back account balance.
        """
        return self._account.get_balance()

    def format_amount(self) -> str:
        """
        Return a humann-readable amount string.
        """
        return f"Your bank account has {self.balance} left...."

    def deposit(self, amount: int) -> None:
        """
        Apply a deposit.
        """
        self._account.deposit(amount)

    def withdraw(self, amount: int) -> Tuple[bool, Optional[str]]:
        """
        Apply a withdraw.
        """
        self._account.withdraw(amount)

    def render(self) -> RenderSpec:
        return self.state.render()


    def dispatch(self, action: Action) -> None:
        pass

