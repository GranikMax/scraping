import json
import re
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import time
import hashlib
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
client = MongoClient('localhost', 27017)

db = client['lesson_3_1']
vacancy_db = db.vacancy

vacancy_name = 'Python' #input('Введите Вакансию : ')
base_url = 'https://hh.ru'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}

response = requests.get(base_url + '/search/vacancy?area=1&fromSearchLine=true&text='+vacancy_name+'&page=0&hhtmFrom=vacancy_search_list', headers=headers)

dom = bs(response.text, 'html.parser')
vacancys = dom.find_all("div", {'class': 'vacancy-serp-item'})
def max_num():
    mxnum = 0
    for item in dom.find_all('a', {'data-qa': 'pager-page'}):
        mxnum = list(item.strings)[0].split(" ")[-1]
    return mxnum

max_page = int(max_num())

def data_collect(pages):

    for page in range(pages):
        url2 = base_url +'/search/vacancy?area=1&fromSearchLine=true&text=python&page={page}&hhtmFrom=vacancy_search_list'
        response2 = requests.get(url2, headers=headers)
        dom2 = bs(response2.text, 'html.parser')
        vacancys2 = dom2.find_all('div', {'class': 'vacancy-serp-item'})
        for vacancy in vacancys2:
            vacancy_data = {}
            vacancy_link = vacancy.find('a',{'class':'bloko-link'})['href']
        for vacancy in vacancys2:
            vacancy_name_element = vacancy.find('span', {'class': 'g-user-content'})
            vacancy_name = vacancy_name_element.getText() if vacancy_name_element else "Нет описания"
            vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            vacancy_salary_data = {'min_salary': '', 'max_salary': '', 'currency': ''}
            if vacancy_salary is None:
               vacancy_salary_data['min_salary'] = 'None'
               vacancy_salary_data['max_salary'] = 'None'
               vacancy_salary_data['currency'] = 'None'
            else:
               vacancy_salary = vacancy_salary.text.replace("\u202f", '').split()
               if 'от' in vacancy_salary:
                   if 'руб.' in vacancy_salary:
                       vacancy_salary_data['min_salary'] = int(vacancy_salary[1])
                       vacancy_salary_data['max_salary'] = 'None'
                       vacancy_salary_data['currency'] = 'руб.'
                   if 'USD' in vacancy_salary:
                       vacancy_salary_data['min_salary'] = int(vacancy_salary[1])
                       vacancy_salary_data['max_salary'] = 'None'
                       vacancy_salary_data['currency'] = 'USD'
               if 'до' in vacancy_salary:
                    if 'руб.' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = 'None'
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[1])
                        vacancy_salary_data['currency'] = 'руб.'
                    if 'USD' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = 'None'
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[1])
                        vacancy_salary_data['currency'] = 'USD'
               if 'от' not in vacancy_salary and 'до' not in vacancy_salary:
                    if 'руб.' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = int(vacancy_salary[0])
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[2])
                        vacancy_salary_data['currency'] = 'руб.'
                    if 'USD' in vacancy_salary:
                        vacancy_salary_data['min_salary'] = int(vacancy_salary[0])
                        vacancy_salary_data['max_salary'] = int(vacancy_salary[2])
                        vacancy_salary_data['currency'] = 'USD'


            hash_link = hashlib.sha224(vacancy_link.encode())
            link_hex = hash_link.hexdigest()
            vacancy_data['_id'] = link_hex
            vacancy_data['name'] = vacancy_name
            vacancy_data['link'] = vacancy_link
            vacancy_data['salary'] = vacancy_salary

            try:
                vacancy_db.insert_one(vacancy_data)
            except DuplicateKeyError:
                print(f"Document with id = {link_hex} already exists")


data = data_collect(max_page)












