#!/usr/bin/env python

import requests
import re
import json
import os
import time
import threading

config = {
	# 'dirName':'半藏森林',
	# 'owner_uid':2331498495,	
	'dirName':'徐小溢',
	#'owner_uid':3967022310,
	'owner_uid':'',
	'nickname':u'徐小溢',
	'start_page':1,
	'end_page':3,
}

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
		print('创建目录'+dirName+'成功')		
	else:
		print('目录'+dirName+'已经存在')
	return save_path

def download_photos(imgs,page_num):
	# imgs is a list		
	global save_path
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

def getAlbumIds( owner_uid , page_num=1 ):
	album_lists = [] 
	_rnd = int(1000 * time.time())
	url = 'http://photo.weibo.com/albums/get_all?uid='+str(owner_uid)+'&page='+str(page_num)+'&count=20&__rnd='+str(_rnd)		
	r = requests.get( url , cookies=cookies ,headers=headers )	
	albumListJson = r.text		
	albumListArr = json.loads(albumListJson)	
	if int( albumListArr['code'] ) != 0:
		print('用户'+owner_uid+'的相册ID信息未请求到...')
		return False
	albumListData = albumListArr['data']['album_list']	
	return albumListData

def getUidNick(nickname):
	if nickname == '':
		print('微博昵称不能为空!')
		exit()
	_rnd = int(1000 * time.time())	
	url = 'http://open.weibo.com/widget/ajax_getuidnick.php?rnd='+str(_rnd)
	payload = {"nickname":nickname}	
	r = requests.post(url,data=payload,cookies=cookies,headers=headers_open)			
	uidJson = r.text	
	uidArr = json.loads(uidJson)
	uid = uidArr['data']
	if uid:
		return uid
	else:
		print('找不到用户:'+nickname)
		return False


if __name__ == '__main__':	

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

	headers_open = {    
	    'Host':'open.weibo.com',
	    "Referer": "http://open.weibo.com/widget/followbutton.php",
	    'Origin':'http://open.weibo.com',
	    'Connection': 'keep-alive',
	    'User-Agent': agent
	}	

	with open('cookie') as f:
		content = f.read()	
	cookies = dict( l.strip().split('=',1) for l in content.split(';') ) 

	# with open('cookie_open') as f:
	# 	content_open = f.read()
	# cookie_open = dict( l.strip().split('=',1) for l in content_open.split(';') ) 	

	

	save_path = makeSavePath(config['dirName'])

	#徐娇
	# owner_uid = 1078007814
	# album_id =3818092304731046

	#半藏森林
	nickname = config['nickname']
	owner_uid = config['owner_uid']
	if owner_uid:
		owner_uid = config['owner_uid']	
	else:
		owner_uid = getUidNick(nickname)

	albumListData = getAlbumIds( owner_uid )
	start_page = config['start_page']
	end_page   = config['end_page']

	for album in albumListData:
		photoList = [] 
		threads = []

		album_id = album['album_id']
		albumName = album['caption']	
		if '微博配图' not in albumName:
			print(albumName+':忽略')
			continue 
		save_path = makeSavePath( config['dirName']+'/'+str(albumName) )	

		if start_page >= end_page :
			print('图片列表开始页码必须小于结束页码')
			exit()
		for page in range(start_page,end_page):
			photos = getPhotoList(cookies,owner_uid,album_id,page)
			#download_photos(photos,page)
			#print(photos)	
			photoList.append( photos )	
			i = page - start_page
			t = threading.Thread(target=download_photos,args=(photoList[i],page))
			threads.append(t)

		for t in threads:
			t.setDaemon(True)
			t.start()
		for t in threads:
			t.join()