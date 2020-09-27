from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telethon import sync, events
from selenium.webdriver.chrome.options import Options
import requests
import json
import hashlib
from time import sleep
import re
from telethon import TelegramClient, events, sync
import webbrowser
import urllib.request
import os
import sqlite3
from fake_useragent import FakeUserAgent
from socks import SOCKS5
from random import randint, sample
import logging
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest, ImportChatInviteRequest
from sys import argv
from threading import Lock
import pickle
import datetime
from telethon import functions, types
from transliterate import translit
from string import hexdigits

with open("proxies.pkl", 'rb') as f:
    proxies = list(pickle.load(f))


def get_random_proxy():
    proxy = proxies[randint(0, len(proxies) - 1)]
    return str(proxy[0]), int(proxy[1])


def auth_client(filename, x, ip, port):
    client = TelegramClient(f'anons/{filename}', int(dict_db["API_ID"]), str(dict_db["API_HASH"]),
                            device_model=dict_db["DEVICE"], proxy=(SOCKS5, ip, port))
    return client


class LTCBot:
    def __init__(self, client, x, logger, ch):
        self.name = "LTC Click Bot"
        self.client = client
        self.x = x
        self.logger = logger
        self.ch = ch

    def get_balance(self):
        try:
            self.client.send_message(self.name, "/balance")
            sleep(5)
            msgs = self.client.get_messages(self.tegmo, limit=1)
            for mes in msgs:
                str_a = str(mes.message)
                zz = str_a.replace('Available balance: ', '')
                qq = zz.replace(" LTC", '')
                return float(qq)
        except Exception as e:
            self.client.send_message(self.name, "❌ Cancel")
            return self.get_balance()

    def take_balance(self):
        msgs = self.client.get_messages(self.tegmo, limit=1)
        for mes in msgs:
            if re.search(r'Enter the amount to withdraw:', mes.message):
                if float(dict_db["BALANCE"]) > 0.0004:
                    self.client.send_message(self.name, str(dict_db["BALANCE"]))
                else:
                    self.client.send_message(self.name, "0.0004")
        sleep(3)
        self.client.send_message(self.name, "✅ Confirm")
        self.logger.info(f"№{self.x}, withdraw - {dict_db['BALANCE']}")

    def withdraw(self):
        self.client.send_message(self.name, "💵 Withdraw")
        sleep(3)
        msgs = self.client.get_messages(self.tegmo, limit=1)
        for mes in msgs:
            if re.search(r'To withdraw, enter your Litecoin address:', mes.message):
                self.client.send_message(self.name, dict_db["LITECOIN"])
                sleep(3)
                self.take_balance()
            elif re.search(r'Enter the amount to withdraw:', mes.message):
                self.take_balance()

    def check_withdraw(self):
        self.logger.info(f"№{self.x}, balance - {dict_db['BALANCE']}")
        if float(dict_db["BALANCE"]) >= 0.0004:
            self.logger.info(f"№{self.x}, start withdraw - {dict_db['BALANCE']}")
            self.withdraw()

    def work(self):
        self.logger.info(self.name)
        n = 0
        u = 0
        dlgs = self.client.get_dialogs()
        for dlg in dlgs:
            if dlg.title == self.name:
                self.tegmo = dlg
        dict_db["BALANCE"] = float(self.get_balance())
        self.check_withdraw()
        self.client.send_message(self.name, "🖥 Visit sites")
        sleep(10)
        while True:
            sleep(10)
            if u != 0:
                # self.logger.info(f"№{self.x}, Нет заданий уже: " + str(u) + " раз")
                pass
            if u == 5:
                self.logger.info(f'{datetime.datetime.now()} №{self.x} Переходим на другого бота, нет заданий')
                break
            # if n % 100 == 0 and n != 0:
            #     self.logger.info(f"{datetime.datetime.now()} №{self.x} Пройдено циклов: " + str(n))
            if n == 300:
                self.logger.info(f'{datetime.datetime.now()} №{self.x} Переходим на другого бота, лимит заданий')
                break
            msgs = self.client.get_messages(self.tegmo, limit=1)
            for mes in msgs:
                if re.search(r'\bseconds to get your reward\b', mes.message):
                    # self.logger.info("Найдено reward")
                    str_a = str(mes.message)
                    zz = str_a.replace('You must stay on the site for', '')
                    qq = zz.replace('seconds to get your reward.', '')
                    waitin = int(qq)
                    # self.logger.info(f"Ждать придется: {waitin}")
                    self.client.send_message(self.name, "/visit")
                    sleep(5)
                    msgs2 = self.client.get_messages(self.tegmo, limit=1)
                    for mes2 in msgs2:
                        button_data = mes2.reply_markup.rows[1].buttons[1].data
                        message_id = mes2.id
                        # self.logger.info("Перехожу по ссылке")
                        sleep(5)
                        url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                        try:
                            ch = RunChromeTests()
                            ch.testMethod(url_rec, waitin)
                        except:
                            resp = self.client(GetBotCallbackAnswerRequest(
                                self.name,
                                message_id,
                                data=button_data
                            ))
                        sleep(15)
                        try:
                            fp = urllib.request.urlopen(url_rec)
                            mybytes = fp.read()
                            mystr = mybytes.decode("utf8")
                            fp.close()
                            if re.search(r'\bSwitch to reCAPTCHA\b', mystr):
                                resp = self.client(GetBotCallbackAnswerRequest(
                                    self.name,
                                    message_id,
                                    data=button_data
                                ))
                                sleep(5)
                                # self.logger.info("КАПЧА!")
                            else:
                                sleep(waitin)

                                sleep(5)
                        except:
                            sleep(waitin)
                elif re.search(r'\bSorry\b', mes.message):
                    # self.logger.info("Найдено Sorry")
                    u = u + 1
                else:
                    messages = self.client.get_messages('Litecoin_click_bot')
                    url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                    f = open(f"pers/per{self.x}.txt", 'w+')
                    fd = f.read()
                    if fd == url_rec:
                        # self.logger.info("Найдено повторение переменной")
                        msgs2 = self.client.get_messages(self.tegmo, limit=1)
                        for mes2 in msgs2:
                            button_data = mes2.reply_markup.rows[1].buttons[1].data
                            message_id = mes2.id
                            resp = self.client(GetBotCallbackAnswerRequest(
                                self.tegmo,
                                message_id,
                                data=button_data
                            ))
                            sleep(5)
                        u += 1
                    else:
                        waitin = 15
                        try:
                            data1 = requests.get(url_rec).json
                            my_file = open(f'pers/per{self.x}.txt', 'w+')
                            my_file.write(url_rec)
                            # self.logger.info("Новая запись в файле сделана")
                            sleep(30)
                            n = n + 1
                            if n == 10:
                                break
                        except requests.exceptions.SSLError:
                            self.logger.info('SSLError skip')
                        except:
                            sleep(10)
        self.check_withdraw()
        self.logger.removeHandler(self.ch)


