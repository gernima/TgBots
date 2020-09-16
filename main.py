import os
import subprocess
import sys
from colorama import init, Fore, Back, Style
import time
from threading import Thread, Lock
import sqlite3
from sys import argv

init()


def start_process(x):
    while True:
        process = subprocess.Popen([sys.executable, "bot_V2.py", str(x), dict_db[x]["PHONE"], dict_db[x]["PASS"],
                                    dict_db[x]["API_ID"], dict_db[x]["API_HASH"], dict_db[x]["LITECOIN"], dict_db[x]["DEVICE"]])
        process.wait()


def get_data_from_db():
    try:
        lock.acquire(True)
        a = {}
        b = cur.execute("Select ID from Account").fetchall()
        a['len'] = len(b)
        for i in b:
            i = i[0]
            if cur.execute(f"""Select ACTIVITY from Account WHERE ID = '{i}'""").fetchone()[0].strip() == "ON":
                a[i] = {'PHONE': '', 'PASS': '', 'API_ID': '', 'API_HASH': '', 'LITECOIN': '', 'DEVICE': ''}
                a[i]['PHONE'] = cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{i}'").fetchone()[0]
                a[i]['PASS'] = cur.execute(f"SELECT PASS FROM Account WHERE ID = '{i}'").fetchone()[0]
                a[i]['API_ID'] = cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{i}'").fetchone()[0]
                a[i]['API_HASH'] = cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{i}'").fetchone()[0]
                a[i]['LITECOIN'] = cur.execute(f"SELECT LITECOIN FROM Account WHERE ID = '{i}'").fetchone()[0]
                a[i]['DEVICE'] = cur.execute(f"SELECT DEVICE FROM Account WHERE ID = '{i}'").fetchone()[0]
                a[i]["BALANCE"] = float()
        return a
    finally:
        lock.release()


lock = Lock()
db = sqlite3.connect('Account.db')
cur = db.cursor()
dict_db = get_data_from_db()
input("Нажми Enter чтобы запустить...")
# process = subprocess.Popen([sys.executable, "bot_V2.py", str(0) + ' ' + str(10) + ' ' + str(3)])
# process.wait()
# db = sqlite3.connect('Account.db')
# cur = db.cursor()
# n = [x[0] for x in cur.execute("Select ID from Account").fetchall()][-1]
# db.close()
from_n = int(argv[1]) - 1
to_n = int(argv[2])
# from_n = 1 - 1
# to_n = 6
print(f"Start bots from {from_n} to {to_n}")
for i in range(from_n, to_n):
    # print(i)
    thread = Thread(target=start_process, args=(i + 1,))
    thread.start()
    time.sleep(1)
