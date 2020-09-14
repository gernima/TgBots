import os
import subprocess
import sys
from colorama import init, Fore, Back, Style
import time
from threading import Thread
import sqlite3
from sys import argv

init()


def start_process(x):
    while True:
        process = subprocess.Popen([sys.executable, "bot_V2.py", str(x)])
        process.wait()


input("Нажми Enter чтобы запустить...")
# process = subprocess.Popen([sys.executable, "bot_V2.py", str(0) + ' ' + str(10) + ' ' + str(3)])
# process.wait()
# db = sqlite3.connect('Account.db')
# cur = db.cursor()
# n = [x[0] for x in cur.execute("Select ID from Account").fetchall()][-1]
# db.close()
args = argv[1].split(' ')
print(args)
from_n = int(args[0]) - 1
to_n = int(args[0])
print(f"Start bots from {from_n} to {to_n}")
for i in range(from_n, to_n):
    print(i)
    # thread = Thread(target=start_process, args=(i + 1,))
    # thread.start()
    # time.sleep(1)
