"""
tui.py

Used for interface creation with blessed
"""

from __future__ import annotations

from contextlib import contextmanager

from blessed import Terminal

from ..actions import Action
from ..render_spec import RenderSpec

__all__ = ['TUI']


class TUI:
    """
    Governs the session of the terminal
    Can read from user input
    Can draw from RenderSpec
    """

    def __init__(self) -> None:
        """
        will initialize the terminal
        """
        self._term = Terminal()

    @contextmanager
    def session(self):
        """
        Full screen context manager
        """
        with self._term.fullscreen(), \
                self._term.cbreak(), self._term.hidden_cursor():
            print(self._term.move_xy(0, 0) + self._term.clear, end="")
            try:
                yield
            finally:
                print(self._term.clear + self._term.home,
                      end="")

    def read(self, timeout: float = 0.05) -> None | Action | str:
        """
        Return Action, or text.
        """
        k = self._term.inkey(timeout=timeout)
        if not k:
            return None
        if k.is_sequence:
            match k.name:
                case "KEY_UP":
                    return Action.UP
                case "KEY_DOWN":
                    return Action.DOWN
                case "KEY_ENTER" | "KEY_RETURN":
                    return Action.CONFIRM
                case "KEY_ESCAPE":
                    return Action.CANCEL
                case "KEY_BACKSPACE":
                    return "BACKSPACE"
                case _:
                    return None
        ch = str(k)
        match ch.lower():
            case "q":
                return Action.QUIT
            case "d":
                return Action.DEPOSIT
            case "w":
                return Action.WITHDRAW
            case "s":
                return Action.SHOW_BALANCE
            case _ if ch.isdigit():
                return ch
            case _:
                return None

    def draw(self, spec: RenderSpec) -> None:
        """
        Given the render spec, tui would draw
        title menu footline body shouldquit status
        """
        t = self._term
        y = 0
        print(t.clear + t.move_xy(0, y), end="")

        # status
        if spec.status:
            kind = spec.status.kind  # "info" | "error" | "success"
            style = {"info": t.bold, "error": t.bold_red,
                     "success": t.bold_green}.get(kind, t.bold)
            print(t.move_xy(0, y) + style(spec.status.text))
            y += 2

        # title
        if spec.title:
            title = spec.title[: t.width]
            print(t.move_xy(max(0, (t.width - len(title)) // 2), y)
                  + t.bold(title))
            y += 2

        # body lines
        for line in getattr(spec, "body_lines", [])[: max(0, t.height - 3)]:
            print(t.move_xy(2, y) + line[: t.width - 4])
            y += 1

        # menu
        if spec.menu:
            for i, item in enumerate(spec.menu.items):
                prefix = "➤ " if i == spec.menu.selected_index else "  "
                label = f"{item.label}"
                if item.hint:
                    label += f" [{item.hint}]"
                line = prefix + label
                if item.disabled:
                    line = t.color(250)(line)
                elif i == spec.menu.selected_index:
                    line = t.reverse(line)
                print(t.move_xy(2, y) + line[: t.width - 4])
                y += 1

        # footer (bottom row)
        if spec.footline:
            print(t.move_xy(0, t.height - 1)
                  + t.color(250)(spec.footline[: t.width]))
