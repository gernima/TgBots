from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import sqlite3
import time
# from bot_V2 import get_data_from_db, get_random_proxy
from socks import SOCKS5
from random import randint
import getpass
from threading import Lock

lock = Lock()


def get_random_proxy():
    proxy = proxies[randint(0, len(proxies) - 1)]
    return str(proxy[0]), int(proxy[1])


def get_data_from_db():
    try:
        lock.acquire(True)
        a = {}
        b = cur.execute("Select ID from Account").fetchall()
        a['len'] = len(b)
        for i in b:
            i = i[0]
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


def auth_client(filename, x, ip, port):
    client = TelegramClient(f'anons/{filename}', int(dict_db[x]["API_ID"]), str(dict_db[x]["API_HASH"]),
                            device_model=dict_db[x]["DEVICE"], proxy=(SOCKS5, ip, port))
    return client


proxies = [['178.62.197.23', '42237'], ['148.251.173.36', '1080'], ['140.82.39.225', '32843'], ['173.44.37.82', '1085'],
           ['90.76.55.14', '1080'], ['54.85.107.167', '8888'], ['85.192.160.54', '1180'], ['176.9.26.123', '1080'],
           ['78.157.192.86', '1080'], ['80.82.69.126', '8975'], ['78.141.196.193', '30245']]
db = sqlite3.connect('Account.db')
cur = db.cursor()
dict_db = get_data_from_db()
if __name__ == '__main__':
    ip, port = get_random_proxy()
    # for i in cur.execute("Select ID from Account").fetchall():
    x = 6
    print("Входим в аккаунт: " + dict_db[x]["PHONE"])
    filename = str("anon" + str(x))
    client = TelegramClient(f'anons/{filename}', int(dict_db[x]["API_ID"]), str(dict_db[x]["API_HASH"]),
                            device_model=dict_db[x]["DEVICE"], proxy=(SOCKS5, ip, port))
    password = lambda x: x
    client.start(password=password(dict_db[x]["PASS"]))
    time.sleep(1)
