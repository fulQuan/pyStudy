#!/usr/bin/env python

import requests
import re
import json
import os

import threading

def get_cookie(content):
	for line in content.split(';'):
		name,value = line.strip().split('=',1)
		cookies[name] = value
	return cookies

def makeSavePath(dirName):
	cur_path = os.path.abspath('.')
	save_path = cur_path + '/' + dirName +'/' 	
	isExists = os.path.exists(save_path)
	if not isExists:
		os.makedirs(save_path)


def download_imgs(imgs,page_num):
	# imgs is a list	
	cur_path = os.path.abspath('.')	
	save_path = cur_path + '/banzhangshenlin/' 	
	isExists = os.path.exists(save_path)

	if not isExists:
		os.makedirs(save_path)
	for img in imgs:
		
		filename = save_path + str(page_num) + '_' + str( imgs.index(img)+1 ) + '.jpg'
		#urlretrieve(img,filename)
		r = requests.get( img , headers=headers2,stream=True )		
		if r.status_code == 200:
			with open(filename,'wb') as f:
				f.write(r.content)				
		else:
			print(img+' is not 200 status')		

def getPhotoList( cookies , owner_uid , album_id , page_num):
	#url = 'http://weibo.com/p/aj/album/loading?ajwvr=6&type=photo&owner_uid='+str(owner_uid)+'&viewer_uid=&since_id=3815918373333594_-1_20150306_5afd5284313cb1faacf9a120a82ffa04&page_id=1005051665709880&page='+str(page_num)+'&ajax_call=1&__rnd=1491543315599'
	url = 'http://photo.weibo.com/photos/get_all?uid='+ str(owner_uid) +'&album_id='+ str(album_id) +'&count=30&page='+ str(page_num) +'&type=3&__rnd=1491549561043'	
	r = requests.get( url , cookies=cookies ,headers=headers )

	photoJson = r.text			
	photoArr = json.loads(photoJson)
	if int(photoArr['code']) != 0:		
		return False	

	photoData = photoArr['data'] 	
	photoList = photoData['photo_list']	
	imgList = []
	for photo in photoList:
		#print(photo['pic_name'])
		if photo['pic_name'] == '':
			continue
		pic_name = 'http://ww4.sinaimg.cn/mw1024/'+photo['pic_name']
		imgList.append(pic_name)
	return imgList				

agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
headers = {    
    'Host':'photo.weibo.com',
    "Referer": "http://photo.weibo.com/2074590761/talbum/index",
    'User-Agent': agent    
}

headers2 = {    
    'Host':'ww4.sinaimg.cn',
    "Referer": "http://photo.weibo.com/2074590761/talbum/index",
    'User-Agent': agent
}

with open('cookie') as f:
	content = f.read()
cookies = {}
cookies = get_cookie(content)

#owner_uid = 1665709880
#album_id = 3555868877467252
#owner_uid = 2074590761
#album_id = 3556570949005383
owner_uid = 1665709880
album_id = 3555868877467252

#徐娇
owner_uid = 1078007814
album_id =3818092304731046

#半藏森林
owner_uid = 2331498495
album_id = 3565934787550937

# photos = getPhotoList( cookies , owner_uid , 3 )
# download_imgs(photos)

photoList = [] 
threads = []
for page in range(1,150):
	photos = getPhotoList(cookies,owner_uid,album_id,page)
	#download_imgs(photos,page)
	#print(photos)	
	photoList.append( photos )	
	i = page - 1 
	#download_imgs( photoList[i],page )
	t = threading.Thread(target=download_imgs,args=(photoList[i],page))
	threads.append(t)

for t in threads:
	#t.setDaemon(True)
	t.start()
for t in threads:
	t.join()