from typing import List
from attr import attrs, attrib
from os.path import exists


TIMES_SEPARATOR = '-'
CASE_SEPARATOR = '#'
DAY = slice(None, 2)
MONTH = slice(3, 5)
YEAR = slice(6, None)


@attrs(slots=True)
class Business:
    date_begin: str = attrib(default='')  # 'dd.mm.yyyy' -> '01.34.6789'
    time_begin: str = attrib(default='')  # 'hh:mm' -> '01:34'
    date_end: str = attrib(default='')  # 'dd.mm.yyyy'
    time_end: str = attrib(default='')  # 'hh:mm'
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
        with open(self.file_name, 'w', encoding='utf8') as write_file:
            sort_lines = sorted(lines,
                                key=lambda case: f'{case.date_begin[YEAR]}'
                                f'{case.date_begin[MONTH]}'
                                f'{case.date_begin[DAY]}')
            for line in sort_lines:
                write_data = (f'{line.date_begin} {line.time_begin} {TIMES_SEPARATOR} '
                              f'{line.date_end} {line.time_end} {CASE_SEPARATOR} {line.case}'
                              if line.date_end else
                              f'{line.date_begin} {line.time_begin} {CASE_SEPARATOR} {line.case}')
                write_file.write(write_data + '\n')
