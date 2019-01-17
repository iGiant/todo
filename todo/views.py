from attr import attrs, attrib
from datetime import datetime
from tkinter import Tk, Frame, Entry, Label, Checkbutton, IntVar
from tkinter.constants import RIDGE, TOP, X, RIGHT, LEFT
from typing import List, Optional

from .logger import Business, Logger, DAY, MONTH
from .threads import start_scrool_label

MONTHS = ('янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек')


@attrs(slots=True)
class Controls:
    frame: Optional[Frame] = attrib(default=None)
    date_case: Optional[Label] = attrib(default=None)
    var: Optional[IntVar] = attrib(default=None)
    check: Optional[Checkbutton] = attrib(default=None)
    end_time: Optional[Entry] = attrib(default=None)
    end_date: Optional[Entry] = attrib(default=None)


class GuiForm:
    """
    Основное окно ввода информации
    """
    def __init__(self, file_name: str):
        self.logger = Logger(file_name)
        self._case_list = self.logger.load_from_files()
        self._controls_list = []
        self._ctrl_mode = False
        self._unfinished_case_list = self._get_reversed_unfinished_case_list()
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
        now = datetime.now()
        self._edit_frame = Frame(self.root, relief=RIDGE, borderwidth=1)
        self._edit_frame.pack(side=TOP, fill=X)
        self._edit_date = Entry(self._edit_frame, width=10, font=f"Arial 12", borderwidth=1)
        self._edit_date.pack(side=LEFT)
        self._edit_date.bind('<KeyPress>', self._fedit_key_press)
        self._edit_date.insert(0, f'{now.strftime("%d.%m.%Y")}')
        self._edit_time = Entry(self._edit_frame, width=5, font=f"Arial 12", borderwidth=1)
        self._edit_time.insert(0, f'{now.strftime("%H:%M")}')
        self._edit_time.pack(side=LEFT)
        self._edit_time.bind('<KeyPress>', self._fedit_key_press)
        self._edit_case = Entry(self._edit_frame, width=40, font=f"Arial 12", borderwidth=1)
        self._edit_case.pack(side=LEFT)
        self._edit_case.bind('<KeyPress>', self._fedit_key_press)
        self._edit_case.bind('<KeyRelease>', self._fedit_key_release)
        self._edit_case.focus_set()

    def _create_widgets_done(self):
        """
        Помещение элементов незаконченных дел на форму для отметки
        :return:
        """
        now = datetime.now()
        for case in self._unfinished_case_list:
            controls = Controls()
            controls.frame = Frame(self.root, relief=RIDGE, borderwidth=1)
            controls.frame.pack(fill=X)
            controls.date_case = Label(controls.frame, font=f"Arial 12", justify=LEFT)
            controls.date_case.pack(side=LEFT)
            date = f'{case.time_begin} ({case.date_begin[DAY]} {MONTHS[int(case.date_begin[MONTH]) - 1]})'
            start_scrool_label(controls.date_case, date, case.case, 30)
            controls.var = IntVar()
            controls.check = Checkbutton(controls.frame, variable=controls.var, relief=RIDGE, borderwidth=1)
            controls.check.pack(side=RIGHT)
            controls.end_time = Entry(controls.frame, width=5, font=f"Arial 12", borderwidth=1)
            controls.end_time.insert(0, f'{now.strftime("%H:%M")}')
            controls.end_time.pack(side=RIGHT)
            controls.end_time.bind('<KeyPress>', self._fedit_key_press)
            controls.end_date = Entry(controls.frame, font=f"Arial 12", width=10, borderwidth=1)
            controls.end_date.insert(0, f'{now.strftime("%d.%m.%Y")}')
            controls.end_date.pack(side=RIGHT)
            controls.end_date.bind('<KeyPress>', self._fedit_key_press)

            self._controls_list.append(controls)

    def show_form(self):
        """
        Показ формы
        :return:
        """
        self.root.call('wm', 'attributes', '.', '-topmost', True)
        self.root.after_idle(self.root.call, 'wm', 'attributes', '.', '-topmost', False)
        self.root.wm_geometry("+750+450")
        self.root.mainloop()

    def _fedit_key_release(self, event):
        if event.keycode == 17:
            self._ctrl_mode = False

    def _fedit_key_press(self, event):
        """
        Обработка нажатия Enter и Esc
        :param event: параметры события
        :return:
        """
        if event.keycode in range(49, 59) and self._ctrl_mode:
            code = event.keycode - 49
            if code < len(self._unfinished_case_list):
                self._controls_list[code].var.set(0 if self._controls_list[code].var.get() else 1)
        if event.keycode == 17 and not self._ctrl_mode:
            self._ctrl_mode = True
        if event.keycode == 13:
            need = False
            if self._edit_case.get():
                business = Business()
                business.date_begin = self._edit_date.get()
                business.time_begin = self._edit_time.get()
                business.case = self._edit_case.get()
                self._case_list.append(business)
                self.logger.write_to_file(self._case_list)
                need = True
            for index, controls in enumerate(self._controls_list):
                if controls.var.get():
                    found_index = self._get_index_case(self._unfinished_case_list[index])
                    if found_index != -1:
                        case = self._case_list[found_index]
                        case.date_end = controls.end_date.get()
                        case.time_end = controls.end_time.get()
                        need = True
            if need:
                self.logger.write_to_file(self._case_list)
            exit(0)
        elif event.keycode == 27:
            exit(1)

    def _get_index_case(self, business: Business)-> int:
        for index, case in enumerate(self._case_list):
            if (business.date_begin == case.date_begin and
                    business.time_begin == case.time_begin and
                    business.case == case.case):
                return index
        return -1

    def _get_reversed_unfinished_case_list(self)-> List[Business]:
        """
        Возвращение списка незаконченных дел
        :return: список незаконченных дел
        """
        return list(reversed([case for case in self._case_list if not case.date_end]))
