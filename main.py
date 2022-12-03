import csv
import math
import os
import re
from collections import Counter
from itertools import islice
import matplotlib.pyplot as plt
import numpy as np
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side
from jinja2 import FileSystemLoader, Environment
import pdfkit
from prettytable import PrettyTable, ALL

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

all_titles_table = ["№", "Название", "Оклад", "Название региона", "Дата публикации вакансии"]

dict_experince_format = {
    "noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет"
}

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


class Vacancy:
    def __init__(self, dict_vacancy: dict):
        self.name = dict_vacancy['name']
        self.salary = Salary(salary_from=dict_vacancy['salary_from'],
                             salary_to=dict_vacancy['salary_to'],
                             salary_currency=dict_vacancy['salary_currency'])
        self.area_name = dict_vacancy['area_name']
        self.published_at = dict_vacancy['published_at']
        self.published_at_year = int(self.published_at[:4])


class Salary:
    def __init__(self, salary_from: str, salary_to: str, salary_currency: str):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.salary_avg = currency_to_rub[salary_currency] * (float(salary_to) + float(salary_from)) / 2


class DataSet:
    def __init__(self, file_name: str, name: str, start: int, end: int):
        self.file_name = file_name
        self.vacancies_objects = []
        self.vacancies_objects_name = []
        for vacancy in self.csv_reader(file_name):
            if not start <= int(vacancy['published_at'][:4]) <= end:
                continue
            self.vacancies_objects.append(Vacancy(vacancy))
            if name in vacancy['name']:
                self.vacancies_objects_name.append(Vacancy(vacancy))

    @staticmethod
    def csv_reader(file_name: str) -> list:
        with open(file_name, encoding='utf-8-sig') as read_file:
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
                DataSet.csv_filer(html_tags=html_tags,
                                  row=row,
                                  titles=titles)
                if len(row) == len(titles):
                    data_vacancies.append({titles[i]: row[i] for i in range(len(titles))})
            if len(data_vacancies) == 0:
                print('Нет данных')
                exit(0)
            return data_vacancies

    @staticmethod
    def csv_filer(html_tags, row: list, titles: list):
        if len(row) < len(titles):
            return
        for i in range(len(row)):
            row[i] = ' '.join(re.sub(html_tags, '', row[i])
                              .strip()
                              .split())


class InputConnect:
    def __init__(self):
        self.file_name = 'vacancies_by_year.csv'  # self.processing_file_name(input('Введите название файла: '))
        self.name = 'аналитик'  # input('Введите название профессии: ')
        self.dict_formatter = {
            'Название': lambda row: row.name,
            'Оклад': lambda row: f'{self.slr_format(row.salary.salary_from)} - {self.slr_format(row.salary.salary_to)} ' \
                                 f'({dict_slr_currency[row.salary.salary_currency]}) ',
            'Название региона': lambda row: row.area_name,
            'Дата публикации вакансии': lambda row: '.'.join(reversed(row.published_at[0:10].split('-')))
        }

    @staticmethod
    def processing_file_name(file_name: str) -> str:
        if os.stat(file_name).st_size == 0:
            print('Пустой файл')
            exit(0)
        return file_name

    @staticmethod
    def slr_format(slr: str) -> str:
        return '{:,}'.format(math.floor(float(slr))).replace(',', ' ')

    def table_print(self, data_vacancies: list):
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
                temp = self.dict_formatter[v](value)
                temp_array.append(temp if len(temp) < 100 else temp[:100] + '...')
            table.add_row(temp_array)
            counter += 1
        print(table.get_string(fields=all_titles_table))


