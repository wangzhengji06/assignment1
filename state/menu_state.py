"""
menu_state.py

Define the class of MenuState
"""
from app.render_spec import RenderSpec
from action import Action
from .state import State


class MenuState(State):
    """
    The class of the menu selection stage
    """

    def on_enter(self) -> None:
        """
        the state's move when newly entered
        """

    def on_ui(self, action: Action) -> State:
        """
        the state's move when a new action is activated
        """

    def on_text(self, text: str) -> None:
        """
        the state's move when a text is provided
        """

    def render(self) -> RenderSpec:
        """
        Render the state's ouput on screen
        """
