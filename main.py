import cProfile, pstats, io
from collections import Counter
from os import walk
from pstats import SortKey
from DataSet import DataSet
from InputConnect import InputConnect
from Report import Report
from StatisticsByCities import StatisticsByCities
from StatisticsByYear import StatisticsByYear

if __name__ == '__main__':
    # pr = cProfile.Profile()
    # pr.enable()
    input_data = InputConnect()
    changing_output = int(input('Таблица в консоль или отчет по статистике? (1 или 2): '))
    if changing_output == 2:
        dataset = DataSet(input_data.file_name, input_data.name, 2003, 2022)
        # splitted_file_names = input_data.split()
        splitted_file_names = list(map(lambda x: 'csv_files_by_year/' + x,
                                       next(walk('csv_files_by_year'), (None, None, []))[2]))
        statistics_by_year = StatisticsByYear(input_data.name, splitted_file_names)
        statistics_by_cities = StatisticsByCities(input_data.file_name, input_data.name)
        statistics_by_cities.print_statistics()
        statistics_by_year.print_statistics()
        report = Report()
        report.generate_excel(input_data.name, statistics_by_year, statistics_by_cities)
        report.generate_image(input_data.name, statistics_by_year, statistics_by_cities)
        report.generate_pdf(input_data.name, statistics_by_year, statistics_by_cities)
    elif changing_output == 1:
        dataset = DataSet(input_data.file_name, input_data.name, 2003, 2022)
        input_data.table_print(dataset.vacancies_objects_name, is_full_slr=False)
    # pr.disable()
    # s = io.StringIO()
    # sortby = SortKey.CUMULATIVE
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # print(s.getvalue())
