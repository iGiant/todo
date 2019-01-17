from threading import Thread
from time import sleep
from tkinter import Label


PAUSE = 0.15


def _get_fixit_length_text(label_ : Label, text_: str, width: int)-> str:
    label_['text'] = text_
    end = len(text_)
    while label_.winfo_reqwidth() > width:
        end -= 1
        label_['text'] = text_[:end]
    return text_[:end]


def _scrool_label(label: Label, date: str, text: str, length: int)-> None:

    def _show_text(text_, time):
        label['text'] = text_
        sleep(time)

    temp_label = Label(None, font=f"Tahoma 12", justify='left')

    if _get_fixit_length_text(temp_label, f'{date}: {text}', length) == f'{date}: {text}':
        label['text'] = f'{date}: {text}'
        return None

    start = 0

    _show_text(_get_fixit_length_text(temp_label, f'{date}: {text[start:]}', length), 5 * PAUSE)
    while True:
        if _get_fixit_length_text(temp_label, f'{date}: {text[start:]}', length) == f'{date}: {text[start:]}':
            _show_text(f'{date}: {text[start:]}', 7 * PAUSE)
            start = 0
            _show_text(_get_fixit_length_text(temp_label, f'{date}: {text[start:]}', length), 5 * PAUSE)
        else:
            _show_text(_get_fixit_length_text(temp_label, f'{date}: {text[start:]}', length), PAUSE)
        start += 1


def start_scrool_label(label: Label, date: str, text: str, length: int)-> None:
    thread = Thread(target=_scrool_label, args=(label, date, text, length))
    thread.daemon = True
    thread.start()
