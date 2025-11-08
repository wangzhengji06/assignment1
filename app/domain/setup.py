from .account import AccountStorage

db = AccountStorage()
db.create_account(1234, "4321", 1000)
