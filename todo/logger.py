from typing import List
from attr import attrs, attrib
from os.path import exists


TIMES_SEPARATOR = '-'
CASE_SEPARATOR = '#'

@attrs(slots=True)
class Business:
    date_begin: str = attrib(default='')
    time_begin: str = attrib(default='')
    date_end: str = attrib(default='')
    time_end: str = attrib(default='')
    case: str = attrib(default='')


class Logger:
    def __init__(self, file_name: str)-> None:
        self.file_name = file_name

    @staticmethod
    def parse_list(lines: List[str])-> List[Business]:
        """
        Парсинг извлеченных строк, заполнение класса Business
        :param lines: Список изначальных строк
        "date_begin time_begin - date_end time_end # case"
        :return: Список дел
        """
        result_list: List[Business] = []
        for line in lines:
            business = Business()

            times, case = line.split(CASE_SEPARATOR)

            business.case = case.strip()

            try:
                times_begin, times_end = times.split(TIMES_SEPARATOR)
                date_begin, time_begin = times_begin.split()
                business.date_begin = date_begin.strip()
                business.time_begin = time_begin.strip()
                date_end, time_end = times_end.split()
                business.date_end = date_end.strip()
                business.time_end = time_end.strip()

            except ValueError:
                date_begin, time_begin = times.split()
                business.date_begin = date_begin.strip()
                business.time_begin = time_begin.strip()

            result_list.append(business)
        return result_list

    def load_from_files(self)-> List[Business]:
        if not self.file_name:
            return []
        with open(self.file_name) as reading_file:
            lines:  List[str] = [line.strip() for line in reading_file]
        return self.parse_list(lines)

