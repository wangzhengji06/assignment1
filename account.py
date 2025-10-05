"""
account.py

This module is used to define the back account class
"""


class BankAccount():

    """
    class that represents a bank account
    """

    def __init__(self):
        self._balance = 0

    def deposit(self, amount: int) -> None:
        """
        deposits {amount} dollars into the back account
        """
        self._balance += amount

    def withdraw(self, amount: int) -> None:
        """
        withdraws {amount} dollars from the back account
        """
        if self._balance < amount:
            raise ValueError("Not enough balance")
        self._balance -= amount

    def get_balance(self) -> int:
        """
        return the balance of the bank account
        """
        return self._balance
