"""
main.py

Used to run interative task for the user

"""

from app import App
from app.tui import TUI


def main():
    app = App()
    tui = TUI()
    event = None

    with tui.session():
        spec0 = app.render()
        tui.draw(spec0)

        while True:
            app.dispatch(event)
            spec = app.render()
            tui.draw(spec)
            if spec.should_quit:
                break
            event = tui.read()


if __name__ == "__main__":
    main()
