"""
main.py

Used to run interative task for the user

"""

from app import App
from app.tui import TUI


def main():
    """
    Will create a app and start tunning
    """
    app = App()
    tui = TUI()
    with tui.session():
        while True:
            spec = app.render()
            tui.draw(spec)
            if spec.should_quit:
                break
            event = tui.read()
            app.dispatch(event)


if __name__ == "__main__":
    main()
