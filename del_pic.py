#!/usr/bin/env python

import os

for root,dirs,files in os.walk('.'):
	#print(files)
	for file in files:
		if file.endswith('.jpg') :
			os.remove(root+'/'+file)