class Statistics:
    def __init__(self, dataset: DataSet):
        self.dict_dynamics_slr = self.dynamics_salary(dataset.vacancies_objects)
        self.dict_dynamics_count_vac = self.dynamics_count_vac(dataset.vacancies_objects)
        self.__list_years = list(self.dict_dynamics_slr)
        self.dict_dynamics_slr_name = self.dynamics_salary(dataset.vacancies_objects_name)
        self.dict_dynamics_count_vac_name = self.dynamics_count_vac(dataset.vacancies_objects_name)
        self.dict_dynamics_count_vac_all_cities = self.dynamics_count_vac_big_cities(dataset.vacancies_objects)
        self.dict_dynamics_count_vac_big_cities = dict(filter(lambda x: x[0] != 'Другие',
                                                              list(self.dict_dynamics_count_vac_all_cities.items())))
        self.dict_dynamics_slr_cities = self.dynamics_slr_big_cities(data_vacancies=dataset.vacancies_objects,
                                                                     big_cities=list(
                                                                         self.dict_dynamics_count_vac_big_cities))

    def dynamics_salary(self, data_vacancies: list) -> dict:
        if len(data_vacancies) == 0:
            return {x: 0 for x in self.__list_years}
        dict_dynamic_slr = {}
        for vac in data_vacancies:
            if vac.published_at_year not in dict_dynamic_slr.keys():
                dict_dynamic_slr[vac.published_at_year] = [vac.salary.salary_avg]
            else:
                dict_dynamic_slr[vac.published_at_year].append(vac.salary.salary_avg)
        for key, value in dict_dynamic_slr.items():
            dict_dynamic_slr[key] = math.floor(sum(value) / len(value))
        return dict_dynamic_slr

    def dynamics_count_vac(self, data_vacancies: list) -> dict:
        if len(data_vacancies) == 0:
            return {x: 0 for x in self.__list_years}
        dict_dynamic_count_vac = dict(Counter(map(lambda x: x.published_at_year, data_vacancies)))
        return dict_dynamic_count_vac

    @staticmethod
    def dynamics_slr_big_cities(data_vacancies: list, big_cities: list) -> dict:
        dict_dynamic_slr_cities = {}
        for vac in data_vacancies:
            if vac.area_name not in dict_dynamic_slr_cities.keys() and vac.area_name in big_cities:
                dict_dynamic_slr_cities[vac.area_name] = [vac.salary.salary_avg]
            elif vac.area_name in big_cities:
                dict_dynamic_slr_cities[vac.area_name].append(vac.salary.salary_avg)
        for key, value in dict_dynamic_slr_cities.items():
            dict_dynamic_slr_cities[key] = math.floor(sum(value) / len(value))
        return dict(sorted(dict_dynamic_slr_cities.items(), key=lambda x: x[1], reverse=True))

    def dynamics_count_vac_big_cities(self, data_vacancies: list) -> dict:
        dict_dynamic_count_vac_cities = dict(Counter(map(lambda x: x.area_name, data_vacancies)))
        dict_dynamic_count_vac_big_cities = {}
        count_vac_small_cities = 0
        for key, val in dict_dynamic_count_vac_cities.items():
            if math.floor(val * 100 / len(data_vacancies)) >= 1:
                dict_dynamic_count_vac_big_cities[key] = round(val / len(data_vacancies), 4)
            else:
                count_vac_small_cities += round(val / len(data_vacancies), 4)
        dict_dynamic_count_vac_big_cities['Другие'] = count_vac_small_cities
        return dict(sorted(dict_dynamic_count_vac_big_cities.items(), key=lambda x: x[1], reverse=True))

    def print_statistics(self):
        print('Динамика уровня зарплат по годам: ' + str(self.dict_dynamics_slr))
        print('Динамика количества вакансий по годам: ' + str(self.dict_dynamics_count_vac))
        print('Динамика уровня зарплат по годам для выбранной профессии: ' + str(self.dict_dynamics_slr_name))
        print(
            'Динамика количества вакансий по годам для выбранной профессии: ' + str(self.dict_dynamics_count_vac_name))
        print('Уровень зарплат по городам (в порядке убывания): ' +
              str(dict(islice(self.dict_dynamics_slr_cities.items(), 10))))
        print('Доля вакансий по городам (в порядке убывания): ' +
              str(dict(islice(self.dict_dynamics_count_vac_big_cities.items(), 10))))


