# from fake_useragent import FakeUserAgent
# import pprint
# import logging
# from time import sleep
# import os
# from datetime import timedelta, date, datetime
# import pickle
# import shutil
# import numpy as np
# import cv2
# import mss
# import numpy
# import pyautogui
# from fake_useragent import UserAgent
# from random import sample
# from transliterate import translit, get_available_language_codes

# print(translit("Иван Иванов", reversed=True))
# a = [1, 2]
# s = 12345
# print()
import requests

headers = {
    "apikey": "c3b566c0-04b6-11eb-9501-5701751a06f9"
}
params = (
   ("url","https://freegeoip.app/json/"),
   ("render","true"),
   ("keep_headers","true"),
)

response = requests.get('https://app.zenscrape.com/api/v1/get', headers=headers, params=params)
print(response.text)
# x = 1
# dict_db = [1, 2,3,4,5]
# for i in range(5):
#     if x in dict_db:
#         print(1, x)
#     if x == 2:
#         x = 1
#     else:
#         x = 2

# with open("Allproxies.pkl", 'rb') as f:
#     proxies = pickle.load(f)
# with open("proxies.pkl", 'rb') as f:
#     a = pickle.load(f)
# print(len(a))
# a = []
# print(a)
# for i in range(20):
#     x = str(input()).strip().split(':')
#     y = [x[0], x[1]]
#     if y not in a:
#         a.append(y)
#     # if y not in proxies:
#     #     proxies.append(y)
# # print(a)
# pickle.dump(a, open(f"proxies.pkl", "wb"))
# with open("proxies.pkl", 'rb') as f:
#     print(pickle.load(f))
# print('-'*100)
# lenght = len(proxies)
# n = 100
# for i in range(0, lenght, n):
# 	if i // 100 < lenght // n:
# 		print('000')
# n = 3
# for i in range(0, len(proxies), n):
# 	print(proxies[i: i + n])
# for i in proxies:
#     print(f'{i[0]}:{i[1]}')
# for i in range(20):
#     x = str(input()).strip().split(':')
#     y = [x[0], x[1]]
#     if y not in proxies:
#         proxies.append(y)
# print(proxies)