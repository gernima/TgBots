from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telethon import sync, events
from selenium.webdriver.chrome.options import Options
import requests
import json
import hashlib
import time
import re
from telethon import TelegramClient
import webbrowser
import urllib.request
import os
import sqlite3
from fake_useragent import FakeUserAgent
from socks import SOCKS5
from random import randint
import logging
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from sys import argv
from threading import Lock
import pickle
import datetime

lock = Lock()
with open("proxies.pkl", 'rb') as f:
    proxies = list(pickle.load(f))


def get_random_proxy():
    proxy = proxies[randint(0, len(proxies) - 1)]
    return str(proxy[0]), int(proxy[1])


def auth_client(filename, x, ip, port):
    client = TelegramClient(f'anons/{filename}', int(dict_db["API_ID"]), str(dict_db["API_HASH"]),
                            device_model=dict_db["DEVICE"], proxy=(SOCKS5, ip, port))
    return client


class RunChromeTests:
    def testMethod(self):
        selenium_url = "http://localhost:4444/wd/hub"
        options = Options()
        # options.add_argument(f'user-agent={ua.chrome}')
        caps = {'browserName': 'chrome'}
        driver = webdriver.Remote(command_executor=selenium_url, desired_capabilities=caps, options=options)
        driver.maximize_window()
        driver.get(url_rec)
        time.sleep(waitin + 10)
        driver.close()
        driver.quit()


def get_balance(client, bot, tegmo, x):
    try:
        client.send_message(bot, "/balance")
        time.sleep(5)
        msgs = client.get_messages(tegmo, limit=1)
        for mes in msgs:
            str_a = str(mes.message)
            zz = str_a.replace('Available balance: ', '')
            qq = zz.replace(" LTC", '')
            return float(qq)
    except Exception as e:
        client.send_message(bot, "❌ Cancel")
        return get_balance(client, bot, tegmo, x)


def take_balance(client, tegmo):
    msgs = client.get_messages(tegmo, limit=1)
    for mes in msgs:
        if re.search(r'Enter the amount to withdraw:', mes.message):
            if float(dict_db["BALANCE"]) > 0.0004:
                client.send_message(bot, str(dict_db["BALANCE"]))
            else:
                client.send_message(bot, "0.0004")
    time.sleep(3)
    client.send_message(bot, "✅ Confirm")
    logger.info(f"№{x}, withdraw - {dict_db['BALANCE']}")


def withdraw(client, x, tegmo, bot, logger):
    client.send_message(bot, "💵 Withdraw")
    time.sleep(3)
    msgs = client.get_messages(tegmo, limit=1)
    for mes in msgs:
        if re.search(r'To withdraw, enter your Litecoin address:', mes.message):
            client.send_message(bot, dict_db["LITECOIN"])
            time.sleep(3)
            take_balance(client, tegmo)
        elif re.search(r'Enter the amount to withdraw:', mes.message):
            take_balance(client, tegmo)


def check_withdraw(client, x, tegmo, bot, logger):
    logger.info(f"№{x}, balance - {dict_db['BALANCE']}")
    if float(dict_db["BALANCE"]) >= 0.0004:
        logger.info(f"№{x}, start withdraw - {dict_db['BALANCE']}")
        withdraw(client, x, tegmo, bot, logger)


x = int(argv[1])
# x = 2
ua = FakeUserAgent()
# bots = ['LTC Click Bot', 'BTC Click Bot', 'ZEC Click Bot', 'BCH Click Bot', 'DOGE Click Bot']
bots = ['LTC Click Bot']
dict_db = {'PHONE': argv[2], 'PASS': argv[3], 'API_ID': int(argv[4]), 'API_HASH': argv[5], 'LITECOIN': argv[6], 'DEVICE': argv[7]}
filename = f"anon{x}"
logger = logging.getLogger(f'logs/{filename}')
logger.setLevel(logging.INFO)
con = logging.StreamHandler()
con.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
con.setFormatter(formatter)
logger.addHandler(con)
ch = logging.FileHandler(f'logs/{filename}')
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.info(f"{datetime.datetime.now()} Входим в аккаунт: " + str(dict_db["PHONE"]))
ok = False
while ok is False:
    ip, port = get_random_proxy()
    try:
        logger.info(f"№{x} Proxy {ip}:{port}")
        client = auth_client(filename, x, ip, port)
        password = lambda x: x
        client.start(password=password(dict_db["PASS"]))
        ok = True
    except Exception as e:
        logger.error(f"Failed login account №{x}, {e}")
        # proxies.remove([ip, str(port)])
        # pickle.dump(proxies, open(f"proxies.pkl", "wb"))
        # print(f"№{x} remove proxy {ip}:{port} n-proxies:{len(proxies)}")
        time.sleep(300)
