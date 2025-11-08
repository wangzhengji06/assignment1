"""
login_state.py

Define the initial state of logging in
Two steps:
1. Prompt for id
2. Prompt for PIN
"""

from typing import Optional

from ..actions import Action
from ..context import AppView
from ..render_spec import RenderSpec, Status
from .state import State

__all__ = ["LoginState"]


class LoginState(State):
    """
    The class of Login stage
    """

    def __init__(self, status: Optional[Status] = None) -> None:
        self.stage = "id"
        self.id_buffer = ""
        self.pin_buffer = ""
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
        from .quit_state import QuitState

        match action:
            case Action.QUIT:
                return QuitState()
            case Action.CONFIRM:
                if self.stage == "id":
                    if not self.id_buffer:
                        self.status = Status(kind="error", text="Please enter your id.")
                        return self
                    self.stage = "pin"
                    self.status = Status(kind="info", text="Now enter your pin.")
                    return self
                elif self.stage == "pin":
                    try:
                        id = int(self.id_buffer)
                    except ValueError:
                        self.status = Status(kind="error", text="Not a valid ID.")
                        self.stage = "id"
                        self.id_buffer = ""
                        self.pin_buffer = ""
                        return self

                    ok = ctx.login(id, self.pin_buffer)
                    if ok:
                        return MenuState()
                    else:
                        self.status = Status(kind="error", text="Wrong PIN or ID.")
                        self.stage = "id"
                        self.id_buffer = ""
                        self.pin_buffer = ""
                        return self
        return self

    def on_text(self, text: str, ctx: AppView) -> State:
        """
        append the text to id_buffer, pin_buffer
        depneds on stage
        """
        if self.stage == "id":
            if text.isdigit():
                self.id_buffer += text
                self.status = Status("info", "Inputting....")
            elif text == "BACKSPACE":
                self.id_buffer = self.id_buffer[:-1]
            else:
                self.status = Status("error", "Not valid amount")
        elif self.stage == "pin":
            if text.isdigit():
                self.pin_buffer += text
                self.status = Status("info", "Inputting....")
            elif text == "BACKSPACE":
                self.pin_buffer = self.pin_buffer[:-1]
            else:
                self.status = Status("error", "Not valid amount")
        return self

    def render(self, ctx: AppView) -> RenderSpec:
        """
        Return the title as Bank Login
        Return the current buffer in bodyline
        Return a footer shows the hint for current stage
        """
        masked_pin = "*" * len(self.pin_buffer)
        id_line = f"id: {self.id_buffer}"
        pin_line = f"pin: {masked_pin if self.stage == 'pin' else ''}"
        footline = (
            "Enter ID • Press Enter"
            if self.stage == "id"
            else "Enter PIN • Press Enter to Confirm"
        )

        return RenderSpec(
            title="Bank Login",
            body=[id_line, pin_line],
            status=self.status,
            footline=footline,
        )
