import io
from unittest import TestCase, mock
from main import Statistics, DataSet, InputConnect
from unittest.mock import patch, call


class StatisticsTests(TestCase):
    @patch('builtins.input', side_effect=['test_slr.csv', 'аналитик'])
    def test_dict_slr(self, mock_input):
        input_data = InputConnect()
        self.assertEqual(Statistics(DataSet(input_data.file_name, input_data.name, 2007, 2007)).dict_dynamics_slr,
                         {2007: 44285})

    @patch('builtins.input', side_effect=['test_slr.csv', 'аналитик'])
    def test_dict_slr_name1(self, mock_input):
        input_data = InputConnect()
        self.assertEqual(Statistics(DataSet(input_data.file_name, input_data.name, 2007, 2007)).dict_dynamics_slr_name,
                         {2007: 62500})

    @patch('builtins.input', side_effect=['test_slr.csv', 'программист'])
    def test_dict_slr_name2(self, mock_input):
        input_data = InputConnect()
        self.assertEqual(Statistics(DataSet(input_data.file_name, input_data.name, 2007, 2007)).dict_dynamics_slr_name,
                         {2007: 40000})

    @patch('builtins.input', side_effect=['test_count_vac.csv', 'аналитик'])
    def test_dict_count_vac(self, mock_input):
        input_data = InputConnect()
        self.assertEqual(Statistics(DataSet(input_data.file_name, input_data.name, 2007, 2008)).dict_dynamics_count_vac,
                         {2007: 7,
                          2008: 3})

    @patch('builtins.input', side_effect=['test_count_vac.csv', 'аналитик'])
    def test_dict_count_vac_name1(self, mock_input):
        input_data = InputConnect()
        self.assertEqual(Statistics(DataSet(input_data.file_name, input_data.name, 2007, 2008)).dict_dynamics_count_vac_name,
                         {2007: 2})

    @patch('builtins.input', side_effect=['test_count_vac.csv', 'программист'])
    def test_dict_count_vac_name2(self, mock_input):
        input_data = InputConnect()
        self.assertEqual(
            Statistics(DataSet(input_data.file_name, input_data.name, 2007, 2008)).dict_dynamics_count_vac_name,
            {2007: 2,
             2008: 1})

    @patch('builtins.input', side_effect=['test_cities.csv', 'программист'])
    def test_dict_cities(self, mock_input):
        input_data = InputConnect()
        self.assertEqual(
            Statistics(DataSet(input_data.file_name, input_data.name, 2007, 2008)).dict_dynamics_slr_cities,
            {'Варгаши': 31000,
             'Екатеринбург': 22500,
             'Курган': 35000,
             'Москва': 57562,
             'Половинное': 35000,
             'Санкт-Петербург': 48750,
             'Саратов': 7500,
             'Сумки': 65000,
             'Челябинск': 40000})

    @patch('builtins.input', side_effect=['test_cities.csv', 'программист'])
    def test_dict_all_cities_count_vac(self, mock_input):
        input_data = InputConnect()
        self.assertEqual(
            Statistics(DataSet(input_data.file_name, input_data.name, 2007, 2008)).dict_dynamics_count_vac_all_cities,
            {'Варгаши': 0.0769,
             'Другие': 0,
             'Екатеринбург': 0.0769,
             'Курган': 0.0769,
             'Москва': 0.3077,
             'Половинное': 0.0769,
             'Санкт-Петербург': 0.1538,
             'Саратов': 0.0769,
             'Сумки': 0.0769,
             'Челябинск': 0.0769})

    @patch('builtins.input', side_effect=['test_big_cities.csv', 'программист'])
    def test_dict_big_cities_count_vac(self, mock_input):
        input_data = InputConnect()
        self.assertEqual(
            Statistics(DataSet(input_data.file_name, input_data.name, 2007, 2008)).dict_dynamics_count_vac_all_cities,
            {'Другие': 0.0376,
             'Екатеринбург': 0.0189,
             'Казань': 0.0189,
             'Москва': 0.7075,
             'Нижний Новгород': 0.0283,
             'Новосибирск': 0.0472,
             'Санкт-Петербург': 0.1132,
             'Челябинск': 0.0283})

