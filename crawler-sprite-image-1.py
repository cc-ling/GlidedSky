import requests
from bs4 import BeautifulSoup
from env import env
import re
from concurrent.futures import ThreadPoolExecutor
import base64
import io
from PIL import Image

def  trans(div_html,response_str):
	number = ''
	img_size = Image.open(io.BytesIO(base64.b64decode(re.findall( 'base64,(.*?)"', str(response_str))[0]))).size
	size_range = [ _* (img_size[0])/10 for _ in range(1,11 )]
	# print(size_range)#[11.6, 23.2, 34.8, 46.4, 58.0, 69.6, 81.2, 92.8, 104.4, 116.0]

	divs = div_html.find_all('div')
	for div in divs:
		css_x = re.findall( div['class'][0]+ '.*?background-position-x:(.*?)px }', str(response_str))[0]
		css_w = re.findall( div['class'][0]+ '.*?width:(.*?)px }', str(response_str))[0]
		differ = [ abs(abs(int(css_x)) + int(css_w) - _) for _ in size_range  ]
		number  += str(differ.index(min(differ)))

	return int(number)
		



def crawler(url):#一页的
	response = requests.get(url,cookies=env.cookies)
	div_list = BeautifulSoup( response.text ,'lxml').find_all('div',{'class':'col-md-1'})
	return sum( trans(div_html,response.text) for div_html in div_list   )


if __name__ == '__main__':
	a = []
	env =env()
	urls = [f'http://www.glidedsky.com/level/web/crawler-sprite-image-1?page={page}' for page in range(1,1000+1) ]

	pool = ThreadPoolExecutor(max_workers=20)
	score = 0
	for result in pool.map(crawler, urls):
		score += result
	print(score)  #2561855
	
