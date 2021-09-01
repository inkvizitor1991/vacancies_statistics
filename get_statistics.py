from __future__ import print_function

import os

from counts_predict_salary import predict_salary

from create_table import create_table

from dotenv import load_dotenv

import requests


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


def get_vacancies_hh(HH_ALL_VACANCIES, HH_MOSCOW, pages, languages, api):
    url = 'https://api.hh.ru/vacancies'
    headers = {'X-Api-App-Id': api}

    params = {
        'text': f'Программист {language}',
        'per_page': pages,
        'period': HH_ALL_VACANCIES,
        'area': HH_MOSCOW,
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    vacancies = response.json()
    return vacancies


def parse_vacancies_hh(vacancies, language):
    parsed_vacancies = {}
    vacancies_salary = 0
    vacancies_quantity = 0
    for vacancy in vacancies['items']:
        salary = predict_rub_salary_hh(vacancy)
        if salary:
            vacancies_quantity += 1
            vacancies_salary += int(salary)

            parsed_vacancies[language] = {
                'vacancies_found': vacancies['found'],
                'vacancies_processed': vacancies_quantity,
                'average_salary': int(vacancies_salary / vacancies_quantity)
            }
    return parsed_vacancies


def get_vacancies_sj(SJ_ALL_VACANCIES, SJ_MOSCOW, pages, language, api):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': api}

    params = {
        'count': pages,
        'town': SJ_MOSCOW,
        'period': SJ_ALL_VACANCIES,
        'keywords': f'Программист {language}'
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    vacancies = response.json()
    return vacancies


def parse_vacancies_sj(vacancies, language):
    parsed_vacancies = {}
    vacancies_salary = 0
    vacancies_quantity = 0
    for vacancy in vacancies['objects']:
        salary = predict_rub_salary_sj(vacancy)
        if salary:
            vacancies_quantity += 1
            vacancies_salary += int(salary)

            parsed_vacancies[language] = {
                'vacancies_found': vacancies['total'],
                'vacancies_processed': vacancies_quantity,
                'average_salary': int(vacancies_salary / vacancies_quantity)
            }
    return parsed_vacancies


if __name__ == '__main__':
    load_dotenv()

    SJ_MOSCOW = 4
    HH_MOSCOW = 1
    SJ_ALL_VACANCIES = 0
    HH_ALL_VACANCIES = 30

    api = os.environ['USER_AGENT']
    pages = 100
    sj_title = 'SuperJob'
    hh_title = 'HeadHunter'

    languages = [
        'TypeScript', 'Swift', 'Scala',
        'Shell', 'Go', 'C', 'C++', 'Ruby',
        'JavaScript', 'Java', 'Python'
    ]

    hh_statistics = []
    sj_statistics = []
    for language in languages:
        hh_vacancies = get_vacancies_hh(
            HH_ALL_VACANCIES, HH_MOSCOW, pages, language, api
        )
        hh_parsed_vacancies = parse_vacancies_hh(hh_vacancies, language)
        hh_statistics.append(hh_parsed_vacancies)

        sj_vacancies = get_vacancies_sj(
            SJ_ALL_VACANCIES, SJ_MOSCOW, pages, language, api
        )
        sj_parsed_vacancies = parse_vacancies_sj(sj_vacancies, language)
        sj_statistics.append(sj_parsed_vacancies)

    hh_table = create_table(hh_statistics, hh_title)
    sj_table = create_table(sj_statistics, sj_title)
    print(hh_table)
    print(sj_table)
