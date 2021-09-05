import os

import requests

from dotenv import load_dotenv

from counts_predict_salary import predict_salary
from create_table import create_table
from collects_language_statistics import get_statistics


def predict_rub_salary_hh(vacancy):
    payment = vacancy['salary']
    if payment and payment['currency'] == 'RUR':
        return predict_salary(
            payment['from'],
            payment['to']
        )


def predict_rub_salary_sj(vacancy):
    if vacancy and vacancy['currency'] == 'rub':
        return predict_salary(
            vacancy['payment_from'],
            vacancy['payment_to']
        )


def get_vacancies_hh(language):
    moscow = 1
    all_vacancies_period = 30
    vacancies_on_page = 50
    language_vacancies = []
    url = 'https://api.hh.ru/vacancies'
    pages_number = 40
    page = 0
    while page < pages_number:
        params = {
            'page': page,
            'text': f'Программист {language}',
            'per_page': vacancies_on_page,
            'period': all_vacancies_period,
            'area': moscow,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        vacancies = response.json()
        language_vacancies.append(vacancies)
        pages_number = response.json()['pages']
        page += 1
    return language_vacancies


def parse_vacancies_hh(language_vacancies):
    vacancies_salary = 0
    vacancies_processed = 0
    vacancies_found = 0
    for vacancies in language_vacancies:
        vacancies_found = vacancies['found']
        for vacancy in vacancies['items']:
            salary = predict_rub_salary_hh(vacancy)
            if salary:
                vacancies_processed += 1
                vacancies_salary += int(salary)
    return vacancies_found, vacancies_processed, vacancies_salary


def get_vacancies_sj(language, api):
    moscow = 4
    vacancies_on_page = 100
    all_vacancies_period = 0
    language_vacancies = []
    url = 'https://api.superjob.ru/2.0/vacancies/'
    pages_number = 5
    page = 0
    while page < pages_number:
        headers = {'X-Api-App-Id': api}
        params = {
            'page': page,
            'count': vacancies_on_page,
            'town': moscow,
            'period': all_vacancies_period,
            'keywords': f'Программист {language}'
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        vacancies = response.json()
        language_vacancies.append(vacancies)
        pages_number = response.json()['more']
        page += 1
    return language_vacancies


def parse_vacancies_sj(language_vacancies):
    vacancies_salary = 0
    vacancies_processed = 0
    vacancies_found = 0
    for vacancies in language_vacancies:
        vacancies_found = vacancies['total']
        for vacancy in vacancies['objects']:
            salary = predict_rub_salary_sj(vacancy)
            if salary:
                vacancies_processed += 1
                vacancies_salary += int(salary)
    return vacancies_found, vacancies_processed, vacancies_salary


if __name__ == '__main__':
    load_dotenv()
    api = os.environ['SUPERJOB_TOKEN']
    sj_title = 'SuperJob'
    hh_title = 'HeadHunter'

    languages = [
        'TypeScript', 'Swift', 'Scala',
        'Shell', 'Go', 'C', 'C++', 'Ruby',
        'JavaScript', 'Java', 'Python'
    ]

    hh_statistics = {}
    sj_statistics = {}
    for language in languages:
        hh_language_vacancies = get_vacancies_hh(language)
        vacancies_found, vacancies_processed, vacancies_salary = parse_vacancies_hh(
            hh_language_vacancies
        )
        hh_language_statistics = get_statistics(
            language, vacancies_found,
            vacancies_processed, vacancies_salary
        )
        hh_statistics.update(hh_language_statistics)

        sj_language_vacancies = get_vacancies_sj(language, api)
        vacancies_found, vacancies_processed, vacancies_salary = parse_vacancies_sj(
            sj_language_vacancies
        )
        sj_language_statistics = get_statistics(
            language, vacancies_found,
            vacancies_processed, vacancies_salary)
        sj_statistics.update(sj_language_statistics)

    hh_table = create_table(hh_statistics, hh_title)
    sj_table = create_table(sj_statistics, sj_title)
    print(hh_table)
    print(sj_table)
