#https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text=&page=0&hhtmFrom=vacancy_search_list

import re
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import time
page = 0
vacancy = 'Python'
base_url = 'https://hh.ru'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}

#Получаем данные в HTML
#while True:
#    response = requests.get(base_url + '/search/vacancy?area=1&fromSearchLine=true&text='+vacancy+'&page=' + str(page)+'&hhtmFrom=vacancy_search_list', headers=headers)

#    if page<40:
#        page += 1
#        with open('response.html', 'a', encoding='utf-8') as f:
#           f.write(response.text)
#    else:
#        break
html_file = ''
with open('response.html', 'r', encoding='utf-8') as f:
    html_file = f.read()

dom = bs(html_file, 'html.parser')

vacancys = dom.find_all("div", {'class': 'vacancy-serp-item'})
vacancys_list = []
for vacancy in vacancys:
    vacancy_data = {}
    vacancy_link = vacancy.find('a',{'class':'bloko-link'})['href']
    vacancy_name = vacancy.find('span', {'class': 'g-user-content'}).getText()
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

    vacancy_data['name'] = vacancy_name
    vacancy_data['link'] = vacancy_link
    vacancy_data['salary'] = vacancy_salary
    vacancys_list.append(vacancy_data)

pprint(vacancys_list)