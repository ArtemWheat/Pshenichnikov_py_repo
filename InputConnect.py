import csv
import math
import os

from prettytable import PrettyTable, ALL

all_titles_table = ["№", "Название", "Оклад", "Название региона", "Дата публикации вакансии"]

dict_slr_currency = {
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум"
}


class InputConnect:
    """Класс ввода с консоли и вывода таблицы в консоль

    Attributes:
        file_name (str): Имя файла
        name (str): Искомое имя
        __dict_formatter_for_full_slr (dict): Словарь функций предобработки вакансий для вывода таблицы
    """

    def __init__(self):
        """Инициализация класса InputConnect"""
        self.file_name = self.__processing_file_name('Resources/' + input('Введите название файла: '))
        self.name = input('Введите название профессии: ')
        self.__dict_formatter_for_full_slr = {
            'Название': lambda row: row.name,
            'Оклад': lambda
                row: f'{self.__slr_format(row.salary.salary_from)} - {self.__slr_format(row.salary.salary_to)} ' \
                     f'({dict_slr_currency[row.salary.salary_currency]}) ',
            'Название региона': lambda row: row.area_name,
            'Дата публикации вакансии': lambda row: '.'.join(reversed(row.published_at[0:10].split('-')))
        }
        self.__dict_formatter_for_small_slr = {
            'Название': lambda row: row.name,
            'Оклад': lambda row: row.salary.salary_avg,
            'Название региона': lambda row: row.area_name,
            'Дата публикации вакансии': lambda row: '.'.join(reversed(row.published_at[0:10].split('-')))
        }

    @staticmethod
    def __processing_file_name(file_name: str) -> str:
        """Обработка ввода имени файла

        :param file_name: Имя файла
        :return: Имя файла
        """
        if os.stat(file_name).st_size == 0:
            print('Пустой файл')
            exit(0)
        return file_name

    @staticmethod
    def __slr_format(slr: str) -> str:
        """Форматирование ЗП для данных таблицы

        :param slr: Зарплата 'от' или 'до'
        :return: Преобразованная ЗП
        """
        return '{:,}'.format(math.floor(float(slr))).replace(',', ' ')

    def table_print(self, data_vacancies: list, is_full_slr=True):
        """Вывод в консоль таблицы

        :param data_vacancies: Список вакансий
        :return:
        """
        counter = 1
        table = PrettyTable()
        table.hrules = ALL
        table.align = 'l'
        table.field_names = all_titles_table
        for title in table.field_names:
            table.max_width[title] = 20
        for value in data_vacancies:
            temp_array = [counter]
            for v in all_titles_table[1:]:
                if is_full_slr:
                    temp = self.__dict_formatter_for_full_slr[v](value)
                else:
                    temp = self.__dict_formatter_for_small_slr[v](value)
                temp_array.append(temp if len(str(temp)) < 100 else str(temp)[:100] + '...')
            table.add_row(temp_array)
            counter += 1
        print(table.get_string(fields=all_titles_table))

    def split(self, delimiter=',', output_path='csv_files_by_year'): #TODO переделать в вид без чтения
        with open(self.file_name, encoding='utf-8-sig') as read_file:
            file_reader = csv.reader(read_file, delimiter=delimiter)
            try:
                titles = next(file_reader)
            except StopIteration:
                print('Пустой файл')
                exit(0)

            first_row = next(file_reader)
            current_year = first_row[titles.index('published_at')][2:4]
            current_out_path = output_path + '/' + current_year + '.csv'
            file_names = [current_out_path]
            current_out_writer = csv.writer(open(current_out_path, 'w', encoding='utf-8-sig'),
                                            delimiter=delimiter,
                                            lineterminator="\r")
            current_out_writer.writerow(titles)
            current_out_writer.writerow(first_row)
            for row in file_reader:
                if row[titles.index('published_at')][2:4] != current_year:
                    current_year = row[titles.index('published_at')][2:4]
                    current_out_path = output_path + '/' + current_year + '.csv'
                    file_names.append(current_out_path)
                    current_out_writer = csv.writer(open(current_out_path, 'w', encoding='utf-8-sig'),
                                                    delimiter=delimiter,
                                                    lineterminator="\r")
                    current_out_writer.writerow(titles)
                    current_out_writer.writerow(row)
                else:
                    current_out_writer.writerow(row)
            return file_names
