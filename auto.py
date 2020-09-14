from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import pickle
import os.path
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from smshuborg import Sms, SmsService, GetNumber
import cv2
import numpy as np
import pyscreenshot as ImageGrab
import pyautogui
from datetime import timedelta, date, datetime
from tkinter import Tk
import os
import shutil
from random import sample, randint
import sqlite3
from telethon import TelegramClient
from socks import SOCKS5
import subprocess, signal


class Coinomi:
    def __init__(self):
        self.open()

    def open(self):
        find_and_click_img("imgs/coinomi_icon.png", 0.90)
        # sleep(10)
        find_and_click_img("imgs/coinomi_wallet.png", 0.90)
        sleep(1)

    def wallet_get_key(self):
        find_and_click_img("imgs/coinomi_wallet_receive.png", 0.90)
        sleep(0.2)
        find_and_click_img("imgs/coinomi_wallet_receive_copy_key.png", 0.90)
        return Tk().clipboard_get()

    def create_wallet(self):
        find_and_click_img("imgs/coinomi_add_asset.png", 0.90)
        # sleep(0.2)
        find_and_click_img("imgs/coinomi_add_coin.png", 0.90)
        # sleep(0.2)
        find_and_click_img("imgs/coinomi_add_coin_search.png", 0.90)
        # sleep(0.2)
        pyautogui.write('LTC')
        sleep(0.5)
        find_and_click_img("imgs/coinomi_add_coin_ltc.png", 0.90)
        find_and_click_img("imgs/coinomi_add_coin_add.png", 0.90)
        find_and_click_img("imgs/coinomi_add_coin_password.png", 0.90)
        pyautogui.write(coinomi_password)
        sleep(0.2)
        find_and_click_img("imgs/coinomi_add_coin_password_unlock.png", 0.90)

    def send_all(self):
        screenshot = ImageGrab.grab()
        img = np.array(screenshot.getdata(), dtype='uint8').reshape((screenshot.size[1], screenshot.size[0], 3))
        patt = cv2.imread("imgs/coinomi_wallet_ltc_icon.png", 0)
        h, w, points = find_patt(img, patt, 0.92)
        first = True
        for pt in points:
            if not first:
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
                pyautogui.moveTo(pt[0] + w / 2, pt[1] + h / 2)
                pyautogui.click()
                sent = self.get_sent_transaction()
                received = self.get_received_transaction()
                if (sent == 0 and received >= 2) or ((sent > 0) and (received / sent > 2)):
                    self.send_to_main_wallet()
            else:
                first = False
        cv2.imwrite("output.jpg", img)

    def send_to_main_wallet(self):
        find_and_click_img("imgs/coinomi_wallet_send.png", 0.90)
        find_and_click_img("imgs/coinomi_wallet_send_address.png", 0.90)
        pyautogui.write("ltc1qzms32ydc9gnraz08j0qcpj5zhcg94tnpe7lmha")
        find_and_click_img("imgs/coinomi_wallet_send_all.png", 0.90)
        find_and_click_img("imgs/coinomi_wallet_send_send.png", 0.90)
        sleep(0.1)
        find_and_click_img("imgs/coinomi_wallet_send_confirm.png", 0.90)
        find_and_click_img("imgs/coinomi_wallet_send_password.png", 0.90)
        pyautogui.write(coinomi_password)
        find_and_click_img("imgs/coinomi_wallet_send_password_unlock.png", 0.90)
        sleep(5)

    def get_received_transaction(self):
        screenshot = ImageGrab.grab()
        img = np.array(screenshot.getdata(), dtype='uint8').reshape((screenshot.size[1], screenshot.size[0], 3))
        patt = cv2.imread("imgs/coinomi_wallet_received.png", 0)
        h, w, points = find_patt(img, patt, 0.9)
        return len(list(points))

    def get_sent_transaction(self):
        screenshot = ImageGrab.grab()
        img = np.array(screenshot.getdata(), dtype='uint8').reshape((screenshot.size[1], screenshot.size[0], 3))
        patt = cv2.imread("imgs/coinomi_wallet_sent.png", 0)
        h, w, points = find_patt(img, patt, 0.9)
        return len(list(points))