class EarnBot:
    def __init__(self, name, search_name, client, x, logger, ch, view_chanell_name):
        self.name = name
        self.dlg_name = search_name
        self.client = client
        self.x = x
        self.logger = logger
        self.ch = ch
        self.view_chanell_name = view_chanell_name
        self.bot_messages = {"CorpBisbot_newbot": {"output": {"join_chanell1": "❗️ Для использования бота подпишитесь на наш канал: ",
                                                              "join_chanell2":"🚀 Для заработка подпишитесь на наш канал с просмотрами: ",
                                                              "view": "Для начисления нажмите на кнопку:",
                                                              "end_tasks": ["Задания кончились"],
                                                              "go_to_bot": "Перейдите в бота",
                                                              "go_to_chanell": "Вступите в группу",
                                                              "earn": "заработать",
                                                              "bonus": "бонус",
                                                          "check_robot": "Для проверки, что Вы не робот, решите пример:"},
                                                   "input": {"earn_mes": "🚀 Заработать"},
                                                   "before_change_task_n": False,
                                                   "task_n": {0: 3, 3: 6},
                                                   "break_task_n": 6,
                                                   "skip_button": [1, 0],
                                                    "check_robot": False},
                            "Eternal_Money_Bot": {"output": {"join_chanell1": "❗️ Для использования бота подпишитесь на наш канал: ",
                                                              "join_chanell2": "🚀 Для заработка подпишитесь на наш канал с просмотрами: ",
                                                              "view": "Для начисления нажмите на кнопку:",
                                                              "end_tasks": ["Задания кончились", "Задания закончились"],
                                                              "go_to_bot": ["Перейдите в бота"],
                                                              "go_to_chanell": ["Вступите в группу"],
                                                              "earn": "🤑 Выберите способ заработка 👇",
                                                              "bonus": "бонус",
                                                          "check_robot": "Для проверки, что Вы не робот, решите пример:"},
                                                   "input": {"earn_mes": "❤️ Заработок"},
                                                   "before_change_task_n": True,
                                                   "task_n": {0: 1, 3: 5},
                                                   "break_task_n": 5,
                                                   "skip_button": [[2, 0], [1, 0]],
                                                    "check_robot": False},
                            "Toptgmoney_bot": {"output": {
                                                          "join_chanell1": "❗️ Для использования бота подпишитесь на наш канал: ",
                                                          "join_chanell2": "🚀 Для заработка подпишитесь на наш канал с просмотрами: ",
                                                          "view": "Для начисления нажмите на кнопку:",
                                                          "end_tasks": ["Задания кончились", "Задания закончились"],
                                                          "go_to_bot": ["Перейдите в бота"],
                                                          "go_to_chanell": ["Вступите в группу"],
                                                          "earn": "🚀 Как Вы хотите заработать?",
                                                          "bonus": "бонус",
                                                          "check_robot": "Для проверки, что Вы не робот, решите пример:"},
                                                    "input": {"earn_mes": "💳 Заработать"},
                                                    "before_change_task_n": False,
                                                    "task_n": {0: 2, 2: 5},
                                                    "break_task_n": 5,
                                                    "skip_button": [[1, 0]],
                                                    "check_robot": True,
                                                    "robot_answers": 3},
                             "TGSTAR_BOT": {"output": {
                                                 "join_chanell1": "❗️ Для использования бота подпишитесь на наш канал: ",
                                                 "join_chanell2": "🚀 Для заработка подпишитесь на наш канал с просмотрами: ",
                                                 "view": "Для начисления нажмите на кнопку:",
                                                 "end_tasks": ["Задания кончились", "Задания закончились"],
                                                 "go_to_bot": ["Перейдите в бота"],
                                                 "go_to_chanell": ["Подпишитесь на канал", "Вступите в группу"],
                                                 "earn": "💰 Вы можете заработать:",
                                                 "bonus": "бонус",
                                                 "check_robot": "Для проверки, что Вы не робот, решите пример:"},
                                 "input": {"earn_mes": "👨‍💻 Заработать"},
                                 "before_change_task_n": False,
                                 "task_n": {2: 5},
                                 "break_task_n": 5,
                                 "skip_button": [[1, 0], [2, 0]],
                                 "check_robot": False,
                                 "robot_answers": 3},
                             "Nicetgbot": {"output": {
                                                 "join_chanell1": "❗️ Для использования бота подпишитесь на наш канал: ",
                                                 "join_chanell2": "🚀 Для заработка подпишитесь на наш канал: ",
                                                 "view": "Для начисления нажмите на кнопку:",
                                                 "end_tasks": ["Задания кончились", "Задания закончились"],
                                                 "go_to_bot": ["Перейдите в бота"],
                                                 "go_to_chanell": ["Подпишитесь на канал", "Вступите в группу"],
                                                 "earn": "🚀 Как Вы хотите заработать?",
                                                 "bonus": "бонус",
                                                 "check_robot": "🤖 Для проверки, что Вы не робот, решите пример:"},
                                 "input": {"earn_mes": "🚀 Заработать"},
                                 "before_change_task_n": False,
                                 "task_n": {0: 2, 3: 6},
                                 "break_task_n": 5,
                                 "skip_button": [[1, 0], [2, 0]],
                                 "check_robot": True,
                                 "robot_answers": 3}
        }
        dlgs = self.client.get_dialogs()
        for dlg in dlgs:
            if dlg.title == self.dlg_name:
                self.tegmo = dlg
        # self.set_avatar()
        # self.set_username()

    def join(self, chanell):
        self.client(functions.channels.JoinChannelRequest(channel=chanell))

    def set_avatar(self):
        file = sample(os.listdir("avatars/"), 1)[0]
        self.client(functions.photos.UploadProfilePhotoRequest(
            file=client.upload_file(f'avatars/{file}')
        ))

    def set_username(self):
        added = "".join(sample(list(hexdigits), 3))
        a = client.get_me().stringify().split("\n")[16:18]
        info = {}
        for i in a:
            i = i.replace("'", "").replace("\t", "").replace(",", "")
            c = i.split("=")
            info[c[0]] = c[1]
        name = "".join((str(info["first_name"]) + str(info['last_name'])).split())
        username = translit(name, reversed=True) + added
        self.client(functions.account.UpdateUsernameRequest(
            username=username
        ))

    def start_join(self, mes, join_chanell):
        chanell_url = mes.message.replace(join_chanell, "").replace("https://t.me/", "").strip()
        self.join("@" + chanell_url)
        self.client.send_message(self.name, self.bot_messages[self.name]["input"]["earn_mes"])

    def click_callback(self, mes, row, col):
        button_data = mes.reply_markup.rows[row].buttons[col].data
        message_id = mes.id
        try:
            resp = self.client(GetBotCallbackAnswerRequest(
                peer=self.name,
                msg_id=message_id,
                data=button_data
            ))
        except:
            pass

    def earn_go_to_bot(self, mes):
        forward = False
        if "перешлите любое сообщение" in mes.message.lower() and "затем вернитесь в бот" not in mes.message.lower():
            forward = True
        url = mes.reply_markup.rows[0].buttons[0].url.split("/")[-1].split("?")[0]
        # print(mes.reply_markup.rows[0].buttons[0].url, url, forward)
        try:
            self.join("@" + url)
        except:
            try:
                self.join(url)
            except:
                try:
                    self.client.send_message("@" + url, "/start")
                except:
                    self.skip(mes)
                    return
        sleep(1)
        if forward:
            new_mes = self.client.get_messages(url, limit=1)[-1]
            self.client.forward_messages(self.name, new_mes.id, url)
        else:
            self.click_callback(mes, 1, 0)
            sleep(10)
        if not self.check_reward():
            self.skip(mes)
            # self.earn_go_to_bot(new_mes)

    def skip(self, mes):
        try:
            self.click_callback(mes, self.bot_messages[self.name]["skip_button"][0][0],
                                self.bot_messages[self.name]["skip_button"][0][1])
        except:
            self.click_callback(mes, self.bot_messages[self.name]["skip_button"][1][0],
                                self.bot_messages[self.name]["skip_button"][1][1])

    def earn_mes(self):
        self.client.send_message(self.name, self.bot_messages[self.name]["input"]["earn_mes"])

    def check_reward(self):
        sleep(2)
        mes = self.client.get_messages(self.name, limit=1)[-1].message
        if "начислено" in mes:
            return True
        return False

    def earn_join_group(self, mes, row, col):
        url = mes.reply_markup.rows[row].buttons[col].url.replace("https://t.me/", "").split("?")[0]
        try:
            self.join("@" + url)
        except:
            self.client.send_message("@" + url, "/start")

    def earn_views(self):
        dlgs = self.client.get_dialogs()
        for dlg in dlgs:
            if dlg.title == self.view_chanell_name:
                url = dlg
        # url = "@" + self.view_chanell_name
        messgs = self.client.get_messages(url, limit=1000)
        for mes in messgs:
            try:
                if self.bot_messages[self.name]["output"]["view"] in mes.message:
                    self.click_callback(mes, 0, 0)
                    sleep(5)
            except:
                pass

    def answer_robot(self, mes, answer):
        for i in range(self.bot_messages[self.name]["robot_answers"]):
            if str(answer) in str(mes.reply_markup.rows[0].buttons[i].text):
                self.click_callback(mes, 0, i)
                return

    def work(self):
        # self.earn_views()
        task_n = 0
        not_task = 0
        # input("end")
        mes = self.client.get_messages(self.name, limit=1)[-1]
        if "Вы бот или нет?:" in mes.message:
            self.click_callback(mes, 0, 0)
        if self.bot_messages[self.name]["before_change_task_n"]:
            if task_n in self.bot_messages[self.name]["task_n"]:
                task_n = self.bot_messages[self.name]["task_n"][task_n]
        self.earn_mes()
        prev_mes = ""
        while True:
            sleep(3)
            mes = self.client.get_messages(self.name, limit=1)[-1]
            while self.bot_messages[self.name]["input"]["earn_mes"] in mes.message:
                self.earn_mes()
                mes = self.client.get_messages(self.name, limit=1)[-1]
            if not_task > 5:
                break
            # print(not_task, task_n, mes.message.split("\n")[0])
            if check_subs_in_mes(self.bot_messages[self.name]["output"]["end_tasks"], mes.message) or prev_mes == mes.message:
                # print("end_tasks")
                not_task += 1
                if task_n == self.bot_messages[self.name]["break_task_n"]:
                    break
                else:
                    if task_n in self.bot_messages[self.name]["task_n"]:
                        task_n = self.bot_messages[self.name]["task_n"][task_n]
                    else:
                        task_n += 1
                self.earn_mes()
            elif self.bot_messages[self.name]["output"]["bonus"] in mes.message.lower():
                # print("bonus")
                not_task = 0
                if self.bot_messages[self.name]["output"]["bonus"] in mes.reply_markup.rows[0].buttons[0].text.lower():
                    self.click_callback(mes, 0, 0)
                break
            elif self.bot_messages[self.name]["output"]["earn"] in mes.message:
                # print("earn")
                if self.name == "TGSTAR_BOT" and task_n == 5:
                    self.click_callback(mes, task_n, 1)
                else:
                    self.click_callback(mes, task_n, 0)
            elif self.bot_messages[self.name]["output"]["join_chanell1"] in mes.message:
                self.start_join(mes, self.bot_messages[self.name]["output"]["join_chanell1"])
            elif "Выберите социальную сеть для заработка:" in mes.message:
                self.click_callback(mes, 0, 0)
            elif self.bot_messages[self.name]["output"]["check_robot"] in mes.message:
                exs = mes.message.replace(self.bot_messages[self.name]["output"]["check_robot"], "").strip().replace("=", "")
                if "+" in exs:
                    exl = exs.split("+")
                    answer = int(exl[0]) + int(exl[1])
                self.answer_robot(mes, answer)
            elif self.bot_messages[self.name]["output"]["join_chanell2"] in mes.message:
                self.start_join(mes, self.bot_messages[self.name]["output"]["join_chanell2"])
            elif check_subs_in_mes(self.bot_messages[self.name]["output"]["go_to_bot"], mes.message) or \
                    check_subs_in_mes(self.bot_messages[self.name]["output"]["go_to_chanell"], mes.message):
                not_task = 0
                self.earn_go_to_bot(mes)
                self.earn_mes()
            prev_mes = mes.message


