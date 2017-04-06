#!/usr/bin/env python

import random
import string
for _ in range(0,200):
	randChars = '' 
	for _ in range(0,15):
		randChars += random.choice(string.ascii_letters)
	print(randChars)