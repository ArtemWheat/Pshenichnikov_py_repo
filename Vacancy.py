from Salary import Salary


class Vacancy:
    """Класс вакансии

    Attributes:
        name (str): Имя
        salary (Salary): Зарплата
        area_name (str): Регион
        published_at (str): Дата публикации
        published_at_year (str): Год публикации
    """

    def __init__(self, dict_vacancy: dict):
        """Инициализирует класс вакансии из словаря вакансии

        :param dict_vacancy: Словарь вакансии
        """
        self.name = dict_vacancy['name']
        if 'salary' in dict_vacancy.keys():
            self.salary = Salary(salary_avg=dict_vacancy['salary'])
        else:
            self.salary = Salary(salary_from=dict_vacancy['salary_from'],
                                 salary_to=dict_vacancy['salary_to'],
                                 salary_currency=dict_vacancy['salary_currency'])
        self.area_name = dict_vacancy['area_name']
        self.published_at = dict_vacancy['published_at']

        # str(parser.parse(dict_vacancy['published_at']).date())
        # '.'.join(str(datetime.datetime.strptime(dict_vacancy['published_at'], '%Y-%m-%dT%H:%M:%S%z').date()).split('-'))

        self.published_at_year = int(self.published_at[:4])
