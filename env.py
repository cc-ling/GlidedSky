#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/4 
# @Author : cc_ling


import requests

import re
class env(object):
	"""docstring for env"""
	def __init__(self):
		self.requests = requests.Session()
		self.email = ''
		self.password = ''
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
		}
		self.cookies = self.login()


	def login(self):
		login_url = 'http://glidedsky.com/login'
		text = self.requests.get(login_url, headers=self.headers).text
		token = re.findall('_token".*?"(.*?)"', str(text))[0]  # 用于登录的token
		data = {
			'_token': token,
			'email':self.email ,
			'password':self.password ,
		}
		a = self.requests.post(login_url, headers=self.headers, data=data)
		return requests.utils.dict_from_cookiejar(a.cookies)

	def get_ip(self):
		proxies = {}
		url = 'http://www.zhuzhaiip.com','http://www.xiequ.cn/'#两个ip代理平台
		
		proxy = requests.get(url).text.strip()
		# requests.get('http://www.baidu.com', proxies = {'http': 'http://' +  proxy},timeout=10 )
		proxies['http'] = 'http://' + proxy

		return proxies




if __name__ == '__main__':
	print(env().get_ip())


	