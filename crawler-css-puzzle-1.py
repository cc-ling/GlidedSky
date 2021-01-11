import requests
from bs4 import BeautifulSoup
from env import env
import re
from concurrent.futures import ThreadPoolExecutor


def  trans(div_html,response_str):

	divs = div_html.find_all('div')
	if '' in [ _.text for _ in divs] : #有一个在context内
		for div in divs:
			if not div.text:  #如果是空，就在class标签的context内
				class_name = div['class'][0]
				number = re.findall( f'{class_name}:before.*content:"(.*?)"', str(response_str))[0]
				number = int(number)	
	
	else :#left:2em  em正数就是往右，负数就是往左
		class_list = [div['class'][0] for div in divs ]
		numbet_str = ''.join(div.text.strip() for div in divs )
		new_number = ['' for _ in numbet_str]	
		for i in range(len(class_list)):
			css = re.findall( class_list[i] + '.*?left:(.*?)em'  ,str(response_str))
			if css: #如果有left
				new_number[  i + int(css[0])	] = numbet_str[i]

			elif re.findall( class_list[i] + '.*?opacity:(.*?) }'  ,str(response_str)): #若果有透明
				new_number[i] = ''
			else: #啥都没有就是不动
				new_number[ i ] = numbet_str[i]
		number =  int(''.join(new_number)) 

	return number


def crawler(url):#一页的
	response = requests.get(url,cookies=env.cookies)
	div_list = BeautifulSoup( response.text ,'lxml').find_all('div',{'class':'col-md-1'})
	return sum( trans(div_html,response.text) for div_html in div_list   )


if __name__ == '__main__':

	env =env()
	urls = [f'http://www.glidedsky.com/level/web/crawler-css-puzzle-1?page={page}' for page in range(1,1000+1) ]

	pool = ThreadPoolExecutor(max_workers=20)
	score = 0
	for result in pool.map(crawler, urls):
		score += result
	print(score)  #2953704 [Finished in 20.6s]
	