def find_patt(image, patt, thres):
    img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (patt_H, patt_W) = patt.shape[:2]
    res = cv2.matchTemplate(img_grey, patt, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res > thres)
    return patt_H, patt_W, zip(*loc[::-1])


def find_and_click_img(img_name, percent, x_plus=0, y_plus=0):
    screenshot = ImageGrab.grab()
    img = np.array(screenshot.getdata(), dtype='uint8').reshape((screenshot.size[1], screenshot.size[0], 3))
    patt = cv2.imread(img_name, 0)
    h, w, points = find_patt(img, patt, percent)
    points = list(points)
    if len(points) != 0:
        pyautogui.moveTo(points[0][0] + w / 2 + x_plus, points[0][1] + h / 2 + y_plus)
        pyautogui.click()


def get_completed_bots_from_folder():
    files = os.listdir(bots_dir)
    res = []
    db_accounts = [x[0] for x in cur.execute("""Select PHONE from Account""").fetchall()]
    for i in range(len(files)):
        file = files[i]
        if "template" not in file and "BANNED" not in file.upper():
            end_date = list(reversed(list(str(datetime.strptime(file.split(" ")[0], '%d.%m.%y').date() + timedelta(days=days_acc_stay)).split("-"))))
            end_date = datetime(int(end_date[2]), int(end_date[1]), int(end_date[0]))
            now = list(reversed(str(date.today()).split("-")))
            deadline = datetime(int(now[2]), int(now[1]), int(now[0]))
            if (file.split(" ")[0] in file) and (deadline >= end_date) and (file.split(" ")[-1] not in db_accounts):
                res.append(file)
    return res


def open_telegram(acc):
    os.startfile(f"{bots_dir}/{acc}/Telegram.exe")


def close_telegram():
    os.system("taskkill /f /im Telegram.exe")


class Proxy:
    def __init__(self, ms):
        self.checker = "https://checkerproxy.net/"
        self.open_browser()
        self.driver.get(self.checker)
        archives = self.get_archives_url()
        # self.driver.quit()
        # proxies = []
        self.ms = ms
        self.proxies = []
        res = []
        print(archives)
        for archive in archives:
            self.driver.get(archive)
            sleep(5)
            for j in self.get_proxies_from_checker():
                a = j.split(":")
                res.append([a[0], a[1]])
            sleep(5)
        print(len(res))
        print(res)
        self.save_proxies_to_file(res)
        self.driver.quit()

    def get_proxies_from_checker(self):
        self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/div/div[1]/div[1]/select[1]').click()
        self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/div/div[1]/div[1]/select[1]/option[3]').click()
        self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/div/div[1]/div[1]/select[3]').click()
        self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/div/div[1]/div[1]/select[3]/option[1]').click()
        WebDriverWait(self.driver, 5)
        tdbody = self.driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/div/table/tbody')
        trs = tdbody.find_elements_by_css_selector('tr')
        res = []
        for i in trs:
            ms = int(i.find_element_by_css_selector('td:nth-child(5) > div > span').text.replace(' ms', ''))
            if ms <= self.ms:
                res.append(i.find_element_by_css_selector('td:nth-child(1)').text)
        return res

    def save_proxies_to_file(self, a):
        pickle.dump(a, open(f"proxies.pkl", "wb"))

    def open_browser(self):
        options = Options()
        # options.add_argument("--headless")
        options.add_argument("disable-gpu")
        options.add_argument("--disable-extensions")
        # ua = UserAgent()
        # options.add_argument(f'user-agent={ua.chrome}')
        self.driver = webdriver.Chrome("chromedriver.exe", options=options)
        self.driver.set_window_size(1920, 1080)

    def new_tab(self, url):
        # self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + "t")
        self.driver.execute_script(f'''window.open("{url}","_blank");''')
        # self.driver.get(url)

    def paste_proxies(self, text):
        area = self.driver.find_element_by_xpath('//*[@id="textList"]')
        area.click()
        area.send_keys(text)
        self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div[2]/div/div[2]/div/div/input').click()

    def next_tab(self):
        self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + Keys.PAGE_UP)

    def prev_tab(self):
        self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + Keys.PAGE_DOWN)

    def close_tab(self):
        self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + "W")

    def get_archives_url(self):
        ul = self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div[2]/div/div[1]/ul')
        uls = ul.find_elements_by_css_selector('li > a')
        return [i.get_attribute("href") for i in uls]

    def get_proxies_from_archive(self):
        self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[1]/div/div[1]/div[1]/select[1]').click()
        self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[1]/div/div[1]/div[1]/select[1]/option[3]').click()
        # WebDriverWait(self.driver, 5)
        sleep(5)
        # return self.get_proxies_from_checker()
        elem = self.driver.find_element_by_css_selector('#find_result')
        elem.click()
        elem.send_keys(Keys.CONTROL + "c")
        return Tk().clipboard_get()


