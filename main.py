import os
import subprocess
import sys
from colorama import init, Fore, Back, Style
import time
from threading import Thread
import sqlite3

init()


def start_process(x):
    while True:
        process = subprocess.Popen([sys.executable, "bot_V2.py", str(x)])
        process.wait()


input("Нажми Enter чтобы запустить...")
# process = subprocess.Popen([sys.executable, "bot_V2.py", str(0) + ' ' + str(10) + ' ' + str(3)])
# process.wait()
db = sqlite3.connect('Account.db')
cur = db.cursor()
n = [x[0] for x in cur.execute("Select ID from Account").fetchall()][-1]
db.close()
for i in range(1):
    thread = Thread(target=start_process, args=(i + 1,))
    thread.start()
    time.sleep(1)
