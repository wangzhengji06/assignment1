from main import BankAccount




def test_backaccount():
    account1 = BankAccount()
    account1.deposit(200)
    assert account1.get_balance() == 200
