#encoding: utf-8
import requests
from bs4 import BeautifulSoup
from env import env
import re
import hashlib
import time
import json
from concurrent.futures import ThreadPoolExecutor



def crawler(url_list):
	response = requests.get(url_list[0],headers=env.headers, cookies=env.cookies,)
	t = BeautifulSoup(response.text,'lxml').main.find('div',{'class':'container'}).attrs['t']
	t = int((int(t) - 99) / 99)
	sign = hashlib.sha1(f'Xr0Z-javascript-obfuscation-1{t}'.encode('utf-8')).hexdigest()
	url_list[1] += f'&t={t}&sign={sign}'

	response = requests.get(url_list[1],headers=env.headers, cookies=env.cookies )
	return sum(response.json()['items'])

if __name__ == '__main__':

	env = env()
	
	urls = []
	for page in range(1,1000+1):
		url1 = f'http://www.glidedsky.com/level/web/crawler-javascript-obfuscation-1?page={page}'
		url2 = f'http://www.glidedsky.com/api/level/web/crawler-javascript-obfuscation-1/items?page={page}'
		urls.append([url1,url2])

	pool = ThreadPoolExecutor(max_workers=20)
	score = 0
	for result in pool.map(crawler, urls):
		score += result
	print(score) 