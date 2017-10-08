# coding=utf-8

import os
import requests
from bs4 import BeautifulSoup
import settings
import urllib
from pyzbar.pyzbar import decode
import cv2
import db

def find_bar_code(xml_filename):
    xml_string = open(xml_filename).read()
    soup = BeautifulSoup(xml_string, 'lxml')
    for i in soup.find_all('block'):
        if str(i).count('Barcode'):
            try:
                return int(i.find('formatting').string)
            except:
                return None


def find_info(bar_code):
    r = requests.get(
        'http://www.goodsmatrix.ru/goods/d/{}.html'.format(bar_code))
    s = r.content.decode("windows-1251")
    soup = BeautifulSoup(s, 'lxml')
    title = soup.title.string
    if title.strip() == u'Гудс Матрикс':
        return None, None, None
    mark = soup.find('span', id="ctl00_ContentPH_Mark_MarkL")
    reviews_score = float(db.get_score(title.split()[2]))
    print(reviews_score)
    if mark is not None and reviews_score is not None:
        mark = (float(mark.string.split()[0].replace(',', '.'))/2 + reviews_score)/2
    elif mark is not None:
        mark = reviews_score
    elif reviews_score is not None:
        mark = float(mark.string.split()[0].replace(',', '.'))/2
    mark_num = soup.find('span', id="ctl00_ContentPH_Mark_MarkNum")
    if mark_num is not None:
        mark_num = mark_num.string
    return title, mark, mark_num


def get_info_by_url(bot, chat_id, user_id, url, set=None):
    if not os.path.exists('tmp/' + str(user_id)):
        os.makedirs('tmp/' + str(user_id))

    urllib.urlretrieve(url, 'tmp/' + str(
        user_id) + settings.original_photo_url)
    img = cv2.imread('tmp/' + str(
        user_id) + settings.original_photo_url, 0)
    tmp = decode(img)
    if len(tmp) != 0:
        s = tmp[0].data
        res = find_info(s)
        return res
    else:
        return ["Я не могу распознать фото :( Попробуй отправить получше"]
