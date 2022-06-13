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


def start(url):
    try:
        driver = webdriver.Edge()
        driver.get(url)
        time.sleep(5)
    except Exception as e:
        print(e)
        sys.exit()
    return driver


def genMails(path: str):
    names = json.loads(open('names.json').read())
    mails = json.loads(open('sufix.json').read())

    chars = string.ascii_letters + string.digits + '.'

    # print(len(names))
    m_list = []
    while len(m_list) < 200:
        fName = names[random.randint(0, len(names)-1)].split()[0]
        lName = names[random.randint(0, len(names)-1)].split()[1]
        mail = fName + random.choice(chars) + lName + random.choice(mails)
        m_list.append({
            'ime': fName,
            'prezime': lName,
            'mail': mail
        })

    json_str = json.dumps(m_list)

    with open(path, 'w+') as json_file:
        json_file.write(json_str)


def outputMail(path):
    return json.loads(open(path).read())


if __name__ == '__main__':
    genMails('output.json')
    people = outputMail('output.json')

    for person in people:
        driver = start(
            'https://peticije.kreni-promeni.org/petitions/oduzeti-dozvolu-pink-u-i-happy-u?source=homepage')

        textbox_ime = driver.find_element(By.ID, 'signature-first-name-field')
        textbox_prezime = driver.find_element(By.ID,
                                              'signature-last-name-field')
        textbox_email = driver.find_element(By.ID, 'signature-email')
        textbox_postcode = driver.find_element(By.ID, 'signature-postcode')
        button = driver.find_element(
            By.XPATH, '//button[@type="submit" and @class="btn btn-primary btn btn-primary btn-lg btn-block"]')

        textbox_ime.send_keys(person['ime'])
        textbox_prezime.send_keys(person['prezime'])
        textbox_email.send_keys(person['mail'])
        textbox_postcode.send_keys('11000')

        button.click()
        time.sleep(5)
        driver.close()

    time.sleep(10)
