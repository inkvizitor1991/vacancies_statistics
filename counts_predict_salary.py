def predict_salary(salary_from, salary_to):
    salary = 0
    if salary_from and salary_to:
        salary += (salary_from + salary_to) / 2
    elif salary_from:
        salary += salary_from * 1.2
    elif salary_to:
        salary += salary_to * 0.8
    return salary
