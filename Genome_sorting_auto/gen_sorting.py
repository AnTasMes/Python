#THIS FILE IS MADE AS A PART OF A FULL MODULE SYSTEM FOR GENOME DATA GATHERING AUTOMATION 
#NOTE THAT THIS FILE ALONE WORKS ONLY AS A PARTIAL SEGMENT FOR RESOLVING DATAFRAME OF GATHERED DATA
import time
import os.path
from os import path
import pandas as pd
import numpy as np

def while_file_exists(file_dir, file_name):
	cntr = 1
	file_path = file_dir+file_name
	exists = path.exists(file_path)
	extension = '.'+file_name.split('.')[1]
	file_name =  file_name.strip(extension)
	while exists:
		file_path = file_dir+file_name+str(cntr)+extension #add numbers till file not found
		exists = path.exists(file_path)
		cntr += 1
	return file_path

def wait_for_file(file, TTL):
	exists = path.exists(file)
	while not exists and TTL>=0: #Waiting for gen.txt to come up
		TTL -= 1
		time.sleep(2)
		print(f"Waiting for {file} .....") #wait for file to get downloaded
		exists = path.exists(file)
		pass
	return exists

def sort(file_data):
	column_names = []
	for x in range(len(file_data[0])):
			column_names.append(file_data[0][x])
	#Sorting and filtering DataFrame
	df = pd.DataFrame(file_data, columns=column_names).iloc[1:] #set dataFrame without first line
	df['txStart'] = pd.to_numeric(df['txStart']) #make tx numeric
	df['txEnd'] = pd.to_numeric(df['txEnd'])
	df = df[~df['chrom'].str.contains('alt')] #does not contain alt (remove alt from dataFrame)
	df['txCount'] = df['txEnd']-df['txStart'] #calc tx 

	df = df.sort_values(by=["chrom", "txStart"], ascending=True)
	return df

def make_excel(df, file_name):
	output_file_name = while_file_exists('',file_name)
	writer = pd.ExcelWriter(output_file_name)
	try:
		df.to_excel(writer)
		writer.save()
		print(f"{output_file_name} has been created")
	except:
		print("There was an error while creating a file")


