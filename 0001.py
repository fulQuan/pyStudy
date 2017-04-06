#!/usr/bin/env python

import random
import string
for i in range(0,200):
	randChars = '' 
	for j in range(0,15):
		randChars += random.choice(string.ascii_letters)
	print(randChars)

