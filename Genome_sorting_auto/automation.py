from os import path
import os.path
import time
import selen
import file_read as fr
import gen_sorting as gs

set_file_name = 'settings.txt'
pw_file_name = 'sifre.txt'

#initial loading
try: #loading files and puts them into sets
	set_file = open(set_file_name)
	pw_file = open(pw_file_name)
	sets = fr.get_settings(set_file) #settings file
	pw = fr.get_lines(pw_file) #pw file
except Exception as e:
	print(e)

if __name__ == '__main__':	
	print("-------- :Starting: --------")

	MAX_DATABASE = len(sets['database']) #getting the number of given databases
	FILE_PATH = sets['dwnld_dir'] +'\\'+ sets['file_name']
	DELETE_FILE = int(sets['delete_dwnld_file'])

	print("-------- :Opening browser: --------")

	driver = selen.start(sets['URL'])
	selen.first_phase(driver, pw, sets['database'][0], sets['table'][0])

	print("-------- :Checking for errors: --------")
	time.sleep(2)
	div = selen.found_div(driver)
	cntr = 0
	while div and MAX_DATABASE-1 > cntr:
		cntr += 1	
		try: #if div was found (check other DBs)
			selen.first_phase(driver, pw, sets['database'][cntr], sets['table'][cntr])
			div = selen.found_div(driver) #check for div again
		except Exception as e:
			print(e)
			quit()

	selen.second_phase(driver, sets['file_name']) #start the second phase of loading
	selen.check(driver, sets['table'][cntr], sets['check']) #checkboxes 
	selen.save_file(driver) #save file 

	print(f"-------- :Downloading file {sets['file_name']}: --------")

	output_file = open(FILE_PATH, 'r')

	exists = gs.wait_for_file(FILE_PATH, int(sets['TTL']))
	if exists:
		print("-------- :Sorting data: --------")
		try:
			file_data = fr.get_lines(output_file)
			df = gs.sort(file_data)
			gs.make_excel(df, sets['output_file_name'])
			output_file.close()
			if DELETE_FILE:
				os.remove(FILE_PATH)
			else:
				print(f"File {sets['file_name']} was not deleted and can be found at {sets['dwnld_dir']}")
		except Exception as e:
			output_file.close()
			print(e)

	