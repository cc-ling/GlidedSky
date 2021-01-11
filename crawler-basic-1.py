#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/1/4 1
# @Author : cc_ling
# @Site :
# @Describe: 爬虫-基础1

import requests
from bs4 import BeautifulSoup
from env import env

def crawler(url):
	response = requests.get(url, headers=env.headers,cookies = env.cookies)
	html = BeautifulSoup( response.text ,'lxml').find_all('div',{'class':'col-md-1'})
	score = sum( int(row.text) for row in html )
	return score



if __name__ == '__main__':
	url = 'http://www.glidedsky.com/level/web/crawler-basic-1'
	env = env()
	score = crawler(url)
	print(score)#349466

