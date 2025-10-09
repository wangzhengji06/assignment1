"""
state.py

Define the abstract class of state
"""
from abc import ABC, abstractmethod
from ..render_spec import RenderSpec
from ..actions import Action

__all__ = ['State']


class State(ABC):
    """
    The abstract class of the app state
    """

    @abstractmethod
    def on_enter(self) -> None:
        """
        the state's move when newly entered
        """

    @abstractmethod
    def on_ui(self, action: Action) -> None:
        """
        the state's move when a new action is activated
        """

    @abstractmethod
    def on_text(self, text: str) -> None:
        """
        the state's move when a text is provided
        """
    @abstractmethod
    def render(self) -> RenderSpec:
        """
        Render the state's ouput on screen
        """
