def get_statistics(language, vacancies_found,
                   vacancies_processed, vacancies_salary):
    if vacancies_processed:
        average_salary = int(vacancies_salary / vacancies_processed)
    else:
        average_salary = 0
    language_statistics = {}
    language_statistics[language] = {
        'vacancies_found': vacancies_found,
        'vacancies_processed': vacancies_processed,
        'average_salary': average_salary
    }
    return language_statistics
