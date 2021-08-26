from terminaltables import AsciiTable


def get_statistics(parsed_vacancies, name):
    statistics = [('Язык программирования ', 'Вакансий найдено',
                   'Вакансий обработано', 'Средняя зарплата')]
    for language in parsed_vacancies:
        statistics.append(
            (language, parsed_vacancies[language]['vacancies_found'],
             parsed_vacancies[language]['vacancies_processed'],
             parsed_vacancies[language]['average_salary']))
    create_table(tuple(statistics), name)


def create_table(statistics, name):
    title = f'{name} Moscow'
    table_instance = AsciiTable(statistics, title)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)
    print()
