import keyboard
import sys
from os import path
from selenium import webdriver
#file = open("sifre.txt","r")


def if_fexist(file):
	exists = path.exists(file)
	if not exists:
		print(f"File: {file} does not exist")
		sys.exit()
	return exists

def get_lines(file):
	key_array = []
	for line in file:
		line = line.strip('\n')
		line = line.split()
		key_array.append(line)
	return key_array

#print("LINE NUMBER: ",len(key_array))

def get_settings(file):
	sets = {}
	try:	
		for line in file:
			line = line.strip('\n')
			line = line.replace(' ','')
			line = line.split('=')
			if line[0] == '' or line[0].startswith('#'):
				continue
			sets[line[0]] = line[1]
		for elem in sets: #Resolving multiple values per key in settings.txt
			if sets[elem].startswith('{'):
				sets[elem] = sets[elem].strip('{}')				
				sets[elem] = sets[elem].split(',')
		return sets
	except Exception as e:
		print(e,f": Check your settings.txt file : {line}")
		sys.exit()
#print(value)
#print(file.read())