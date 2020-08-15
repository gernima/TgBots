import sqlite3
import time
from telethon import TelegramClient
from telethon import sync, events
import re
import json
from create_client import get_random_proxy, get_data_from_db, proxies, auth_client
from socks import SOCKS5


def get_balance(client, bot, tegmo):
    client.send_message(bot, "/balance")
    time.sleep(3)
    msgs = client.get_messages(tegmo, limit=1)
    for mes in msgs:
        str_a = str(mes.message)
        zz = str_a.replace('Available balance: ', '')
        if 'satoshi' in zz:
            zz = zz.replace(zz[zz.find(' ('):zz.find(')') + 1], '')
        qq = zz.replace(" LTC", '')
        return float(qq)


db = sqlite3.connect('Account.db')
cur = db.cursor()
print('checking balance')
x = 1
# sum = [0.00135624, 0, 0, 0, 0]
sum = [0, 0, 0, 0, 0]
coins = [' LTC', ' BTC', ' ZEC', ' BCH', ' DOGE']
coin = 0
# ltc,btc, zec, bch, doge
dict_db = get_data_from_db()

# bots = ['LTC Click Bot', 'BTC Click Bot', 'ZEC Click Bot', 'BCH Click Bot', 'DOGE Click Bot']
bots = ['LTC Click Bot']
while True:
    if x == 7:
        print("Всего добыто:")
        print(coins)
        print(sum)
        input('exit?')
        break
    print("Очередь аккаунта № " + str(x))
    filename = str("anon" + str(x))
    ok = False
    while ok is False:
        try:
            ip, port = get_random_proxy()
            client = auth_client(filename, x, ip, port)
            client.start(password=dict_db[x]["PASS"])
            ok = True
        except:
            pass
    coin = 0
    dlgs = client.get_dialogs()
    for bot in bots:
        for dlg in dlgs:
            if dlg.title == bot:
                tegmo = dlg
        sum[coin] += get_balance(client, bot, tegmo)
        coin += 1
    print(coins)
    print(sum)
    x += 1
    time.sleep(5)
