import sys
import json
import random
import string
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def start(url: str, load_time: int):
    try:
        driver = webdriver.Edge()
        driver.get(url)
        time.sleep(load_time)
    except Exception as e:
        print(e)
        sys.exit()
    return driver


def genMails(path: str, record_count: int, names_path: str = 'names.json', mails_path: str = 'sufix.json'):
    # get names and mails from json files
    names = json.loads(open(names_path, encoding='utf-8').read())
    mails = json.loads(open(mails_path, encoding='utf-8').read())

    chars = string.ascii_letters + string.digits + '.'

    # print(len(names))
    m_list = []
    while len(m_list) < record_count:
        # generate random combination of names and lastnames
        fName = names[random.randint(0, len(names)-1)].split()[0]
        lName = names[random.randint(0, len(names)-1)].split()[1]
        mail = fName + random.choice(chars) + lName + random.choice(mails)
        m_list.append({
            'first_name': fName,
            'last_name': lName,
            'email': mail
        })

    json_str = json.dumps(m_list)

    # writes to json of people
    with open(path, 'w+', encoding='utf-8') as json_file:
        json_file.write(json_str)


if __name__ == '__main__':
    genMails('output.json', 500)
    people = json.loads(open('output.json', encoding='utf-8').read())

    for person in people:
        driver = start(
            'https://peticije.kreni-promeni.org/petitions/oduzeti-dozvolu-pink-u-i-happy-u?source=homepage', 5)

        textbox_ime = driver.find_element(By.ID, 'signature-first-name-field')
        textbox_prezime = driver.find_element(By.ID,
                                              'signature-last-name-field')
        textbox_email = driver.find_element(By.ID, 'signature-email')
        textbox_postcode = driver.find_element(By.ID, 'signature-postcode')
        button = driver.find_element(
            By.XPATH, '//button[@type="submit" and @class="btn btn-primary btn btn-primary btn-lg btn-block"]')

        textbox_ime.send_keys(person['first_name'])
        textbox_prezime.send_keys(person['last_name'])
        textbox_email.send_keys(person['email'])
        textbox_postcode.send_keys('11000')

        button.click()
        time.sleep(5)
        driver.close()

    time.sleep(10)
