"""
test_backaccount.py

Used to implement pytest
"""

from app import domain


def test_backaccount_deposit():
    """
    Creates a back account and deposits 200 dollars in it.
    """
    account1 = domain.BankAccount()
    account1.deposit(200)
    assert account1.get_balance() == 200


def test_backaccount_withdraw():
    """
    Creates a bank account and withdraw 100 dollars from it.
    """
    account1 = domain.BankAccount()
    account1.deposit(300)
    account1.withdraw(200)
    assert account1.get_balance() == 100


def test_backaccount_withdraw_toomuch():
    """
    Creates a back account withdraing too much that trigger the error.
    """
    account1 = domain.BankAccount()
    account1.deposit(200)
    account1.withdraw(300)
    assert account1.get_balance() == 200
