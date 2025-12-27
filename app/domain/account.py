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
    DataClass that defines the BankAccount.
    has pin, id, _balance.
    """

    id: int
    pin: str
    _balance: int

    def deposit(self, amount: int) -> None:
        """
        Add the amount to the _balance field.
        """
        self._balance += amount

    def withdraw(self, amount: int) -> Tuple[bool, Optional[str]]:
        """
        Returns (True, None) if withdraw is succeeded.
        Otherwise Return (False, "not enought balance")
        """
        if self._balance < amount:
            return False, "Not enough balance"
        self._balance -= amount
        return True, None

    def get_balance(self) -> int:
        """
        Return the balance Field of the BankAccount.
        """
        return self._balance


class AccountStorage:
    """
    Persistent data stroage class
    """

    def __init__(self, db_path: str = "bank.db") -> None:
        """
        Create a database in db_path.
        Will try to create table accounts if not existed.
        """
        self.db_path = db_path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        """
        Tried to establish a connection with the sqlite database.
        """
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        """
        Try to create table if not exists.
        """
        conn = self._connect()
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY,
                    pin TEXT NOT NULL,
                    balance INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            conn.commit()
        finally:
            conn.close()

    def create_account(self, id: int, pin: str, initial_balance: int = 0) -> None:
        """
        Create an account given id, pin, and initial_balance, by default the balance would be 0.
        """
        salt = bcrypt.gensalt(rounds=12)
        pin_hash = bcrypt.hashpw(pin.encode("utf-8"), salt).decode("utf-8")

        conn = self._connect()
        try:
            conn.execute(
                "INSERT INTO accounts (id, pin, balance) VALUES (?, ?, ?)",
                (id, pin_hash, initial_balance),
            )
            conn.commit()
        finally:
            conn.close()

    def get_account(self, id: int, pin: str) -> Optional[BankAccount]:
        """
        Get an account by using id and pin.
        """
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, pin, balance FROM accounts WHERE id=?", (id,))
            row = cur.fetchone()
            if not row:
                return None

            stored_hash = row[1].encode("utf-8")
            if not bcrypt.checkpw(pin.encode("utf-8"), stored_hash):
                return None

            return BankAccount(id=row[0], pin=pin, _balance=int(row[2]))
        finally:
            conn.close()

    def get_account_by_id(self, id: int) -> Optional[BankAccount]:
        """
        Needed for GET /accounts/{id} without auth.
        """
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, balance FROM accounts WHERE id=?", (id,))
            row = cur.fetchone()
            if not row:
                return None
            return BankAccount(id=row[0], pin="", _balance=int(row[1]))
        finally:
            conn.close()

    def update_balance(self, account: BankAccount) -> None:
        """
        Update the balance in the database using the current account state.
        """
        conn = self._connect()
        try:
            conn.execute(
                "UPDATE accounts SET balance=? WHERE id=?",
                (account.get_balance(), account.id),
            )
            conn.commit()
        finally:
            conn.close()
