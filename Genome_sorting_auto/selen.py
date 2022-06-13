import sys
import time
import keyboard
#from Setting import Settings
#from Setting import SettingArrays
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def start(url):
	try:
		driver = webdriver.Firefox();
		driver.get(url)
	except Exception as e:
		print(e)
		sys.exit()
	return driver

def wait_until_avail(elem, ref, driver):
	if ref == 'name':
		elem = WebDriverWait(driver, 2).until(
			EC.presence_of_element_located((By.NAME, elem)))
	elif ref == 'id':
		elem = WebDriverWait(driver, 2).until(
			EC.presence_of_element_located((By.ID, elem)))

def found_div(driver):
	found_div = 0
	try:
		found_div = driver.find_element_by_xpath("//div[@id='warnBox'][@style='width: 65%;']")
		print(f"Error_div_state: {found_div}")
	except Exception as e:
		print(f"Error_div_state: {found_div}")
	return bool(found_div)

def input_key(text_box, key_array):
	line_num = 0
	for key in range(len(key_array)):
		text_box.send_keys(key_array[line_num])
		keyboard.press_and_release('enter')
		line_num += 1

#ovde mora da se doda da se default baza uzima iz set fajla
#srediti da se baza menja po klasi
def first_phase(driver, key_array, database, table):
	try:
		wait_until_avail('hgta_track', 'id', driver)
		driver.find_element_by_xpath(f"//select[@id='hgta_track']/option[@value='{database}']").click()
		wait_until_avail('hgta_table', 'id', driver)
		driver.find_element_by_xpath(f"//select[@id='hgta_table']/option[@value='{table}']").click()
		wait_until_avail('hgta_regionType_genome', 'id', driver)
		driver.find_element_by_id('hgta_regionType_genome').click()
		driver.find_element_by_id('hgta_doPasteIdentifiers').click()
		wait_until_avail('hgta_pastedIdentifiers', 'name', driver)
		text_box = driver.find_element_by_name('hgta_pastedIdentifiers')
		input_key(text_box, key_array)
		driver.find_element_by_name('hgta_doPastedIdentiers').click()
	except Exception as e:
		print(e)
		driver.quit()
		sys.exit()

def second_phase(driver, file_name):
	try:
		wait_until_avail('outputTypeDropdown', 'id', driver)
		driver.find_element_by_xpath(f"//select[@id='outputTypeDropdown']/option[@value='selectedFields']").click()
		wait_until_avail('hgta_outFileName', 'id', driver)
		driver.find_element_by_id('hgta_outFileName').send_keys(file_name)
		driver.find_element_by_id('hgta_doTopSubmit').click()
	except Exception as e:
		print(e)
		driver.quit()
		sys.exit()

def check(driver, table, check_name):
	for name in check_name:
		try: #find all checkboxes
			driver.find_element_by_name(f'hgta_fs.check.hg38.{table}.{name}').click()
		except Exception as e:
			print(e) #list checkboxes not found (varies per database)

def save_file(driver):
	wait_until_avail('hgta_doPrintSelectedFields', 'id', driver)
	driver.find_element_by_id('hgta_doPrintSelectedFields').click() #get output click
	#time.sleep(1)
	keyboard.press_and_release('down') #saving popup
	time.sleep(1)
	keyboard.press_and_release('enter')
	driver.quit()
