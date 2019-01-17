from threading import Thread
from time import sleep
from tkinter import Label


PAUSE = 0.2


def _scrool_label(label: Label, date: str, text: str, length: int)-> None:
    if length > len(text):
        label['text'] = f'{date}: {text}'
        return None
    start = 0
    end = start + length
    scrool_text = text[start:end]
    label['text'] = f'{date}: {scrool_text}'
    sleep(PAUSE * 10)
    while True:
        end += 1
        if end > len(text):
            start = 0
            end = start + length
            sleep(PAUSE * 5)
            scrool_text = text[start:end]
            label['text'] = f'{date}: {scrool_text}'
            sleep(PAUSE * 5)
        else:
            start += 1
            scrool_text = text[start:end]
            label['text'] = f'{date}: {scrool_text}'
            sleep(PAUSE)


def start_scrool_label(label: Label, date: str, text: str, length: int)-> None:
    thread = Thread(target=_scrool_label, args=(label, date, text, length))
    thread.daemon = True
    thread.start()
