from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import json


client = MongoClient('localhost', 27017)
db = client['mvideo']
mv = db.mvideo_hits

driver = webdriver.Chrome()

driver.get('https://www.mvideo.ru/')


hits = driver.find_elements_by_xpath("//div[contains(@class, 'sel-hits-block')]")

# driver.execute_script("arguments[0].scrollIntoView();",hits)
actions = ActionChains(driver)
actions.move_to_element(hits[1])
actions.perform()

while True:
    try:
        button = driver.find_element_by_xpath(
            '//div[@class="gallery-layout"][2]//a[@class = "next-btn sel-hits-button-next"]')
    except:
        break
    actions.move_to_element(button).click().perform()


goods = driver.find_elements_by_xpath("//div[@class='gallery-layout'][2]//li[contains(@class, 'gallery-list-item')]//h4/a")
for good in goods:
    good = good.get_attribute('data-product-info')
    good = json.loads(good)
    print(good)
    mv.insert_one(good)

driver.close()