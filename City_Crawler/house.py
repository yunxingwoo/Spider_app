#!/usr/bin/env python
# coding: utf-8
__author__ = 'lucky'

from bs4 import BeautifulSoup
import requests
import re
from statistics import *
from pypinyin import lazy_pinyin
import time


city = "上海"
header = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Cookie':'ganji_uuid=4741463695578080298139; ganji_xuuid=02e29c9a-0125-433d-ffd9-daca5c5efc01.1467566554164; GANJISESSID=fcfefa0d744404ca4816b70ab4bd3709; ganji_login_act=1467598678399; lg=1; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A32792188361%7D; __utmt=1; __utma=32156897.1683123081.1467566554.1467594393.1467597315.3; __utmb=32156897.4.10.1467597315; __utmc=32156897; __utmz=32156897.1467597315.3.2.utmcsr=sh.ganji.com|utmccn=(referral)|utmcmd=referral|utmcct=/fang1/o1/; webimUserId=3360501046%3A%3A2592000%3A%3A1467598680'
}

def house_crawler(city):
    city_pinyin = ''.join(lazy_pinyin(city))
    for i in range(1,20):
        time.sleep(3)
        rent_url = 'http://{}.ganji.com/fang1/o{}/'.format(city_pinyin,i)
        rent_web_data = requests.get(rent_url,headers = header)
        rent_soup = BeautifulSoup(rent_web_data.text,'lxml')
        rent_prices = rent_soup.select('.sale-price')
        rent_areas = rent_soup.find_all(text=re.compile("㎡"))[1::2]

        rent_price_list=[]
        rent_area_list=[]
        rent_sq_price_list=[]

        for price in rent_prices:
            rent_price_list.append(price.get_text())
        for area in rent_areas:
            yuan_position = area.find('.')
            rent_area_list.append(int(area[1:yuan_position]))

        for i, j in zip(rent_price_list,rent_area_list):
            if i !='面议' and j != 0:
                rent_sq_price_list.append(round(int(i)/j))
                rent_average_price = round(mean(rent_sq_price_list))

    time.sleep(10)
    buy_sq_price_list = []
    for i in range(1,20):
        time.sleep(2)
        buy_url = 'http://{}.ganji.com/fang5/o{}/'.format(city_pinyin,i)
        buy_web_data = requests.get(buy_url)
        buy_soup = BeautifulSoup(buy_web_data.text,'lxml')
        buy_sq_price = buy_soup.find_all(text=re.compile(('元')))
        for price in buy_sq_price:
            if price != '':
                if price[2:price.find('元')].isdigit():
                    buy_sq_price_list.append(int(price[2:price.find('元')]))

    buy_price = round(mean(buy_sq_price_list))
    print('{}的租房平均价格为{}元/平方米/月，二手房平均价格为{}元/平方米'.format(city,rent_average_price,buy_price))

house_crawler(city)