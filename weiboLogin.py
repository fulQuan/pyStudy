#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests
import base64
import re
import rsa
import json
import time
import urllib.parse
import binascii
from config import config

def preLogin( username ,password ):
	su  = base64.b64encode(username.encode(encoding="utf-8")) 	
	_rnd = int(1000 * time.time())	

	session = requests.Session()
	url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su='+str(su)+'&rsakt=mod&client=ssologin.js(v1.4.19)&_='+str(_rnd)	
	url_login = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)'
	
	r = session.get(url)
	rtext = r.text 
	pattern = r'{.*?}'
	list_data = re.findall(pattern,rtext)
	data = json.loads(list_data[0])

	servertime = data['servertime'] 
	nonce = data['nonce']
	pubkey = data['pubkey']
	rsakv = data['rsakv']

	rsaPublickey= int(pubkey,16)  
	key = rsa.PublicKey(rsaPublickey,65537)	
	 
	# calculate sp
	rsaPublickey = int(pubkey, 16)
	key = rsa.PublicKey(rsaPublickey, 65537)
	message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
	sp = binascii.b2a_hex(rsa.encrypt(message.encode(encoding = "utf-8"), key))
	
	postdata = {
	    'entry': 'weibo',
	    'gateway': '1',
	    'from': '',
	    'savestate': '7',
	    'qrcode_flag':'false',
	    'userticket': '1',
	    'ssosimplelogin': '1',
	    'vsnf': '1',
	    #'useticket':'1',
	    'vsnval': '',
	    'su': su,
	    'service': 'miniblog',
	    'servertime': servertime,
	    'nonce': nonce,
	    'pwencode': 'rsa2',
	    'sp': sp,
	    'encoding': 'UTF-8',
	    'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',	    
	    'returntype': 'META',
	    'rsakv': rsakv,
	}
	resp = session.post(url_login, data = postdata)# print resp.headers	
	login_url = re.findall(r'http://weibo.*&retcode=0', resp.text)#
	#print(login_url)

	if len(login_url)<=0:
		print('登录失败了..')
		exit()

	respo = session.get(login_url[0])
	uid = re.findall('"uniqueid":"(\d+)",', respo.text)[0]
	url = "http://weibo.com/u/" + uid
	
	r = session.get(url)
	cookies = session.cookies.get_dict()
	cookie_str = ''
	for item in cookies:
		cookie_str += str(item)+'='+str(cookies[item])+'; '
	cookie_str = cookie_str.rstrip('; ')
	print(cookie_str)
	filename = 'cookie'
	with open(filename,'w') as f:
		f.write(cookie_str)
		print('cookie文件写入成功,写入了'+filename+'文件')

username = config['username']
password = config['password']

preLogin(username,password)