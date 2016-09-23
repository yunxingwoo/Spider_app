#!/usr/bin/env python
# coding: utf-8
__author__ = 'lucky'

import requests
from bs4 import BeautifulSoup

def app_crawler(name):
    url = 'http://www.appchina.com/sou/'+name
    web_data =requests.get(url)
    soup = BeautifulSoup(web_data.text,'lxml')
    title = soup.select('ul > li > div.app-info > h1 > a')[0].get_text()
    downloads = soup.select('ul > li > div.app-info > span.download-count')[0].get_text()
    print('在应用汇上,'+title+' '+'下载量为：'+downloads)

def zhushou_crawler(name):
    url ='http://zhushou.360.cn/search/index/?kw='+name
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text,'lxml')
    title = soup.select('body > div.warp > div.main > div > ul > li > dl > dd > h3 > a > span')[0].get_text()
    downloads = soup.select('body > div.warp > div.main > div > ul > li > div > div.sdlft > p.downNum')[0].get_text()
    print('在360手机助手上,'+title+' '+'下载量为：'+downloads)

def andorid_crawler(name):
    url = 'http://apk.hiapk.com/search?key='+name
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text,'lxml')
    title = soup.select('ul > li > div > dl > dt > span > a')[0].get_text()
    downloads = soup.select('div.soft_list_box > ul > li > div > div.right > div.s_dnum')[0].get_text().replace(' ','').replace('\n','')[:-2]
    print('在安卓市场上,'+title+' '+'下载量为：'+downloads)


name = input('请输入想搜索的应用名称：')
app_crawler(name)
zhushou_crawler(name)
andorid_crawler(name)
