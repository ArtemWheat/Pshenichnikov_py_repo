import math
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from DataSet import DataSet


class StatisticsByYear:
    """Класс статистики по годам на основании csv чанков

    Attributes:
        name (str): Словарь количества вакансий по всем городам
        dict_dynamics_slr (dict): Словарь динамики уровня зарплат по годам для всех вакансий
        dict_dynamics_count_vac (dict): Словарь динамики количества вакансий по годам для всех вакансий
        dict_dynamics_slr_name (dict): Словарь динамики уровня зарплат по годам для искомых вакансий
        dict_dynamics_count_vac_name (dict): Словарь динамики количества вакансий по годам для искомых вакансий
    """
    def __init__(self, name: str, splitted_file_names: list):
        """инициализация класса StatisticsByYear

        :param name: название профессии
        :param splitted_file_names: список чанков csv
        """
        self.name = name
        list_dict_dynamics_slr = []
        list_dict_dynamics_count_vac = []
        list_dict_dynamics_slr_name = []
        list_dict_dynamics_count_vac_name = []

        pool = ProcessPoolExecutor(max_workers=6)
        for el in pool.map(self.stat, splitted_file_names):
            list_dict_dynamics_slr.append(el[0])
            list_dict_dynamics_count_vac.append(el[1])
            list_dict_dynamics_slr_name.append(el[2])
            list_dict_dynamics_count_vac_name.append(el[3])

        self.dict_dynamics_slr = self.__get_dict_from_list(list(filter(None, list_dict_dynamics_slr)))
        self.dict_dynamics_count_vac = self.__get_dict_from_list(list(filter(None, list_dict_dynamics_count_vac)))
        self.dict_dynamics_slr_name = self.__get_dict_from_list(list(filter(None, list_dict_dynamics_slr_name)))
        self.dict_dynamics_count_vac_name = self.__get_dict_from_list(list(filter(None, list_dict_dynamics_count_vac_name)))

    @staticmethod
    def __get_dict_from_list(list_dicts: list) -> dict:
        """преобразование списка словарей в словарь

        :param list_dicts:
        :return: словарь
        """
        result = {}
        for x in list_dicts:
            result.update(x)
        return result

    def stat(self, file_name):
        """вывод статистики по годам

        :param file_name: имя файла
        :return: кортеж словарей со статистикой
        """
        dataset = DataSet(file_name, self.name, 2007, 2014)
        return self.__dynamics_salary(dataset.vacancies_objects), \
               self.__dynamics_count_vac(dataset.vacancies_objects), \
               self.__dynamics_salary(dataset.vacancies_objects_name), \
               self.__dynamics_count_vac(dataset.vacancies_objects_name)

    def __dynamics_salary(self, data_vacancies: list) -> dict:
        """Составление словаря динамики уровня зарплат по годам для всех вакансий

        :param data_vacancies: Список вакансий
        :return: Словарь динамики уровня зарплат по годам для всех вакансий
        """
        # if len(data_vacancies) == 0:
        #    return {x: 0 for x in self.__list_years}
        dict_dynamic_slr = {}
        for vac in data_vacancies:
            if vac.published_at_year not in dict_dynamic_slr.keys():
                dict_dynamic_slr[vac.published_at_year] = [vac.salary.get_salary_to_rub()]
            else:
                dict_dynamic_slr[vac.published_at_year].append(vac.salary.get_salary_to_rub())
        for key, value in dict_dynamic_slr.items():
            dict_dynamic_slr[key] = math.floor(sum(value) / len(value))
        return dict_dynamic_slr

    def __dynamics_count_vac(self, data_vacancies: list) -> dict:
        """Составление словаря динамики количества вакансий по годам для всех вакансий

        :param data_vacancies: Список вакансий
        :return: Словарь динамики количества вакансий по годам для всех вакансий
        """
        # if len(data_vacancies) == 0:
        #    return {x: 0 for x in self.__list_years}
        dict_dynamic_count_vac = dict(Counter(map(lambda x: x.published_at_year, data_vacancies)))
        return dict_dynamic_count_vac

    def print_statistics(self):
        """Метод печати статистики в консоль

        :return:
        """
        print('Динамика уровня зарплат по годам: ' + str(self.dict_dynamics_slr))
        print('Динамика количества вакансий по годам: ' + str(self.dict_dynamics_count_vac))
        print('Динамика уровня зарплат по годам для выбранной профессии: ' + str(self.dict_dynamics_slr_name))
        print(
            'Динамика количества вакансий по годам для выбранной профессии: ' + str(self.dict_dynamics_count_vac_name))