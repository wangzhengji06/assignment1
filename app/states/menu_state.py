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
        the state's move when a new action is activated
        """
        from .input_state import InputAmountState
        from .quit_state import QuitState
        match action:
            case Action.UP:
                self.selected_index = (self.selected_index - 1) % 4
            case Action.DOWN:
                self.selected_index = (self.selected_index + 1) % 4
            case Action.CONFIRM:
                choice = ["DEPOSIT", "WITHDRAW", "SHOW_BALANCE", "QUIT"][
                    self.selected_index
                ]
                if choice == "WITHDRAW" and ctx.balance <= 0:
                    self.status = Status(
                        kind="error",
                        text="No funds to withdraw")
                    return self
                match choice:
                    case "SHOW_BALANCE":
                        amt = ctx.format_amount(ctx.balance)
                        self.status = Status(
                            kind="info",
                            text=f"You have\
 {amt} left.",
                        )
                    case "DEPOSIT":
                        return InputAmountState(kind="deposit")
                    case "WITHDRAW":
                        return InputAmountState(kind="withdraw")
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