def check_subs_in_mes(subs, mes):
    tf = False
    for i in subs:
        if i in mes:
            tf = True
    return tf


class RunChromeTests:
    def testMethod(self, url_rec, waitin):
        selenium_url = "http://localhost:4444/wd/hub"
        options = Options()
        options.add_argument(f'user-agent={ua.chrome}')
        caps = {'browserName': 'chrome'}
        driver = webdriver.Remote(command_executor=selenium_url, desired_capabilities=caps, options=options)
        driver.maximize_window()
        driver.get(url_rec)
        sleep(waitin + 10)
        driver.close()
        driver.quit()


x = int(argv[1])
# x = 20
ua = FakeUserAgent()
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
bots_char = {"CorpBisbot_newbot": ["TimCorpBisNew", "TimCorpBis Views"],
             "Eternal_Money_Bot": ["ETERNAL - Заработок в Telegram", "Каталог постов 👁️"],
             "Toptgmoney_bot": ["TOP TG MONEY", "Каталог постов от TOP TG MONEY💥"],
             "TGSTAR_BOT": ["TGSTAR", "TGSTAR | WORK"],
             "Nicetgbot": ["Телеграм продвижение", ""]}
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
        sleep(300)
while True:
    logger.info("Очередь аккаунта № " + str(x))
    bot = LTCBot(client, x, logger, ch)
    bot.work()
    for bot in list(bots_char):
        logger.info(f"№{x}, {bot}")
        bot = EarnBot(bot, bots_char[bot][0], client, x, logger, ch, bots_char[bot][1])
        bot.work()
    logger.info(f"№{x}, Wait")
    sleep(1800)

