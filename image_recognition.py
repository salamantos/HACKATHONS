# coding=utf-8
import os
import requests
from bs4 import BeautifulSoup

import project_settings
from buildWhiteAndBlack import *
from process import *
from pyzbar.pyzbar import decode

from settings import *


def recognize_img(user_id, link, n):
    urllib.urlretrieve(link, 'tmp/' + str(
        user_id) + project_settings.original_photo_url)
    to_white_and_black[n]('tmp/' + str(user_id) +
                          project_settings.original_photo_url,
                          'tmp/' + str(
                              user_id) + project_settings.white_black_url)
    recognize_file('tmp/' + str(user_id) + project_settings.white_black_url,
                   'tmp/' + str(user_id) + project_settings.result_url, 'xml')

    return 0


def find_bar_code(xml_filename):
    xml_string = open(xml_filename).read()
    soup = BeautifulSoup(xml_string, 'lxml')
    for i in soup.find_all('block'):
        if str(i).count('Barcode'):
            return int(i.find('formatting').string)


def find_info(bar_code):
    r = requests.get(
        'http://www.goodsmatrix.ru/goods/d/{}.html'.format(bar_code))
    s = r.content.decode("windows-1251")
    soup = BeautifulSoup(s, 'lxml')
    title = soup.title.string
    if title.strip() == u'Гудс Матрикс':
        return None, None, None
    mark = soup.find('span', id="ctl00_ContentPH_Mark_MarkL")
    if mark is not None:
        mark = mark.string
    mark_num = soup.find('span', id="ctl00_ContentPH_Mark_MarkNum")
    if mark_num is not None:
        mark_num = mark_num.string
    return title, mark, mark_num


def get_info_by_url(bot, chat_id, user_id, url):
    if not os.path.exists('tmp/' + str(user_id)):
        os.makedirs('tmp/' + str(user_id))
    urllib.urlretrieve(url, 'tmp/' + str(
        user_id) + project_settings.original_photo_url)
    img = cv2.imread('tmp/' + str(
        user_id) + project_settings.original_photo_url, 0)
    tmp = decode(img)
    if len(tmp) != 0:
        s = tmp[0].data
        res = find_info(s)
        return res

    bot.send_message(chat_id, WE_TRYING).wait()

    for i in range(3):
        recognize_img(user_id, url, i)
        tmp1 = find_bar_code(
            'tmp/' + str(user_id) + project_settings.result_url)
        if tmp1 is None:
            print(user_id, i)
            time.sleep(2)
            continue
        res = find_info(tmp1)
        if res[0] is None:
            continue
        return res
    return ["Take a picture one more time, please"]
