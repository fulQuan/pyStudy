#!/usr/bin/env python

import pymysql
import random
import string

db = pymysql.connect('localhost','root','good4399','test')
cursor = db.cursor()
table = 'codes'

for i in range(0,200):
	randChars = '' 
	for j in range(0,15):
		randChars += random.choice(string.ascii_letters)
	#print(randChars)
	sql = 'insert into ' + table + '(code) values("'+randChars+'")'
	cursor.execute(sql)
	db.commit()	