class Report:
    def generate_excel(self, input_data: InputConnect, statistics: Statistics):
        wb = Workbook()
        ws1 = wb.create_sheet("Статистика по годам")
        ws2 = wb.create_sheet("Статистика по городам")
        del wb['Sheet']
        thin_border = Border(left=Side(style='thin'),
                             right=Side(style='thin'),
                             top=Side(style='thin'),
                             bottom=Side(style='thin'))
        ft = Font(bold=True)

        ws1.cell(1, 1, 'Год').font = ft
        ws1.cell(1, 2, 'Средняя зарплата').font = ft
        ws1.cell(1, 3, f'Средняя зарплата - {input_data.name}').font = ft
        ws1.cell(1, 4, 'Количество вакансий').font = ft
        ws1.cell(1, 5, f'Количество вакансий - {input_data.name}').font = ft
        for index in range(5):
            ws1.cell(1, index + 1).border = thin_border

        self.__add_cell(ws1, statistics.dict_dynamics_slr, 1, True, thin_border, 0)
        self.__add_cell(ws1, statistics.dict_dynamics_slr, 2, False, thin_border, 0)
        self.__add_cell(ws1, statistics.dict_dynamics_slr_name, 3, False, thin_border, 0)
        self.__add_cell(ws1, statistics.dict_dynamics_count_vac, 4, False, thin_border, 0)
        self.__add_cell(ws1, statistics.dict_dynamics_count_vac_name, 5, False, thin_border, 0)

        ws2.cell(1, 1, 'Город').font = ft
        ws2.cell(1, 2, 'Уровень зарплат').font = ft
        ws2.cell(1, 4, 'Город').font = ft
        ws2.cell(1, 5, 'Доля вакансий').font = ft
        for index in range(5):
            ws2.cell(1, index + 1 if index == (2 or 3) else index + 2).border = thin_border

        self.__add_cell(ws2, statistics.dict_dynamics_slr_cities, 1, True, thin_border, 10)
        self.__add_cell(ws2, statistics.dict_dynamics_slr_cities, 2, False, thin_border, 10)
        self.__add_cell(ws2, statistics.dict_dynamics_count_vac_big_cities, 4, True, thin_border, 10)
        self.__add_cell(ws2, statistics.dict_dynamics_count_vac_big_cities, 5, False, thin_border, 10)

        self.__auto_width(ws1)
        self.__auto_width(ws2)
        wb.save('report.xlsx')

    def __add_cell(self, ws, data: dict, y: int, key: bool, border: Border, limit: int):
        if key:
            for index, year in enumerate(data.keys()):
                if index + 1 != limit:
                    ws.cell(index + 2, y, year).border = border
                else:
                    break
        elif list(data.values())[0] < 1:
            for index, val in enumerate(data.values()):
                if index + 1 != limit:
                    ws.cell(index + 2, y, str(round(val * 100, 2)) + '%').border = border
                else:
                    break
        else:
            for index, val in enumerate(data.values()):
                if index + 1 != limit:
                    ws.cell(index + 2, y, val).border = border
                else:
                    break

    def __auto_width(self, ws):
        for column_cells in ws.columns:
            new_column_length = max(len(str(cell.value)) for cell in column_cells)
            new_column_letter = (get_column_letter(column_cells[0].column))
            if new_column_length > 0:
                ws.column_dimensions[new_column_letter].width = new_column_length * 1.23

    def generate_image(self, input_data: InputConnect, statistics: Statistics):
        fig = plt.figure(figsize=(10, 6))
        plt.rcParams['font.size'] = '8'
        width = 0.4
        years = np.arange(len(statistics.dict_dynamics_slr.keys()))
        ax = fig.add_subplot(221)
        ax.bar(years - width / 2,
               statistics.dict_dynamics_slr.values(),
               width,
               label='средняя з/п')
        ax.bar(years + width / 2,
               statistics.dict_dynamics_slr_name.values(),
               width,
               label=f'з/п {input_data.name}')
        ax.set_title('Уровень зарплат по годам')
        ax.set_xticks(years)
        ax.set_xticklabels(statistics.dict_dynamics_slr.keys())
        ax.legend()

        bx = fig.add_subplot(222)
        bx.bar(years - width / 2,
               statistics.dict_dynamics_count_vac.values(),
               width,
               label='Количество вакансий')
        bx.bar(years + width / 2,
               statistics.dict_dynamics_count_vac_name.values(),
               width,
               label=f'Количество вакансий\n{input_data.name}')
        bx.set_title('Количество вакансий по годам')
        bx.set_xticks(years)
        bx.set_xticklabels(statistics.dict_dynamics_slr.keys())
        bx.legend()
        bx.grid(axis='y')

        dynamics_slr_cities_rev = dict(reversed(list(statistics.dict_dynamics_slr_cities.items())[:10]))
        cities_slr = np.arange(len(dynamics_slr_cities_rev.keys()))
        cx = fig.add_subplot(223)
        cx.barh(cities_slr - width / 2, dynamics_slr_cities_rev.values(), width + 0.2)
        cx.set_title('Уровень зарплат по годам')
        cx.set_yticks(cities_slr)
        cx.set_yticklabels(dynamics_slr_cities_rev.keys())
        cx.grid(axis='x')

        dx = fig.add_subplot(224)
        dynamics_count_vac_cit_rev = dict(reversed(list(statistics.dict_dynamics_count_vac_all_cities.items())))
        dx.pie(dynamics_count_vac_cit_rev.values(),
               labels=dynamics_count_vac_cit_rev.keys())
        dx.set_title('Доля вакансий по городам')
        dx.axis("equal")
        fig.savefig('graph.png')

    def generate_pdf(self, input_data: InputConnect, statistics: Statistics):
        loader = FileSystemLoader('./temp.html')
        env = Environment(loader=loader)
        template = env.get_template('')
        slr_count_vac_sheet = template.render(name=input_data.name,
                                              year=list(statistics.dict_dynamics_slr),
                                              slr=list(statistics.dict_dynamics_slr.values()),
                                              slr_name=list(statistics.dict_dynamics_slr_name.values()),
                                              count_vac=list(statistics.dict_dynamics_count_vac.values()),
                                              count_vac_name=list(statistics.dict_dynamics_count_vac_name.values()),
                                              city1=list(statistics.dict_dynamics_slr_cities.keys())[:10],
                                              slr_lvl=list(statistics.dict_dynamics_slr_cities.values())[:10],
                                              city2=list(statistics.dict_dynamics_count_vac_big_cities.keys())[:10],
                                              part_slr=list(map(lambda x: str(round(x * 100, 4)) + '%',
                                                                statistics.dict_dynamics_count_vac_big_cities.values()))[
                                                       :10])
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_string(slr_count_vac_sheet,
                           'report.pdf',
                           configuration=config,
                           options={'enable-local-file-access': None})


if __name__ == '__main__':
    changing_output = input('Вакансии или статистика?: ')
    input_data = InputConnect()
    if changing_output == 'Статистика':
        dataset = DataSet(input_data.file_name, input_data.name, 2007, 2014)
        statistics = Statistics(dataset)
        statistics.print_statistics()
        report = Report()
        report.generate_excel(input_data, statistics)
        report.generate_image(input_data, statistics)
        report.generate_pdf(input_data, statistics)
    elif changing_output == 'Вакансии':
        dataset = DataSet(input_data.file_name, input_data.name, 2007, 2014)
        input_data.table_print(dataset.vacancies_objects)
