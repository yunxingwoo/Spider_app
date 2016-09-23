#!/usr/bin/env python
# coding: utf-8
__author__ = 'lucky'

from bs4 import BeautifulSoup
import requests
import re
from statistics import *
from pypinyin import lazy_pinyin
import time

def job_crawler(city,job):
    url_zhaopin_main = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl={}&kw={}".format(city,job)
    web_data = requests.get(url_zhaopin_main)
    Soup = BeautifulSoup(web_data.text,'lxml')
    #获取页码的工作数量
    job_num = Soup.select('body > div.main > div.search_newlist_main > div.seach_yx > span.search_yx_tj > em')[0].get_text()
    page_num = int(job_num) // 60 + 1
    if page_num > 90:
        page_num = 90
    salary_min = []
    salary_max = []
    for i in range(1, page_num + 1):
        url_zhaopin_page = url_zhaopin_main + '&p={}'.format(i)
        web_data_page = requests.get(url_zhaopin_page)
        soup_page = BeautifulSoup(web_data_page.text, 'lxml')
        salary_total = soup_page.select('.zwyx')
        for i in salary_total:
            salary = i.get_text()
            if salary.find('-')+1:
                salary_min.append(int(salary[:salary.find('-')])) #获取薪酬低位
                salary_max.append(int(salary[salary.find('-')+1:])) #获取薪酬高位
    average_salary_min = round(mean(salary_min)) #取最低薪酬的平均
    average_salary_max = round(mean(salary_max)) #取最高薪酬的平均
    median_salary_min = round(median(salary_min)) #取最低工资的中位数
    median_salary_max = round(median(salary_max)) #取最高工资的中位数
    print('在{},关键词为{}的工作共有{}份，平均工资为{}-{}，中位数工资为{}-{}'.format(city,job,job_num,average_salary_min,average_salary_max,median_salary_min,median_salary_max))

def house_crawler(city):
    city_pinyin = ''.join(lazy_pinyin(city))
    for i in range(1,20):
        time.sleep(3)
        rent_url = 'http://{}.ganji.com/fang1/o{}/'.format(city_pinyin,i)
        rent_web_data = requests.get(rent_url)
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

def weather_crawler(city):
    city_pinyin = ''.join(lazy_pinyin(city))
    weather_url = 'http://lishi.tianqi.com/{}/index.html'.format(city_pinyin)
    weather_web_data = requests.get(weather_url)
    weather_soup = BeautifulSoup(weather_web_data.text,'lxml')
    weather = weather_soup.select(' div.tqtongji > p')[0].get_text()[0:-15]
    wind = weather_soup.select('  div.tqtongji > ul')[1].get_text().replace('\n',' ')
    print(weather,'\n\n'+'风力情况为：\n',wind)


if __name__ == '__main__':
    city_keyword = input('请输入目标城市：')
    job_keyword = input('请输入工作关键词：')
    job_crawler(city_keyword, job_keyword)
    print('')
    house_crawler(city_keyword)
    print('')
    weather_crawler(city_keyword)

