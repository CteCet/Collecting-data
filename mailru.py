from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
from pymongo import MongoClient

import time


client = MongoClient('localhost', 27017)
db = client['mailru']
mr = db.mr_mails


driver = webdriver.Chrome()

driver.get('https://account.mail.ru/login')

elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME,'username')))
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.RETURN)
time.sleep(3)
elem = driver.find_element_by_name('password')
elem.send_keys('NewPassword172')
elem.send_keys(Keys.RETURN)


mails = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,'js-letter-list-item')))
#time.sleep(6)

mail_list = []

while True:
    time.sleep(1)
    mails = driver.find_elements_by_class_name('js-letter-list-item')
    for mail in mails:
        link = mail.get_attribute('href')
        if link not in mail_list:
            mail_list.append(link)
    try:
        last_p = driver.find_element_by_class_name('list-letter-spinner_default')
        break
    except:
        mails = driver.find_elements_by_class_name('js-letter-list-item')
        actions = ActionChains(driver)
        actions.move_to_element(mails[-1])
        actions.perform()

data = []

for mail in mail_list:
    mails = {}
    driver.get(mail)
    mails['author'] = driver.find_element_by_class_name('letter-contact').text
    mails['date'] = driver.find_element_by_class_name('letter__date').text
    mails['subject'] = driver.find_element_by_class_name('thread__subject').text
    letter_body =  driver.find_elements_by_xpath(
        '//div[@class="letter__body"]//td[@style] | //div[@class="letter__body"]//p')

    for info in letter_body:
        info = info.text
    mails['info'] = [info.text for info in letter_body]
    data.append(mails)

mr.insert_many(data)

driver.close()