"""
render_spec.py

Define the elements that the app state should return.
"""

from dataclasses import dataclass, field
from typing import List, Literal, Optional

__all__ = ["RenderSpec", "Status"]


@dataclass
class MenuItem:
    """
    Define the menu items
    """

    label: str
    action_id: str
    disabled: bool = False
    hint: Optional[str] = None


@dataclass
class Menu:
    """
    Define the menu layout
    """

    items: List[MenuItem]
    selected_index: int = 0


@dataclass
class Status:
    """
    Define the status bar shown
    """

    kind: Literal["info", "error", "success"]
    text: str


@dataclass
class RenderSpec:
    """
    The general render spec template to feed into tui.draw
    """

    title: Optional[str] = None
    menu: Optional[Menu] = None
    status: Optional[Status] = None
    footline: Optional[str] = None
    should_quit: bool = False
    body: List[str] = field(default_factory=list)
