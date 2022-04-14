from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

def get_letters(email='study.ai_172@mail.ru', password='NextPassword172#'):

    options = Options()
    options.add_argument('headless')
    s = Service('./chromedriver')
    driver = webdriver.Chrome(service=s, options=options)
    wait = WebDriverWait(driver, 10)
    driver.get('https://account.mail.ru/login')
    driver.implicitly_wait(2)
    login = driver.find_element(By.XPATH, '//input[@type="text"]')
    login.send_keys(email)
    login.send_keys(Keys.ENTER)

    psw = driver.find_element(By.XPATH, '//input[@type="password"]')
    psw.send_keys('NextPassword172#')
    psw.send_keys(Keys.ENTER)
    driver.implicitly_wait(6)


    refs = []

    print('Собираем ссылки', end='')
    while True:

        elems = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@class,"llc")]')))

        if len(refs) > 0 and len(elems) > 0:
            if refs[-1] == elems[-1].get_attribute("href"):
                break

        for i in elems:
            try:
                refs.append(i.get_attribute("href"))
            except:
                pass

        try:
            actions = ActionChains(driver)
            actions.move_to_element(elems[-1])
            actions.perform()
        except:
            pass

    print(f'\n Ссылок собрано {len(refs)}')
    result = []

    print('Собираем содержимое писем', end='')

    for i in set(refs):



        if i != None:
            letter = {}

            while True:
                try:
                    driver.get(i)
                    letter['ref'] = i

                    letter['id'] = re.findall("/0:(.*):0/", i)[0]

                    elem = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="letter-contact"]')))
                    letter['from'] = elem.get_attribute('title')

                    elem = wait.until(EC.presence_of_element_located((By.XPATH, '//h2[@class="thread-subject"]')))
                    letter['subject'] = elem.text

                    elem = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="letter__date"]')))
                    letter['date'] = elem.text

                    elem = wait.until(
                        EC.presence_of_element_located((By.XPATH, '//div[@class="letter-body__body-content"]')))
                    letter['text'] = elem.text

                    result.append(letter)

                    break

                except:
                    pass

    print(f'\n Собрано писем {len(result)}')

    driver.quit()

    return result


def save_letters(letters_list):
    client = MongoClient('localhost', 27017)
    db = client['letters']
    letters = db.letters


    for i in letters_list:
        if not letters.find_one({'id': i['id']}):
            print('.', end='')
            letters.insert_one(i)



letters = get_letters()

save_letters(letters)