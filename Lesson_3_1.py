from pprint import pprint
from pymongo import MongoClient
client = MongoClient('127.0.0.1', 27017)
db = client['lesson_3_1']
vacancy_db = db.vacancy

def find_me_job(min_salary=None):
    if not min_salary:
        min_salary = int(input('Укажите минимальный размер зарплаты: '))
    find_dict = {'$or': [{'min_salary': {'$gte': min_salary}},
                         {'max_salary': {'$gte': min_salary}}]}
    show_dict = {'_id': 0, 'source': 0}
    result = vacancy_db.find(find_dict, show_dict)
    print(f'Найдено {vacancy_db.count_documents(find_dict)} '
          f'вакансий с зарплатой от {min_salary}.')
    for n in result:
        pprint(n)


find_me_job()


