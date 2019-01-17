from threading import Thread
from time import sleep
from tkinter import Label


PAUSE = 0.2


def _scrool_label(label: Label, date: str, text: str, length: int)-> None:
    def _show_text(start_, end_, time):
        scrool_text = text[start_:end_]
        label['text'] = f'{date}: {scrool_text}'
        sleep(time)

    if length > len(text):
        label['text'] = f'{date}: {text}'
        return None
    start = 0
    end = start + length
    _show_text(start, end, 5 * PAUSE)
    while True:
        end += 1
        if end > len(text):
            start = 0
            end = start + length
            sleep(PAUSE * 5)
            _show_text(start, end, 6 * PAUSE)
        else:
            start += 1
            _show_text(start, end, PAUSE)


def start_scrool_label(label: Label, date: str, text: str, length: int)-> None:
    thread = Thread(target=_scrool_label, args=(label, date, text, length))
    thread.daemon = True
    thread.start()
