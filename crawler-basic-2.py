#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/1/4 1
# @Author : cc_ling
# @Site :
# @Describe: 爬虫-基础2

import requests
from bs4 import BeautifulSoup
from env import env
from concurrent.futures import ThreadPoolExecutor
# cookies = {'XSRF-TOKEN': 'eyJpdiI6Ik5yNkNScm5oZUJtUTJOcE5ZcnpaR1E9PSIsInZhbHVlIjoiOWl4bWhOelJrT3o3THNxd1puWXdtRlNkVFdaaFN4YXFFODNiclwvV1pVMTJsb1YwWXVsc083TkdZRTZWbUdROWIiLCJtYWMiOiI0OWNkMTQxYmRjN2M3MGQ0OWE5MmM3YTg1MmEzNTlkODc4YTlkZDJlMzUxOTg3YWYxMjhlNzMzZTMxN2VmMWYxIn0%3D', 'glidedsky_session': 'eyJpdiI6IllCc25hVFwvWVJFUXVJemg5N2VmWVh3PT0iLCJ2YWx1ZSI6InI1ZDVpM3lxcDBqOW50YTVPcFoxSDR1UmIzUVwvVlZrdloyOGV1bXc5Q1wvNW5HRkc4bVNPaGR6Y2p1QWlyNFNqWiIsIm1hYyI6IjcwMTY5MTQ4MGIzNDJiYzJmNzkyYWI5ZTljNDI2MDFhNGVmMjU3YmIyMTYyZTFkNTY4Y2UxNzNmYTUyN2EzNTYifQ%3D%3D'}
# headers = {		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'}


def crawler(url):
	response = requests.get(url, headers=env.headers, cookies=env.cookies)
	rows = BeautifulSoup(response.text, 'lxml').find_all('div', class_="col-md-1")
	score = sum(int(row.text) for row in rows)
	return score


if __name__ == '__main__':
	env = env()
	urls = []
	for page in range(1,1000+1):
		url = f'http://www.glidedsky.com/level/web/crawler-basic-2?page={page}'
		urls.append(url)

	pool = ThreadPoolExecutor(max_workers=20)
	score = 0
	for result in pool.map(crawler, urls):
		score += result
	print(score)  # 3349388