"""
main.py

Used to run interative task for the user

"""

from abc import ABC, abstractmethod

import app.action as action
import app.domain as domain

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
    1. Create a back account
    2. Deposit 300 in it
    3. Ask the user to choose action
    4. Execute the action
    """
    account1 = domain.BankAccount()
    account1.deposit(300)
    print(account1.get_balance())

    while True:
        action = input(
            "Choose the action among the following options:\
        deposit / withdraw / get balance / quit \n"
        )
        try:
            action_enum = Action(action.strip().lower())
        except ValueError:
            action_enum = None
        match action_enum:
            case Action.DEPOSIT:
                deposit_amount = ask_amount(
                    "How much\
                do you want to deposit?\n"
                )
                account1.deposit(int(deposit_amount))
            case Action.WITHDRAW:
                withdraw_amount = ask_amount(
                    "How much\
                do you want to withdraw?\n"
                )
                try:
                    account1.withdraw(int(withdraw_amount))
                except ValueError as e:
                    print(f"Error message: {e}.")
            case Action.GET_BALANCE:
                print(f"Your current balance is {account1.get_balance()}.\n")
            case Action.QUIT:
                print("Session ended.")
                break
            case _:
                print("Not a valid action.")


if __name__ == "__main__":
    main()
