import math
from collections import Counter
from itertools import islice

from DataSet import DataSet


class StatisticsByCities:
    """Класс статистики по городам

    Attributes:
        dict_dynamics_count_vac_all_cities (dict): Словарь количества вакансий по всем городам
        dict_dynamics_count_vac_big_cities (dict): Словарь количества вакансий по 'большим' городам
        dict_dynamics_slr_cities (dict): Словарь уровня зарплат по 'большим' городам
    """

    def __init__(self, file_name: str, name: str):
        """Инициадизация класса StatisticsByCities

        :param file_name: имя файла
        :param name: название профессии
        """
        dataset = DataSet(file_name, name, 2007, 2014)
        self.dict_dynamics_count_vac_all_cities = self.__dynamics_count_vac_cities(dataset.vacancies_objects)
        self.dict_dynamics_count_vac_big_cities = dict(filter(lambda x: x[0] != 'Другие',
                                                              list(self.dict_dynamics_count_vac_all_cities.items())))
        self.dict_dynamics_slr_cities = self.__dynamics_slr_big_cities(data_vacancies=dataset.vacancies_objects,
                                                                       big_cities=list(
                                                                           self.dict_dynamics_count_vac_big_cities))

    def __dynamics_count_vac_cities(self, data_vacancies: list) -> dict:
        """Составление словаря количества вакансий по городам

        :param data_vacancies: Список вакансий
        :return: Словарь количества вакансий по городам
        """
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

    @staticmethod
    def __dynamics_slr_big_cities(data_vacancies: list, big_cities: list) -> dict:
        """Составление словаря уровня зарплат по 'большим' городам

        :param data_vacancies: Список вакансий
        :param big_cities: Список 'больших' городов
        :return: Словарь уровня зарплат по 'большим' городам
        """
        dict_dynamic_slr_cities = {}
        for vac in data_vacancies:
            if vac.area_name not in dict_dynamic_slr_cities.keys() and vac.area_name in big_cities:
                dict_dynamic_slr_cities[vac.area_name] = [vac.salary.get_salary_to_rub()]
            elif vac.area_name in big_cities:
                dict_dynamic_slr_cities[vac.area_name].append(vac.salary.get_salary_to_rub())
        for key, value in dict_dynamic_slr_cities.items():
            dict_dynamic_slr_cities[key] = math.floor(sum(value) / len(value))
        return dict(sorted(dict_dynamic_slr_cities.items(), key=lambda x: x[1], reverse=True))

    def print_statistics(self):
        """Метод печати статистики по городам в консоль

        :return:
        """
        print('Уровень зарплат по городам (в порядке убывания): ' +
              str(dict(islice(self.dict_dynamics_slr_cities.items(), 10))))
        print('Доля вакансий по городам (в порядке убывания): ' +
              str(dict(islice(self.dict_dynamics_count_vac_big_cities.items(), 10))))