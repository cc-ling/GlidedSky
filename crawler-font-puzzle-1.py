import requests
from bs4 import BeautifulSoup
from env import env
import re
import io
import base64
from fontTools.ttLib import TTFont
from concurrent.futures import ThreadPoolExecutor

def trans(number,font_face):
	en_dig = {'zero':'0','one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9'}
	fio=io.BytesIO(base64.b64decode(font_face))
	font = TTFont(fio)
	newmap = {}
	for en in en_dig.keys():
		newdig = font.getGlyphID( en )-1
		newmap[ en_dig[en] ] = str( newdig )
	new_number = ''.join( newmap[_] for _ in str(number)  )
	return int(new_number)

def crawler(url):
	response = requests.get(url, headers=env.headers,cookies = env.cookies)
	font_face = re.findall('base64,(.*?)\)',str(response.text))[0]
	html = BeautifulSoup( response.text ,'lxml').find_all('div',{'class':'col-md-1'})
	score = sum(  trans( row.text ,font_face)  for row in html )
	return score

if __name__ == '__main__':
	env = env()
	urls = []
	for page in range(1,1000+1):
		url = f'http://www.glidedsky.com/level/web/crawler-font-puzzle-1?page={page}'
		urls.append(url)

	pool = ThreadPoolExecutor(max_workers=20)
	score = 0
	for result in pool.map(crawler, urls):
		score += result
	print(score)  
