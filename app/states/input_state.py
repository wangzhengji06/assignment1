"""
input_state.py

Define the class of InputAmountState and InputCurrencyState
input_state should not do anything on enter
input_state should append digit and deal with error
input_state should handle only cancel and confirm
"""

from typing import Optional

from ..actions import Action
from ..context import AppView
from ..render_spec import RenderSpec, Status
from .state import State

__all__ = ["InputAmountState", "InputCurrencyState"]


class InputAmountState(State):
    """
    The class of input amount stage
    """

    def __init__(self, kind: str, status: Optional[Status] = None) -> None:
        self.kind = kind
        self.buffer = ""
        self.status = status

    def on_enter(self) -> State:
        """
        do nothing dude
        """
        return self

    def on_ui(self, action: Action, ctx: AppView) -> State:
        """
        the state's move when a new action is activated
        """
        from .menu_state import MenuState

        match action:
            case Action.CANCEL:
                return MenuState()
            case Action.CONFIRM:
                if not self.buffer or not self.buffer.isdigit():
                    self.status = Status("error", "Not allowed input")
                    return self

                amount = int(self.buffer)

                if self.kind == "deposit":
                    ctx.deposit(amount)
                    return MenuState(
                        status=Status(
                            "success", f"Depoisit {ctx.format_amount(amount)}."
                        )
                    )

                if self.kind == "withdraw":
                    ok, err = ctx.withdraw(amount)
                    if ok:
                        return MenuState(
                            status=Status(
                                "success", f"Withdraw {ctx.format_amount(amount)}."
                            )
                        )
                    return MenuState(status=Status("error", err))

    def on_text(self, text: str, ctx: AppView) -> State:
        """
        append the text to buffer
        """
        if text.isdigit():
            self.buffer += text
            self.status = Status("info", "Inputting....")
        elif text == "BACKSPACE":
            self.buffer = self.buffer[:-1]
        else:
            self.status = Status("error", "Not valid Amount")
        return self

    def render(self, ctx: AppView) -> RenderSpec:
        """
        Return the current kind
        Return the current buffer in bodyline
        Show the current status
        Return a footer shows the hint for confirm and cancel
        """
        return RenderSpec(
            title=f"{'Deposit' if self.kind == 'deposit' else 'Withdraw'}",
            body=[
                f"Input: {self.buffer or '(empty)'}",
            ],
            status=self.status,
            footline="Enter to confirm / Esc to escape",
        )


class InputCurrecyState(State):
    """
    The class of input currency stage
    """

    def __init__(self, kind: str, status: Optional[Status] = None) -> None:
        self.kind = kind
        self.buffer = ""
        self.status = status

    def on_enter(self) -> State:
        """
        do nothing dude
        """
        return self

    def on_ui(self, action: Action, ctx: AppView) -> State:
        """
        the state's move when a new action is activated
        """
        from .menu_state import MenuState

        match action:
            case Action.CANCEL:
                return MenuState()
            case Action.CONFIRM:
                if not self.buffer or not self.buffer.isalpha():
                    self.status = Status("error", "Not allowed input")
                    return self

                CUR = int(self.buffer)

                if self.kind == "deposit":
                    ctx.deposit(amount)
                    return MenuState(
                        status=Status(
                            "success", f"Depoisit {ctx.format_amount(amount)}."
                        )
                    )

                if self.kind == "withdraw":
                    ok, err = ctx.withdraw(amount)
                    if ok:
                        return MenuState(
                            status=Status(
                                "success", f"Withdraw {ctx.format_amount(amount)}."
                            )
                        )
                    return MenuState(status=Status("error", err))

    def on_text(self, text: str, ctx: AppView) -> State:
        """
        append the text to buffer
        """
        if text.isdigit():
            self.buffer += text
            self.status = Status("info", "Inputting....")
        elif text == "BACKSPACE":
            self.buffer = self.buffer[:-1]
        else:
            self.status = Status("error", "Not valid Amount")
        return self

    def render(self, ctx: AppView) -> RenderSpec:
        """
        Return the current kind
        Return the current buffer in bodyline
        Show the current status
        Return a footer shows the hint for confirm and cancel
        """
        return RenderSpec(
            title=f"{'Deposit' if self.kind == 'deposit' else 'Withdraw'}",
            body=[
                f"Input: {self.buffer or '(empty)'}",
            ],
            status=self.status,
            footline="Enter to confirm / Esc to escape",
        )