class VPN:
    def open(self):
        find_and_click_img("imgs/vpn_icon.png", 0.90)
        sleep(10)

    def on(self):
        find_and_click_img("imgs/vpn_on.png", 0.90)

    def off(self):
        find_and_click_img("imgs/vpn_off.png", 0.90)

    def refresh(self):
        self.off()
        sleep(5)
        self.on()


def auth_client(filename, x, ip, port, api_id, api_hash, device):
    return TelegramClient(f'anons/{filename}', int(api_id), str(api_hash), device_model=device, proxy=(SOCKS5, ip, port))


def get_random_proxy():
    with open("proxies.pkl", 'rb') as f:
        proxies = pickle.load(f)
    proxy = proxies[randint(0, len(proxies) - 1)]
    return str(proxy[0]), int(proxy[1])


class RegBot:
    def __init__(self, filename):
        self.phone = filename.split(' ')[-1].strip()
        self.password = filename.split(" ")[0].replace('.', '')
        self.url = "https://my.telegram.org/auth?to=apps"
        self.groups = ['@LOWCS','@lifeyt','@breakingmash','@ikniga','@yurydud','@audioknigi_channel','@bazabazon','@muzyka_muzika', '@chop_choop', '@topor', '@darkxaxa', '@Plan_P', '@intimology_sex', '@pocketyt', '@black_side_link', '@toplesofficial', '@skillget', '@special_tg']
        self.bot_groups = ['@Litecoin_click_bot']
        self.api_id = ""
        self.api_hash = ""
        self.device = self.get_device()
        self.proxy = get_random_proxy()

        # self.vpn = VPN()
        # self.vpn.open()
        # self.vpn.on()

        open_telegram(filename)
        pyautogui.prompt('Open Tg')
        self.add_groups()
        self.reg_app()
        self.create_anon()
        sleep(5)
        close_telegram()
        sleep(5)

    def save_to_db(self):
        # key = pyautogui.prompt('Enter wallet key')
        cur.execute(
            """INSERT INTO Account(PHONE, PASS, API_ID, API_HASH, ACTIVITY, LITECOIN, DEVICE) VALUES (?,?,?,?,?,?,?);""",
            (self.phone, self.password, self.api_id, self.api_hash, "ON", "", self.device))
        db.commit()

    def create_anon(self):
        x = str(cur.execute(f"""Select ID from Account where PHONE='{self.phone}'""").fetchone()[0])
        filename = str("anon" + x)
        print(f"Входим в аккаунт {filename}: " + self.phone)
        client = auth_client(filename, x, self.proxy[0], self.proxy[1], self.api_id, self.api_hash, self.device)
        password = lambda x: x
        pyautogui.confirm('Write code and Press enter')
        client.start(password=password(self.password))
        sleep(1)

    def get_ltc_key_from_coinomi(self):
        wallet = Coinomi()
        sleep(3)
        wallet.create_wallet()
        sleep(3)
        return wallet.wallet_get_key()

    def get_device(self):
        return sample([x.strip() for x in UserAgent().random.split('(')[1].split(')')[0].split(';')], 1)[0]

    def get_and_set_api_id_and_hash(self):
        self.api_id = self.driver.find_element_by_css_selector("#app_edit_form > div:nth-child(3) > div.col-md-7 > span > strong").text
        self.api_hash = self.driver.find_element_by_css_selector("#app_edit_form > div:nth-child(4) > div.col-md-7 > span").text

    def open_browser(self):
        options = Options()
        # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # options.add_argument("--headless")
        options.add_argument("disable-gpu")
        # options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-sh-usage")
        ua = UserAgent()
        options.add_argument(f'user-agent={ua.chrome}')
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
        self.driver.set_window_size(1920, 1080)

    def reg_app(self):
        self.open_browser()
        self.driver.get(self.url)
        self.paste_number()
        self.paste_code()
        sleep(3)
        self.driver.find_element_by_css_selector("#app_title").send_keys("Testing")
        self.driver.find_element_by_css_selector("#app_shortname").send_keys("Testing")
        self.driver.find_element_by_css_selector("#app_create_form > div:nth-child(6) > div > div:nth-child(5)").click()
        self.driver.find_element_by_css_selector("#app_save_btn").click()
        sleep(5)
        self.get_and_set_api_id_and_hash()
        self.driver.close()
        self.save_to_db()

    def paste_number(self):
        self.driver.find_element_by_css_selector("#my_login_phone").send_keys(self.phone)
        self.driver.find_element_by_css_selector("#my_send_form > div.support_submit > button").click()

    def paste_code(self):
        code = pyautogui.prompt('Enter telegram code for reg app')
        self.driver.find_element_by_css_selector("#my_password").send_keys(code)
        self.driver.find_element_by_css_selector("#my_login_form > div.support_submit > button").click()

    def get_code_from_number(self):
        self.SMS_HUB_API_KEY = "36265Ua0c6cb84f62dc4849055d9e5d97d86cb"
        self.wrapper = Sms(self.SMS_HUB_API_KEY)
        self.phone = GetNumber(
            service=SmsService().Telegram
        )
        self.activation = self.phone.request(self.wrapper)

    def get_code(self):
        self.activation.was_sent().request(self.wrapper)
        self.code = self.activation.wait_code(wrapper=self.wrapper)

    def reg_telegram(self):
        find_and_click_img("imgs/telegram_start.png", 0.90)
        find_and_click_img("imgs/telegram_login.png", 0.90)
        find_and_click_img("imgs/telegram_login_phone.png", 0.90)

    def add_groups(self):
        find_and_click_img("imgs/telegram_search.png", 0.9, x_plus=60)
        groups = self.bot_groups.copy()
        groups.extend(sample(self.groups, 5))
        for group in groups:
            pyautogui.write(group)
            sleep(2)
            find_and_click_img("imgs/telegram_search_results.png", 0.6, y_plus=30)
            sleep(1)
            if group in self.bot_groups:
                find_and_click_img("imgs/telegram_bot_start.png", 0.6)
            else:
                sleep(1)
                find_and_click_img("imgs/telegram_group_join.png", 0.82)
            find_and_click_img("imgs/telegram_search.png", 0.9, x_plus=60)
            [pyautogui.press("backspace") for _ in range(len(group))]
            [pyautogui.press("delete") for _ in range(len(group))]


def copy_telegram_template(filename):
    path = "E:/Боты"
    shutil.copytree(path + "/template", path + f'/{filename}')


add_id = 0
db = sqlite3.connect('Account.db')
cur = db.cursor()
bots_dir = "E:\Боты"
days_acc_stay = 1
coinomi_password = "wallet0159456"
Proxy(500)
# res_accs = get_completed_bots_from_folder()
# print(res_accs)
# RegBot(res_accs[0])
# RegBot("28.08.20 Антон Лапенко +380935312119")
# for acc in res_accs:
#     RegBot(acc)
#     sleep(10)
# close_telegram()
# copy_telegram_template(acc)
# open_telegram(acc)
# for acc in res_accs:
#     reg = RegBot(acc)
# proxy = Proxy(1000)
# coinomi = Coinomi()
# for i in range(5):
#     coinomi.create_wallet()
# print(coinomi.wallet_get_key())
# a = pyautogui.alert('This is an alert box.')
a = pyautogui.confirm('Программа завершена')
# a = pyautogui.confirm('Enter option.', buttons=['A', 'B', 'C'])
# a = pyautogui.prompt('Enter telegram code for app?')
# a = pyautogui.password('Enter password (text will be hidden)')
db.close()
