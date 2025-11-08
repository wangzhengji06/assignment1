"""
account.py

This module is used to define the back account class
"""

import sqlite3
from dataclasses import dataclass
from typing import Optional, Tuple

import bcrypt

__all__ = ["BankAccount", "AccountStorage"]


@dataclass
class BankAccount:
    """
    Dataclass that represents a bank account
    has id, pin, balance
    """

    id: int
    pin: str
    _balance: str

    def __str__(self) -> str:
        return f"BankAccount with {id(self)}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BankAccount):
            return False
        return self._balance == other._balance

    def deposit(self, amount: int) -> None:
        """
        deposits {amount} dollars into the back account
        """
        self._balance += amount

    def withdraw(self, amount: int) -> Tuple[bool, Optional[str]]:
        """
        withdraws {amount} dollars from the back account
        """
        if self._balance < amount:
            return False, "Not enough balance"
        self._balance -= amount
        return True, None

    def get_balance(self) -> int:
        """
        return the balance of the bank account
        """
        return self._balance


class AccountStorage:
    """
    Persistence data storing class
    """

    def __init__(self, db_path: str = "bank.db") -> None:
        """
        create a table called accounts in db_path
        """
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                pin TEXT NOT NULL,
                balance INTEGER NOT NULL DEFAULT 0
            )
        """)
        self.conn.commit()

    def create_account(self, id: int, pin: str, initial_balance: int = 0) -> None:
        """
        Create account with given parameters
        """
        salt = bcrypt.gensalt(rounds=12)
        pin_hash = bcrypt.hashpw(pin.encode("utf-8"), salt).decode("utf-8")
        self.conn.execute(
            "INSERT INTO accounts (id, pin, balance) VALUES (?, ?, ?)",
            (id, pin_hash, initial_balance),
        )
        self.conn.commit()

    def get_account(self, id: int, pin: str) -> Optional[BankAccount]:
        """
        Get the bankaccount stored inside database
        Using id and pin
        """
        cur = self.conn.cursor()
        cur.execute("SELECT id, pin, balance FROM accounts WHERE id=?", (id,))
        row = cur.fetchone()
        if not row:
            return None
        stored_hash = row[1].encode("utf-8")
        if bcrypt.checkpw(pin.encode("utf-8"), stored_hash):
            return BankAccount(id=row[0], pin=pin, _balance=row[2])
        else:
            return None

    def update_balance(self, account: BankAccount) -> None:
        """
        Update the bankaccount after bank account does some crazy stuff
        """
        self.conn.execute(
            "UPDATE accounts SET balance=? WHERE id=?",
            (account.get_balance(), account.id),
        )
        self.conn.commit()

    def close(self) -> None:
        """
        Close the database connection
        """
        self.conn.close()
