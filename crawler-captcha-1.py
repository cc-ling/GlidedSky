from selenium import webdriver
import requests
from PIL import Image
from io import BytesIO
import cv2
import numpy as np

from random import uniform
from bs4 import BeautifulSoup
import time
from cv2 import cv2 
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

def download_img(img_url,img_name):
	with open(f'img/{img_name}','wb') as f:
		f.write( requests.get(img_url).content )

def get_postion( chunk, canves):
	"""
	判断缺口位置
	:param chunk: 缺口图片是原图
	:param canves:
	:return: 位置 x, y
	"""
	otemp = 'img/' +  chunk
	oblk = 'img/' +  canves
	target = cv2.imread(otemp, 0)
	template = cv2.imread(oblk, 0)
	# w, h = target.shape[::-1]
	temp = 'img/temp.jpg'
	targ = 'img/targ.jpg'
	cv2.imwrite(temp, template)
	cv2.imwrite(targ, target)
	target = cv2.imread(targ)
	target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
	target = abs(255 - target)
	cv2.imwrite(targ, target)
	target = cv2.imread(targ)
	template = cv2.imread(temp)
	result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
	x, y = np.unravel_index(result.argmax(), result.shape)
	return x, y
	# # 展示圈出来的区域
	# cv2.rectangle(template, (y, x), (y + w, x + h), (7, 249, 151), 2)
	# cv2.imwrite("yuantu.jpg", template)
	# cv2.imshow('Show', template)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
def slide(driver):
	driver.switch_to.frame(driver.find_element_by_id('tcaptcha_iframe'))
	# driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))    
	#大图 小滑块
	bk_block = driver.find_element_by_xpath('//img[@id="slideBg"]')  # 大图
	bk_black_width = bk_block.size
	bk_black_width = bk_black_width['width']
	bk_block_x = bk_block.location['x']
	slide_block = driver.find_element_by_xpath('//*[@id="slideBlock"]')
	slide_block_x = slide_block.location['x']
	# 大图 url 小滑块 图片url 滑块
	bk_block_url = driver.find_element_by_xpath('//img[@id="slideBg"]').get_attribute('src')  # 大图 url
	slide_block_url = driver.find_element_by_xpath('//img[@id="slideBlock"]').get_attribute('src')  # 小滑块 图片url
	slid_ing = driver.find_element_by_xpath('//div[@id="tcaptcha_drag_thumb"]')  # 滑块

	download_img(bk_block_url,'bk_block.png')
	download_img(slide_block_url,'slide_block.png')
	time.sleep(0.5)
	img_bk_block = Image.open('img/bk_block.png')
	real_width = img_bk_block.size[0]
	width_scale = float(real_width) / float(bk_black_width)
	position = get_postion('bk_block.png', 'slide_block.png')
	# chunk='bk_block.png'; canves  ='slide_block.png'
	real_position = position[1] / width_scale
	real_position = real_position - (slide_block_x - bk_block_x)
	####模拟滑动
	ActionChains(driver).click_and_hold(on_element= slide_block ).perform()  # 点击鼠标左键，按住不放
	time.sleep(0.5);xxx=uniform(50,150)
	ActionChains(driver).move_by_offset(xoffset= xxx , yoffset=0).perform()  # 鼠标移动到距离
	time.sleep(0.3)
	ActionChains(driver).move_by_offset(xoffset=  real_position-xxx, yoffset=0).perform()  # 鼠标移动到距离
	time.sleep(0.2)
	ActionChains(driver).release(on_element=slid_ing).perform()


def to_next_page(driver):
	
	driver.find_elements_by_css_selector("[rel=next]")[0].click()
	# driver.find_element_by_xpath('//*[@id="app"]/main/div[1]/ul/li[13]/a').click()

def login(driver):
	#登录
	driver.find_element_by_xpath('//*[@id="email"]').send_keys(账号)
	driver.find_element_by_xpath('//*[@id="password"]').send_keys(密码)
	driver.find_element_by_xpath('//*[@id="app"]/main/div[1]/div/div/div/div[2]/form/div[4]/div/button').click()


def get_page_sum(driver):
	time.sleep(1)
	window = driver.current_window_handle
	driver.switch_to.window(window)
	rows = BeautifulSoup(driver.page_source, 'lxml').find_all('div', class_="col-md-1")
	nums = [int(row.text) for row in rows]
	return int(sum(nums))
	

def is_class_element_present(driver, value):
    try:
        driver.find_element_by_class_name(value)
    except NoSuchElementException :
        return False
    return True

def main(page):
	score = 0
	driver = webdriver.Chrome()
	driver.get(f'http://www.glidedsky.com/level/web/crawler-captcha-1?page={page}')

	login(driver)
	for page in range(page,page+10):
		time.sleep(uniform(1,2))
		while True: #过验证码
			slide(driver)
			#如果刷新页面还在
			time.sleep(uniform(1,2))
			if is_class_element_present(driver, 'tc-action-icon'):
				driver.find_element_by_class_name('tc-action-icon').click()
				window = driver.current_window_handle
				driver.switch_to.window(window);time.sleep(uniform(1,2))
				continue
			else:
				_ = get_page_sum(driver)
				score += _
				print(f'第{page}页数据：{_},总计{score}')
				if page %10 ==0:
					break
				to_next_page(driver);time.sleep(uniform(1,2))
				break
	driver.close()
	return score


if __name__ == '__main__':
	from env import env
	score = 0
	for page in range(1,1000,10):
		score += main(page)
		print(f'---前{page-1+10}页数据：{score}---')#每十页关闭重打开一次
		time.sleep(uniform(2,3.5))


