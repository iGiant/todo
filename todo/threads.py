from threading import Thread
from time import sleep
from tkinter import Label

from .settings import FONT, PAUSE


def _scrool_label(label: Label, date: str, text: str, width_label: int) -> None:
    """
    выполняемая в отдельном потоке функция про прокрутки текста
    :param label: виджет для вывода текста
    :param date: часть строки для вывода
    :param text: текст для вывода
    :param width_label: ширина виджета Label в пикселях
    :return:
    """
    def _show_text(show_text: str, time: float) -> None:
        """
        Помещает текст в виджет Label и делает паузу в time секунд
        :param show_text: Выводимы текст
        :param time:
        :return:
        """
        label['text'] = show_text
        sleep(time)

    def _get_fixit_length_text(test_label: Label, full_text: str, width: int) -> str:
        """
        Возвращает текст для формирование Label нужной длины
        :param test_label: тестовый виджет Label для проверки
        :param full_text: текст, часть которого необходимо вывести
        :param width: Максимальная ширина виджета
        :return: срез текста для вывода через виджет Label
        """
        test_label['text'] = full_text
        end = len(full_text)
        while test_label.winfo_reqwidth() > width:
            end -= 1
            test_label['text'] = full_text[:end]
        return full_text[:end]

    # _scrool_label()
    temp_label = Label(None, font=FONT)

    if _get_fixit_length_text(temp_label, f'{date}: {text}', width_label) == f'{date}: {text}':
        label['text'] = f'{date}: {text}'
        return None

    start = 0

    _show_text(_get_fixit_length_text(temp_label, f'{date}: {text[start:]}', width_label), 5 * PAUSE)
    while True:
        if _get_fixit_length_text(temp_label, f'{date}: {text[start:]}', width_label) == f'{date}: {text[start:]}':
            _show_text(f'{date}: {text[start:]}', 7 * PAUSE)
            start = 0
            _show_text(_get_fixit_length_text(temp_label, f'{date}: {text[start:]}', width_label), 5 * PAUSE)
        else:
            _show_text(_get_fixit_length_text(temp_label, f'{date}: {text[start:]}', width_label), PAUSE)
        start += 1


def start_scrool_label(label: Label, date: str, text: str, length: int) -> None:
    """
    Запускает новый поток для прокрутки текста в виджете Label
    :param label: виджет для вывода текста
    :param date: часть строки для вывода
    :param text: текст для вывода
    :param length: ширина виджета Label в пикселях
    :return:
    """
    thread = Thread(target=_scrool_label, args=(label, date, text, length))
    thread.daemon = True
    thread.start()
