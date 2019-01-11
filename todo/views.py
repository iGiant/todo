from datetime import datetime
from tkinter import Tk, Frame, Entry
from tkinter.constants import RIDGE, TOP, X, LEFT
from typing import List

from .logger import Business, Logger


class GuiForm:
    """
    Основное окно ввода информации
    """
    def __init__(self, file_name: str):
        self.logger = Logger(file_name)
        self._case_list = self.logger.load_from_files()
        self._unfinished_case_list = self._get_unfinished_case_list().reverse()
        self._create_window()
        self._create_widgets_entry()
        if self._unfinished_case_list:
            self._create_widgets_done()

    def _create_window(self):
        self.root = Tk()
        self.root.title('Что я делаю или сделал')
        self.root.iconbitmap('todo.ico')
        self.root.resizable(width=False, height=False)

    def _create_widgets_entry(self):
        self._top_frame = Frame(self.root, relief=RIDGE, borderwidth=1)
        self._top_frame.pack(side=TOP, fill=X)
        now = datetime.now()
        self._edit_date = Entry(self._top_frame, width=10, font=f"Arial 12", borderwidth=1)
        self._edit_date.pack(side=LEFT)
        self._edit_date.insert(0, f'{now.strftime("%d.%m.%Y")}')
        self._edit_time = Entry(self._top_frame, width=5, font=f"Arial 12", borderwidth=1)
        self._edit_time.insert(0, f'{now.strftime("%H:%M")}')
        self._edit_time.pack(side=LEFT)
        self._edit_case = Entry(self._top_frame, width=40, font=f"Arial 12", borderwidth=1)
        self._edit_case.pack(side=LEFT)
        self._edit_case.bind('<KeyPress>', self._fedit_key_press)
        self._edit_case.focus_set()

    def _create_widgets_done(self):
        pass

    def show_form(self):
        """
        Показ формы
        :return:
        """
        # self.root.geometry(self.get_centr_screen())
        self.root.update_idletasks()
        self.root.mainloop()

    def get_centr_screen(self):
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        size = tuple(x for x in self.root.geometry().split('+')[0].split('x'))
        return f'{size[0]}x{size[1]}+{w // 2 - int(size[0]) // 2}+{h // 2 - int(size[1]) // 2}'

    def _fedit_key_press(self, event):
        """
        Обработка нажатия Enter и Esc
        :param event: параметры события
        :return:
        """
        if event.keycode == 13:
            if self._edit_case.get():
                business = Business()
                business.date_begin = self._edit_date.get()
                business.time_begin = self._edit_time.get()
                business.case = self._edit_case.get()
                self._case_list.append(business)
                self.logger.write_to_file(self._case_list)
            exit(0)
        elif event.keycode == 27:
            exit(1)
    def _get_unfinished_case_list(self)-> List[Business]:
        """
        Возвращение списка незаконченных дел
        :return: список незаконченных дел
        """
        return [case for case in self._case_list if not case.date_end]
