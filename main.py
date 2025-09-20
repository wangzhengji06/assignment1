from enum import Enum


class BankAccount():
    def __init__(self):
        self._balance = 0


    def deposit(self, amount: int) -> None:
        self._balance += amount

    
    def withdraw(self, amount: int) -> None:
        if self._balance < amount:
            print("Balance not enough")
        else:
            self._balance -= amount 

    
    def get_balance(self) -> int:
        return self._balance 


class Action(Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    GET_BALANCE = "get balance"
    QUIT = "quit"


def ask_amount(prompt: str) -> int:
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
    account1 = BankAccount()
    account1.deposit(300)
    print(account1.get_balance())

    while True:
        action = input("Choose the action among the following options: deposit / withdraw / get balance / quit \n")
        try:
            action_enum = Action(action.strip().lower())
        except ValueError:
            action_enum = None
        match action_enum:
            case Action.DEPOSIT:
                deposit_amount = ask_amount("How much do you want to deposit?\n")
                account1.deposit(int(deposit_amount))
            case Action.WITHDRAW:
                withdraw_amount = ask_amount("How much do you want to withdraw?\n")
                account1.withdraw(int(withdraw_amount))
            case Action.GET_BALANCE:
                print(f"Your current balance is {account1.get_balance()}.\n")
            case Action.QUIT:
                print("Session ended.")
                break
            case _:
                print("Not a valid action.")


if __name__ == "__main__":
    main()

