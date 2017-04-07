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

def download_imgs(imgs,page_num):
	# imgs is a list	
	cur_path = os.path.abspath('.')	
	save_path = cur_path + '/cr2/' 
	isExists = os.path.exists(save_path)

	if not isExists:
		os.makedirs(save_path)
	for img in imgs:
		
		filename = save_path + str(page_num) + '_' + str( imgs.index(img)+1 ) + '.jpg'
		#urlretrieve(img,filename)
		r = requests.get( img , headers=headers,stream=True )
		if r.status_code == 200:
			with open(filename,'wb') as f:
				f.write(r.content)
		
		#exit()
		#print(img)

def getPhotoList( cookies , owner_uid , album_id , page_num):
	#url = 'http://weibo.com/p/aj/album/loading?ajwvr=6&type=photo&owner_uid='+str(owner_uid)+'&viewer_uid=&since_id=3815918373333594_-1_20150306_5afd5284313cb1faacf9a120a82ffa04&page_id=1005051665709880&page='+str(page_num)+'&ajax_call=1&__rnd=1491543315599'
	url = 'http://photo.weibo.com/photos/get_all?uid='+ str(owner_uid) +'&album_id='+ str(album_id) +'&count=30&page='+ str(page_num) +'&type=3&__rnd=1491549561043'	
	r = requests.get( url , cookies=cookies ,headers=headers )

	photoJson = r.text		
	#print(photoJson)
	#exit()
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


#agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
headers = {
    #"Host": "ww4.sinaimg.cn",
    "Referer": "http://weibo.com/",
    'User-Agent': agent,
    'cookie':'SINAGLOBAL=3835687604732.8115.1432179708807; __gads=ID=d8a10c57ed6b586b:T=1465175789:S=ALNI_MZ6g3TIslh-cjxCCMAm_-SauKJ_Kw; _ga=GA1.2.155721227.1465175853; wvr=6; un=kingphar@sina.com; SCF=Al_qKUo3mjcY-iNxta3uyB_pp0dI1-6cGxBYFYJITFZFnzhED_NAUZx8JDT5aqTn-1FSjbbicoeNAjw7ZV1migA.; SUB=_2A2514pptDeRhGedI7lsW9i3OyD2IHXVWmYylrDV8PUNbmtBeLRjdkW9Sjmk3Re0ddbdX9W9RHKstYI815Q..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF550EJJw3QO.-y3X6VEHgQ5JpX5KMhUgL.Fo2cSK.NSoeEe022dJLoIpBLxKqLBonL1K5LxKqLBonL1KWcUntt; SUHB=09P8t4zRilJQvV; ALF=1523064252; SSOLoginState=1491528253; _s_tentry=login.sina.com.cn; Apache=4662900153676.244.1491528257303; ULV=1491528257309:472:4:3:4662900153676.244.1491528257303:1491445068093; USRANIME=usrmdinst_42; UOR=s.share.baidu.com,service.weibo.com,zihaolucky.github.io'
}

with open('cookie') as f:
	content = f.read()
cookies = {}
cookies = get_cookie(content)

#owner_uid = 1665709880
#album_id = 3555868877467252
owner_uid = 2074590761
album_id = 3556570949005383


# photos = getPhotoList( cookies , owner_uid , 3 )
# download_imgs(photos)

photoList = [] 
threads = []
for page in range(1,20):
	photos = getPhotoList(cookies,owner_uid,album_id,page)
	#download_imgs(photos,page)
	#print(photos)
	photoList.append( photos )
	i = page - 1 
	#download_imgs( photoList[i],page )
	t = threading.Thread(target=download_imgs,args=(photoList[i],page))
	threads.append(t)

for t in threads:
	t.setDaemon(True)
	t.start()