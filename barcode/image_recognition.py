# coding=utf-8

import requests
from bs4 import BeautifulSoup

import project_settings
from buildWhiteAndBlack import *
from process import *


def recognize_img(link):
    urllib.urlretrieve(link, project_settings.original_photo_url)
    ToWhiteAndBlack(project_settings.original_photo_url,
                    project_settings.white_black_url)
    recognizeFile(project_settings.white_black_url,
                  project_settings.result_url, 'xml')
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


def get_info_by_url(url):
    recognize_img(url)
    tmp1 = find_bar_code(
        '/home/mb/Desktop/hackathon/mABBYYlity_hackatone_CoddingKittens/barcode/tmp/result.xml')
    return find_info(tmp1)