while True:
    print("Очередь аккаунта № " + str(x))
    for bot in bots:
        logger.info(bot)
        n = 0
        u = 0
        dlgs = client.get_dialogs()
        for dlg in dlgs:
            if dlg.title == bot:
                tegmo = dlg
        dict_db["BALANCE"] = float(get_balance(client, bot, tegmo, x))
        check_withdraw(client, x, tegmo, bot, logger)
        client.send_message(bot, "🖥 Visit sites")
        time.sleep(10)
        while True:
            time.sleep(10)
            if u != 0:
                # logger.info(f"№{x}, Нет заданий уже: " + str(u) + " раз")
                pass
            if u == 5:
                logger.info(f'{datetime.datetime.now()} №{x} Переходим на другого бота, нет заданий')
                break
            if n % 10 == 0 and n != 0:
                logger.info(f"{datetime.datetime.now()} №{x} Пройдено циклов: " + str(n))
            if n == 1000:
                logger.info(f'{datetime.datetime.now()} №{x} Переходим на другого бота, лимит заданий')
                break
            msgs = client.get_messages(tegmo, limit=1)
            for mes in msgs:
                if re.search(r'\bseconds to get your reward\b', mes.message):
                    # logger.info("Найдено reward")
                    str_a = str(mes.message)
                    zz = str_a.replace('You must stay on the site for', '')
                    qq = zz.replace('seconds to get your reward.', '')
                    waitin = int(qq)
                    # logger.info(f"Ждать придется: {waitin}")
                    client.send_message(bot, "/visit")
                    time.sleep(5)
                    msgs2 = client.get_messages(tegmo, limit=1)
                    for mes2 in msgs2:
                        button_data = mes2.reply_markup.rows[1].buttons[1].data
                        message_id = mes2.id
                        # logger.info("Перехожу по ссылке")
                        time.sleep(5)
                        url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                        try:
                            ch = RunChromeTests()
                            ch.testMethod()
                        except:
                            resp = client(GetBotCallbackAnswerRequest(
                                bot,
                                message_id,
                                data=button_data
                            ))
                        time.sleep(15)
                        try:
                            fp = urllib.request.urlopen(url_rec)
                            mybytes = fp.read()
                            mystr = mybytes.decode("utf8")
                            fp.close()
                            if re.search(r'\bSwitch to reCAPTCHA\b', mystr):
                                resp = client(GetBotCallbackAnswerRequest(
                                    bot,
                                    message_id,
                                    data=button_data
                                ))
                                time.sleep(5)
                                # logger.info("КАПЧА!")
                            else:
                                time.sleep(waitin)

                                time.sleep(5)
                        except:
                            time.sleep(waitin)
                elif re.search(r'\bSorry\b', mes.message):
                    # logger.info("Найдено Sorry")
                    u = u + 1
                else:
                    messages = client.get_messages('Litecoin_click_bot')
                    url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                    f = open(f"pers/per{x}.txt", 'w+')
                    fd = f.read()
                    if fd == url_rec:
                        # logger.info("Найдено повторение переменной")
                        msgs2 = client.get_messages(tegmo, limit=1)
                        for mes2 in msgs2:
                            button_data = mes2.reply_markup.rows[1].buttons[1].data
                            message_id = mes2.id
                            resp = client(GetBotCallbackAnswerRequest(
                                tegmo,
                                message_id,
                                data=button_data
                            ))
                            time.sleep(5)
                        u += 1
                    else:
                        waitin = 15
                        try:
                            data1 = requests.get(url_rec).json
                            my_file = open(f'pers/per{x}.txt', 'w+')
                            my_file.write(url_rec)
                            # logger.info("Новая запись в файле сделана")
                            time.sleep(30)
                            n = n + 1
                            if n == 10:
                                break
                        except requests.exceptions.SSLError:
                            logger.info('SSLError skip')
                        except:
                            time.sleep(10)
        check_withdraw(client, x, tegmo, bot, logger)
    logger.info(f"№{x}, Wait")
    time.sleep(900)
    logger.removeHandler(ch)
    # if x == y + 1:
    #     x = y
    # else:
    #     x = y + 1
