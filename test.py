from fake_useragent import FakeUserAgent
import pprint
import logging
from time import sleep
import os
from datetime import timedelta, date, datetime
import pickle
import shutil
import numpy as np
import cv2
import mss
import numpy
import pyautogui
from fake_useragent import UserAgent
from random import sample

print(sample([x.strip() for x in UserAgent().random.split('(')[1].split(')')[0].split(';')], 1)[0])
# sleep(3)
# with mss.mss() as sct:
#     monitor = {"top": 0, "left": 0, "width": 1366, "height": 768}
#     img = numpy.array(sct.grab(monitor))
# template = cv2.imread("imgs/telegram_group_join.png", cv2.IMREAD_GRAYSCALE)
# w, h = template.shape[::-1]
# gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
# loc = np.where(res >= 0.82)
# first = True
# for pt in zip(*loc[::-1]):
#     if not first:
#         cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
#     else:
#         first = False
# cv2.imwrite("output.jpg", img)
# proxies = []
# for i in range(20):
#     x = str(input()).strip().split(':')
#     y = [x[0], x[1]]
#     if y not in proxies:
#         proxies.append(y)
# print(proxies)
# pickle.dump(proxies, open(f"proxies.pkl", "wb"))
# with open("proxies.pkl", 'rb') as f:
# 	print(pickle.load(f))

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
# sum = 0
# print(sum)
# os.startfile("E:/Боты/11.07.20 Ваня Христофоров/Telegram.exe")
# end_date = ".".join(list(reversed(str(datetime.strptime('11.07.2020', '%d.%m.%Y').date() + timedelta(days=10)).split("-"))))
# print(end_date)
# input()