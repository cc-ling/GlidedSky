import requests
from bs4 import BeautifulSoup
from env import env
import re
import time
from concurrent.futures import ThreadPoolExecutor



def crawler(url):#一页的
	while True :
		try:
			response = requests.get(url, headers=env.headers, cookies=env.cookies,proxies = env.get_ip(),timeout=3)
			if response.status_code == 200:
				break
		except:
			continue
	print(f'已运行到{url[-3:]}页')
	rows = BeautifulSoup(response.text, 'lxml').find_all('div', class_="col-md-1")
	score = sum(int(row.text) for row in rows)
	return score if score != 0 else crawler(url)



if __name__ == '__main__':
	env =env()
	urls = [f'http://www.glidedsky.com/level/web/crawler-ip-block-2?page={page}' for page in range(1,1000+1) ]
	pool = ThreadPoolExecutor(max_workers=20)
	score = 0
	for result in pool.map(crawler, urls):
		score += result
	print(f'---{score}---')  
	
