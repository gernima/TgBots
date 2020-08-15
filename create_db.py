import sqlite3

db = sqlite3.connect('Account.db')
cur = db.cursor()
    # Создаем таблицу
cur.execute("""CREATE TABLE IF NOT EXISTS Account (
    ID INTEGER PRIMARY KEY,
    PHONE TEXT,
    PASS TEXT,
    API_ID TEXT,
    API_HASH TEXT,
    ACTIVITY TEXT,
    LITECOIN TEXT,
    DEVICE TEXT
)""")

db.commit()

Phone = "+79819812465"
password = "ПС110720"
Api_id = "1684499"
Api_hash = "8b35f33c88dc2bb2fd253b04aaffad34"
Activity = "ON"
Litecoin = ""
DEVICE = 'Windows NT 10.0'

cur.execute(f"SELECT PHONE FROM Account WHERE PHONE = '{Phone}'")
if cur.fetchone() is None:
    cur.execute("""INSERT INTO Account(PHONE, PASS, API_ID, API_HASH, ACTIVITY, LITECOIN, DEVICE) VALUES (?,?,?,?,?,?,?);""",
                (Phone, password, Api_id, Api_hash, Activity, Litecoin, DEVICE))
    db.commit()
    print("Зарегистрированно!")
    # for value in cur.execute("SELECT * FROM Account"):
    #     print(value)
