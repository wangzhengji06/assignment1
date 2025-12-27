"""
core.py

Implement the app class that deal with action and account.
"""

from __future__ import annotations

from .actions import Action
from .context import AppView
from .domain import AccountStorage
from .network import get_exchange_rates
from .render_spec import RenderSpec
from .states import LoginState

__all__ = ["App"]


class App(AppView):
    """
    Used to talk to Action and BankAccount. Leave the tui to state.
    """

    def __init__(self) -> None:
        self.storage = AccountStorage()
        self._account = None
        self.state = LoginState()
        self.state.on_enter()

    def login(self, id: int, pin: str) -> bool:
        """
        Login using the database.
        If login failed, return False.
        """
        acct = self.storage.get_account(id, pin)
        if not acct:
            return False
        self._account = acct
        return True

    def logout(self) -> None:
        self._account = None

    @property
    def balance(self) -> int:
        """
        Return the back account balance.
        """
        return self._account.get_balance() if self._account else 0

    def format_amount(self, amount: int) -> str:
        """
        Return a human-readable amount string.
        """
        return f"{amount}$"

    def deposit(self, amount: int) -> None:
        """
        Apply a deposit.
        """
        self._require_login()
        self._account.deposit(amount)
        self.storage.update_balance(self._account)

    def withdraw(self, amount: int) -> None:
        """
        Apply a withdraw.
        """
        self._require_login()
        ok, err = self._account.withdraw(amount)
        if ok:
            self.storage.update_balance(self._account)
        return ok, err

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

    def _require_login(self) -> None:
        """
        Needs login to perform
        """
        if self._account is None:
            raise RuntimeError("Log in first.")

    def convert_balance_to(self, target: str) -> tuple[bool, str]:
        """
        Try to convert the currency to target currency.
        Returns ok if target is valid.
        """
        base = "USD"
        ok, rates, err = get_exchange_rates(base=base, timeout=5.0)
        if not ok and rates is None:
            return False, (err or "Network unavailable")
        rate_map = rates if rates else {}
        rate = rate_map.get(target.upper())
        if rate is None:
            return False, "Invalid or unsupported currency code"

        converted = self.balance * rate
        return (
            True,
            f"{self.format_amount(self.balance)} → {target.upper()} {converted:,.2f}",
        )
