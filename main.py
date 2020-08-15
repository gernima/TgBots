import os
import subprocess
import sys
from colorama import init, Fore, Back, Style
import time
from threading import Thread


init()


def start_process(shift1, shift2, x):
    while True:
        process = subprocess.Popen([sys.executable, "bot_V2.py", str(shift1) + ' ' + str(shift2) + ' ' + str(x)])
        process.wait()


input("Нажми Enter чтобы запустить...")
# process = subprocess.Popen([sys.executable, "bot_V2.py", str(0) + ' ' + str(10) + ' ' + str(3)])
# process.wait()
for i in range(6):
    thread_check_quest = Thread(target=start_process, args=(0, 10, i + 1))
    thread_check_quest.start()
    time.sleep(1)
