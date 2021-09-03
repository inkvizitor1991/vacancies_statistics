from terminaltables import AsciiTable


def create_table(statistics, name):
    table_rows = [(
        'Язык программирования ', 'Вакансий найдено',
        'Вакансий обработано', 'Средняя зарплата'
    )]

    for language, language_statistics in statistics.items():
        vacancies_found, vacancies_processed, average_salary = language_statistics.values()
        table_rows.append((language, vacancies_found,
                           vacancies_processed, average_salary))

    title = f'{name} Moscow'
    table_instance = AsciiTable(table_rows, title)
    table_instance.justify_columns[2] = 'right'
    return table_instance.table
