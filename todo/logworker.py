from os import startfile
from os.path import exists
from typing import List

from attr import attrs

from .settings import CASE_SEPARATOR, TIMES_SEPARATOR
from .settings import DAY, MONTH, YEAR
from .settings import HOUR,MINUTE


@attrs(slots=True, auto_attribs=True)
class Business:
    date_begin: str = ''  # 'dd.mm.yyyy' -> '01.34.6789'
    time_begin: str = ''  # 'hh:mm' -> '01:34'
    date_end: str = ''  # 'dd.mm.yyyy'
    time_end: str = ''  # 'hh:mm'
    case: str = ''


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
        """
        Чтение данных из текстового файла-лога и ...
        :return: возврат списка спарсенных значений
        """
        if not exists(self.file_name):
            return []
        with open(self.file_name, encoding='utf8') as reading_file:
            lines:  List[str] = [line.strip() for line in reading_file]
        return self.parse_list(lines)

    def write_to_file(self, lines: List[Business])-> None:
        """
        Запись дел в текстовый файл-лог
        :param lines: Список дел, которые необходимо сохранить
        :return: None
        """
        sort_lines = sorted(lines, key=lambda case: f'{case.date_begin[YEAR]}{case.date_begin[MONTH]}'
                                                    f'{case.date_begin[DAY]}{case.time_begin[HOUR]}'
                                                    f'{case.time_begin[MINUTE]}')
        with open(self.file_name, 'w', encoding='utf8') as write_file:
            for line in sort_lines:
                write_data = (f'{line.date_begin} {line.time_begin} {TIMES_SEPARATOR} '
                              f'{line.date_end} {line.time_end} {CASE_SEPARATOR} {line.case}'
                              if line.date_end else
                              f'{line.date_begin} {line.time_begin} {CASE_SEPARATOR} {line.case}')
                write_file.write(write_data + '\n')

    def show_log_file(self):
        startfile(self.file_name)
