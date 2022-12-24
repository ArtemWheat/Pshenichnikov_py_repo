currency_to_rub = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
}


class Salary:
    """Класс зарплаты
    Attributes:
        salary_from (int): Оклад 'от'
        salary_to (int): Оклад 'до'
        salary_currency (str): Валюта
    """

    def __init__(self, salary_from, salary_to, salary_currency: str):
        """Инициализация класса зарплаты

        :param salary_from(int, float, str): Оклад 'от'
        :param salary_to(int, float, str): Оклад 'до'
        :param salary_currency: Валюта
        >>> type(Salary(10, 20, 'RUR')).__name__
        'Salary'
        >>> Salary(10.0, 20.0, 'RUR').salary_from
        10
        >>> Salary(10.0, 20.0, 'RUR').salary_to
        20
        >>> Salary(10.0, 20.0, 'RUR').salary_currency
        'RUR'
        """
        self.salary_from = int(float(salary_from))
        self.salary_to = int(float(salary_to))
        if salary_currency not in currency_to_rub.keys():
            raise ValueError('Неверно введна валюта')
        self.salary_currency = salary_currency

    def get_salary_to_rub(self) -> float:
        """Функция подсчета средней ЗП в рублях с помощью словаря currency_to_rub
        :return: Вывод средней ЗП в рублях
        >>> Salary(20.0, 30.0, 'RUR').get_salary_to_rub()
        25.0
        >>> Salary(20.0, 30.0, 'RUR').salary_from
        20
        >>> Salary(20.0, 30.0, 'RUR').salary_to
        30
        >>> Salary(20.0, 30.0, 'EUR').get_salary_to_rub()
        1497.5
        >>> Salary(20, 30.0, 'RUR').get_salary_to_rub()
        25.0
        """
        return currency_to_rub[self.salary_currency] * (float(self.salary_to) + float(self.salary_from)) / 2
