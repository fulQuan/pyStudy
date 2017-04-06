#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
抓图片
'''

import requests
import re
import os
from urllib.request import urlretrieve

def get_cookie(content):
	for line in content.split(';'):
		name,value = line.strip().split('=',1)
		cookies[name] = value
	return cookies

def get_imgs(url):
	r = requests.get(url,cookies=cookies)
	if r.status_code != 200 :
		print('访问页面未成功...')
		exit()
	html = r.text

	pattern = r'class="BDE_Image" src="(.*?)"'# *? means non-greedy
	imgs = re.findall(pattern,html)
	return imgs

def download_imgs(imgs):
	# imgs is a list	
	cur_path = os.path.abspath('.')

	save_path = cur_path + '/imgs/' 

	isExists = os.path.exists(save_path)

	if not isExists:
		os.makedirs(save_path)
	
	for img in imgs:
		filename = save_path + str( imgs.index(img)+1 ) + '.jpg'
		#print(filename)
		urlretrieve(img,filename)
		#print(img)


with open('cookie') as f:
	content = f.read()

cookies = {}
cookies = get_cookie(content)

url = 'http://tieba.baidu.com/p/2166231880'
imgs = get_imgs(url)
download_imgs(imgs)

