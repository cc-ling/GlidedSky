import requests
from bs4 import BeautifulSoup
from env import env
import re
import io
import base64
from fontTools.ttLib import TTFont
from concurrent.futures import ThreadPoolExecutor
import time


def trans(number,font_face):
	fio=io.BytesIO(base64.b64decode(font_face))
	font = TTFont(fio)
	newmap = {}
	for i, GlyphID in enumerate(font.getGlyphOrder()[1:11]) :
		GlyphID = GlyphID.replace('uni','0x')
		newmap[ chr(eval(GlyphID)) ] = str(i) #对应的是str不是int，方便一会转换
	new_number = ''.join( newmap[_] for _ in str(number)  )
	return int(new_number)

def crawler(url):
	
	try:
		response = requests.get(url, headers=env.headers,cookies = env.cookies)
		font_face = re.findall('base64,(.*?)\)',str(response.text))[0]
		html = BeautifulSoup( response.text ,'lxml').find_all('div',{'class':'col-md-1'})
		score = sum(  trans( row.text.strip() ,font_face)  for row in html )
		# print(f'已经运行{round(time.time()-t1,1)}s')
		# page = re.findall('?page=(.*?)',str(url))
		print(f'已经运行{round(time.time()-t1,1)}s,当前是第{url[-5:]}页')
		return score
	except:
		return crawler(url)

if __name__ == '__main__':
	t1 = time.time()
	env = env()
	urls = []
	for page in range(1,1000+1):
		url = f'http://www.glidedsky.com/level/web/crawler-font-puzzle-2?page={page}'
		urls.append(url)

	pool = ThreadPoolExecutor(max_workers=20)
	score = 0
	for result in pool.map(crawler, urls):
		score += result
	print(score)  