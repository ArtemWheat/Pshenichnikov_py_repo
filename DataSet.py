import csv
import re
from collections import Counter

from Vacancy import Vacancy


class DataSet:
    """Класс датасета

    Attributes:
        file_name (str): Имя файла
        vacancies_objects (list): Список вакансий
        vacancies_object_name (list): Список вакансий по заданному имени
    """

    def __init__(self, file_name: str, name: str, start: int, end: int):
        """Инициализация класса датасета

        :param file_name: Имя файла
        :param name: Имя искомой профессии
        :param start: С какого года выводить информацию
        :param end: По какой год выводить информацию
        >>> DataSet('Tests/test_data_set.csv', 'аналитик', 2007, 2014).file_name
        'Tests/test_data_set.csv'
        >>> DataSet('Tests/test_data_set.csv', 'администратор', 2007, 2014).vacancies_objects[0].name
        'Менеджер по работе с юридическими лицами'
        >>> DataSet('Tests/test_data_set.csv', 'администратор', 2007, 2014).vacancies_objects_name[0].name
        'Системный администратор'
        """
        self.file_name = file_name
        self.vacancies_objects = []
        self.vacancies_objects_name = []
        data_vac = self.__csv_reader()
        for vacancy in data_vac:
            if not start <= int(vacancy['published_at'][:4]) <= end:
                continue
            self.vacancies_objects.append(Vacancy(vacancy))
            if name in vacancy['name']:
                self.vacancies_objects_name.append(Vacancy(vacancy))

    def filter_by_currency(self, data_vacancies):
        freq_curr = {k: v for k, v in dict(Counter(map(lambda x: x.salary.salary_currency, data_vacancies))).items() if
                     v > 5000}
        data_vacancies = [x for x in data_vacancies if x.salary.salary_currency in list(freq_curr.keys())]

    def __csv_reader(self) -> list:
        """Чтение .csv

        :return: Вывод списка обработанных данных
        """
        with open(self.file_name, encoding='utf-8-sig') as read_file:
            file_reader = csv.reader(read_file, delimiter=",")
            data_vacancies = []
            try:
                titles = next(file_reader)
            except StopIteration:
                print('Пустой файл')
                exit(0)
            html_tags = re.compile('<.*?>')
            for row in file_reader:
                if '' in row or len(row) != len(titles):
                    continue
                self.__csv_filer(html_tags=html_tags,
                                 row=row,
                                 titles=titles)
                if len(row) == len(titles):
                    data_vacancies.append({titles[i]: row[i] for i in range(len(titles))})
            if len(data_vacancies) == 0:
                print('Нет данных')
                exit(0)
            return data_vacancies

    @staticmethod
    def __csv_filer(html_tags, row: list, titles: list):
        """Проверка строки вакансии на правильность и отсев 'неправильных'

        :param html_tags: html теги
        :param row: Строка вакансии
        :param titles: Заголовки
        :return:
        """
        if len(row) < len(titles):
            return
        for i in range(len(row)):
            row[i] = ' '.join(re.sub(html_tags, '', row[i])
                              .strip()
                              .split())