from typing import List
from attr import attrs, attrib


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
        pass

    def load_from_files(self)-> List[Business]:
        lines = List[str]
        return self.parse_list(lines)