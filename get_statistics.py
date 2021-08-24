from __future__ import print_function

import os

import requests
from counts_predict_salary import predict_salary
from create_table import get_statistics
from dotenv import load_dotenv


def predict_rub_salary_hh(vacancy):
    payment = vacancy['salary']
    if payment:
        if payment['currency'] == 'RUR':
            return predict_salary(
                payment['from'],
                payment['from']
            )


def predict_rub_salary_sj(vacancy):
    if vacancy:
        if vacancy['currency'] == 'rub':
            return predict_salary(
                vacancy['payment_from'],
                vacancy['payment_to']
            )


def get_vacancies_hh(pages, languages, api):
    url = 'https://api.hh.ru/vacancies'
    headers = {'X-Api-App-Id': api}
    parsed_vacancies_hh = {}
    for language in languages:
        params = {
            'text': f'Программист {language}',
            'per_page': pages,
            'area': '1',
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        vacancies = response.json()

        salary_all_vacancies = 0
        quantity_vacancies = 0

        for vacancy in vacancies['items']:
            salary = predict_rub_salary_hh(vacancy)

            if salary:
                quantity_vacancies += 1
                salary_all_vacancies += int(salary)

        parsed_vacancies_hh[language] = {
            'vacancies_found': vacancies['found'],
            'vacancies_processed': quantity_vacancies,
            'average_salary': int(salary_all_vacancies / quantity_vacancies)
        }
    return parsed_vacancies_hh


def get_vacancies_sj(pages, languages, api):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': api}
    parsed_vacancies_sj = {}

    for language in languages:
        params = {
            'count': pages,
            'town': 4,
            'keywords': f'Программист {language}'
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        vacancies = response.json()

        salary_all_vacancies = 0
        quantity_vacancies = 0

        for vacancy in vacancies['objects']:
            salary = predict_rub_salary_sj(vacancy)
            if salary:
                quantity_vacancies += 1
                salary_all_vacancies += int(salary)

        parsed_vacancies_sj[language] = {
            'vacancies_found': vacancies['total'],
            'vacancies_processed': quantity_vacancies,
            'average_salary': int(salary_all_vacancies / quantity_vacancies)
        }
    return parsed_vacancies_sj


if __name__ == '__main__':
    load_dotenv()
    api = os.environ['USER_AGENT']
    pages = 100
    title_sj = 'SuperJob'
    title_hh = 'HeadHunter'

    languages = [
        'TypeScript', 'Swift', 'Scala',
        'Shell', 'Go', 'C', 'C++', 'Ruby',
        'JavaScript', 'Java', 'Python'
    ]
    parsed_vacancies_hh = get_vacancies_hh(pages, languages, api)
    parsed_vacancies_sj = get_vacancies_sj(pages, languages, api)

    get_statistics(parsed_vacancies_hh, title_hh)

    get_statistics(parsed_vacancies_sj, title_sj)
