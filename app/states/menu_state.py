"""
menu_state.py

Define the class of MenuState
menu_state should not do anything on enter
menu_state should not do anything on text
menu_state should change status on ui
"""

from typing import Optional

from ..actions import Action
from ..context import AppView
from ..render_spec import Menu, MenuItem, RenderSpec, Status
from .state import State

__all__ = ["MenuState"]


class MenuState(State):
    """
    The class of the menu selection stage
    """

    def __init__(self, status: Optional[Status] = None) -> None:
        self.selected_index = 0
        self.status = status

    def on_enter(self) -> State:
        """
        Do nothing dude.
        """
        return self

    def on_ui(self, action: Action, ctx: AppView) -> State:
        """
        Handle state transition when a new action is activated.
        """
        from .input_state import InputAmountState
        from .quit_state import QuitState

        menu = ("DEPOSIT", "WITHDRAW", "SHOW_BALANCE", "QUIT")
        no_funds_msg = "No funds to withdraw"

        def show_balance():
            amt = ctx.format_amount(ctx.balance)
            self.status = Status(kind="info", text=f"You have {amt} left.")

        def ensure_funds() -> bool:
            if ctx.balance <= 0:
                self.status = Status(kind="error", text=no_funds_msg)
                return False
            return True

        match action:
            case Action.UP:
                self.selected_index = (self.selected_index - 1) % len(menu)
            case Action.DOWN:
                self.selected_index = (self.selected_index + 1) % len(menu)

            case Action.DEPOSIT:
                return InputAmountState(kind="deposit")

            case Action.WITHDRAW:
                if ensure_funds():
                    return InputAmountState(kind="withdraw")

            case Action.SHOW_BALANCE:
                show_balance()

            case Action.CONFIRM:
                choice = menu[self.selected_index]
                match choice:
                    case "DEPOSIT":
                        return InputAmountState(kind="deposit")
                    case "WITHDRAW":
                        if ensure_funds():
                            return InputAmountState(kind="withdraw")
                    case "SHOW_BALANCE":
                        show_balance()
                    case "QUIT":
                        return QuitState()

        return self

    def on_text(self, text: str, ctx: AppView) -> State:
        """
        do nothing dude.
        """
        return self

    def render(self, ctx: AppView) -> RenderSpec:
        """
        Render the state's ouput on screen
        """
        disabled = ctx.balance <= 0
        items = [
            MenuItem("Deposit", "DEPOSIT"),
            MenuItem("Withdraw", "WITHDRAW", disabled),
            MenuItem("Show Balance", "SHOW_BALANCE"),
            MenuItem("Quit", "QUIT"),
        ]
        return RenderSpec(
            title="Bank Account",
            menu=Menu(items=items, selected_index=self.selected_index),
            status=self.status,
            footline="↑/↓ select • Enter confirm • Q quit",
        )
