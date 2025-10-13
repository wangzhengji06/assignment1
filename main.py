"""
main.py

Used to run interative task for the user

"""

import app
from app import domain
from app import App


def ask_amount(prompt: str) -> int:
    """
    takes in the amount prompt from customer.
    will try to transfer the prompt into a positive integer,
    otherwise asks the user to try again.
    """
    while True:
        raw = input(prompt)
        try:
            amount = int(raw)
            if amount <= 0:
                print("Please enter a positive amount.")
                continue
            return amount
        except ValueError:
            print("Invalid number, please try again.")


def main():
    """
    Will create a app and start tunning
    """
    app = App()
    
    with _.session():
        while True:
            spec = app.render()
            tui.draw(spec)


if __name__ == "__main__":
    main()
