"""
test_backaccount.py

Used to implement pytest
"""


from account import BankAccount


def test_backaccount():
    """
    Creates a back account and deposits 200 dollars in it.
    """
    account1 = BankAccount()
    account1.deposit(200)
    assert account1.get_balance() == 200
