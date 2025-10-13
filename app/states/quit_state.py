"""
quit_state.py

Define the class of QuitState
quit_state should not do anything on enter
quit_state should not do anything on ui
quit_state should not do anything on text
quit_state should return title, body, should_quit
"""

from ..actions import Action
from ..context import AppView
from ..render_spec import RenderSpec
from .state import State

__all__ = ["QuitState"]


class QuitState(State):
    """
    The class of the quit stage
    """

    def on_enter(self) -> State:
        """
        do nothing dude.
        """
        return self

    def on_ui(self, action: Action, ctx: AppView) -> State:
        """
        do nothing dude.
        """
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
        return RenderSpec(
            title="Quit", body=["Thank you for using it."], should_quit=True
        )
