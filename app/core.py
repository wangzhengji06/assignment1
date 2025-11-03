"""
core.py

Implement the app class that deal with action and account.
"""

from __future__ import annotations

from .actions import Action
from .context import AppView
from .domain import BankAccount
from .render_spec import RenderSpec
from .states import MenuState

__all__ = ["App"]


class App(AppView):
    """
    Used to talk to Action and BankAccount. Leave the tui to state.
    """

    def __init__(self) -> None:
        self._account = BankAccount()
        self.state = MenuState()
        self.state.on_enter()

    @property
    def balance(self) -> int:
        """
        Return the back account balance.
        """
        return self._account.get_balance()

    def format_amount(self, amount: int) -> str:
        """
        Return a humann-readable amount string.
        """
        return f"{amount}$"

    def deposit(self, amount: int) -> None:
        """
        Apply a deposit.
        """
        self._account.deposit(amount)

    def withdraw(self, amount: int) -> None:
        """
        Apply a withdraw.
        """
        self._account.withdraw(amount)

    def render(self) -> RenderSpec:
        """
        Given the current app state, render something.
        """
        return self.state.render(self)

    def dispatch(self, event: Action | str) -> None:
        """
        Call state based on Action or text.
        """
        if event is None:
            return
        if isinstance(event, str):
            next_state = self.state.on_text(event, self)
        elif isinstance(event, Action):
            next_state = self.state.on_ui(event, self)
        else:
            return
        self.state = next_state
