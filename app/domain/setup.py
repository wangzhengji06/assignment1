from .account import AccountStorage

db = AccountStorage()
db.conn.execute("INSERT INTO accounts (id, pin, balance) VALUES (1234, '4321', 1000)")
db.conn.commit()
