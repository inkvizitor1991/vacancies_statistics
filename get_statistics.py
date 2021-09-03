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
            payment['from']
        )


def predict_rub_salary_sj(vacancy):
    if vacancy and vacancy['currency'] == 'rub':
        return predict_salary(
            vacancy['payment_from'],
            vacancy['payment_to']
        )


def get_vacancies_hh(vacancies_on_page, language):
    moscow = 1
    all_vacancies_period = 30
    url = 'https://api.hh.ru/vacancies'

    params = {
        'text': f'Программист {language}',
        'per_page': vacancies_on_page,
        'period': all_vacancies_period,
        'area': moscow,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    vacancies = response.json()
    return vacancies


def parse_vacancies_hh(vacancies):
    vacancies_salary = 0
    vacancies_processed = 0
    vacancies_found = vacancies['found']
    for vacancy in vacancies['items']:
        salary = predict_rub_salary_hh(vacancy)
        if salary:
            vacancies_processed += 1
            vacancies_salary += int(salary)
    return vacancies_found, vacancies_processed, vacancies_salary


def get_vacancies_sj(vacancies_on_page, language, api):
    moscow = 4
    all_vacancies_period = 0
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': api}

    params = {
        'count': vacancies_on_page,
        'town': moscow,
        'period': all_vacancies_period,
        'keywords': f'Программист {language}'
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    vacancies = response.json()
    return vacancies


def parse_vacancies_sj(vacancies):
    vacancies_salary = 0
    vacancies_processed = 0
    vacancies_found = vacancies['total']
    for vacancy in vacancies['objects']:
        salary = predict_rub_salary_sj(vacancy)
        if salary:
            vacancies_processed += 1
            vacancies_salary += int(salary)
    return vacancies_found, vacancies_processed, vacancies_salary


if __name__ == '__main__':
    load_dotenv()
    api = os.environ['USER_AGENT']
    vacancies_on_page = 100
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
        hh_vacancies = get_vacancies_hh(vacancies_on_page, language)
        vacancies_found, vacancies_processed, vacancies_salary = parse_vacancies_hh(
            hh_vacancies
        )
        hh_language_statistics = get_statistics(
            language, vacancies_found,
            vacancies_processed, vacancies_salary
        )
        hh_statistics.update(hh_language_statistics)

        sj_vacancies = get_vacancies_sj(vacancies_on_page, language, api)
        vacancies_found, vacancies_processed, vacancies_salary = parse_vacancies_sj(
            sj_vacancies
        )
        sj_language_statistics = get_statistics(
            language, vacancies_found,
            vacancies_processed, vacancies_salary)
        sj_statistics.update(sj_language_statistics
                             )

    hh_table = create_table(hh_statistics, hh_title)
    sj_table = create_table(sj_statistics, sj_title)
    print(hh_table)
    print(sj_table)
