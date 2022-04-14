import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
db_mvideo = db.db_mvideo

options = Options()
options.add_argument('start-maximized')
s = Service('./chromedriver')
driver = webdriver.Chrome(service=s, options=options)
driver.get('https://www.mvideo.ru/')


actions = ActionChains(driver)
actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).perform()
wait = WebDriverWait(driver, 10)
button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'В тренде')]")))
button.click()

names = driver.find_elements(By.XPATH, "//h1[@class='title']")
links = driver.find_elements(By.XPATH, "//mvid-shelf-group//a[@class='img-with-badge ng-star-inserted']")
prices = driver.find_elements(By.XPATH, "//span[@class='price__main-value']")

for j in range(0):
    mvideo_data = {'_id': names[j].text,
                   'link': links[j].get_attribute('href'),
                   'prices': prices[j],
                                      }
    try:
        db_mvideo.insert_one(mvideo_data)
    except DuplicateKeyError:
        pass

for doc in db_mvideo.find({}):
    pprint(doc)

driver.quit()