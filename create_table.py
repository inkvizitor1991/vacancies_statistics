from terminaltables import AsciiTable


def create_table(statistics, name):
    table_description = [(
        'Язык программирования ', 'Вакансий найдено',
        'Вакансий обработано', 'Средняя зарплата'
    )]
    for languages in statistics:
        for language in languages:
            vacancies_found, vacancies_processed, average_salary = languages[
                language].values()

            table_description.append((language, vacancies_found,
                                      vacancies_processed, average_salary))

    title = f'{name} Moscow'
    table_instance = AsciiTable(tuple(table_description), title)
    table_instance.justify_columns[2] = 'right'
    return table_instance.table
