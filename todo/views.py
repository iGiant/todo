from tkinter import Tk, Frame, Entry
from tkinter.constants import RIDGE, TOP, X, LEFT
from datetime import datetime
from .logger import Business, Logger


class GuiForm:
    """
    Основное окно ввода информации
    """
    def __init__(self, file_name: str):
        self.case_list = Logger(file_name)
        self._create_window()
        self._create_widgets_entry()

    def _create_window(self):
        self.root = Tk()
        self.root.title('Что я делаю или сделал')
        self.root.iconbitmap('todo.ico')
        self.root.resizable(width=False, height=False)

    def _create_widgets_entry(self):
        self.top_frame = Frame(self.root, relief=RIDGE, borderwidth=1)
        self.top_frame.pack(side=TOP, fill=X)
        now = datetime.now()
        self.edit_date = Entry(self.top_frame, width=10, font=f"Arial 12", borderwidth=1)
        self.edit_date.pack(side=LEFT)
        self.edit_date.insert(0, f'{now.strftime("%d.%m.%Y")}')
        self.edit_time = Entry(self.top_frame, width=5, font=f"Arial 12", borderwidth=1)
        self.edit_time.insert(0, f'{now.strftime("%H:%M")}')
        self.edit_time.pack(side=LEFT)
        self.edit_case = Entry(self.top_frame, width=40, font=f"Arial 12", borderwidth=1)
        self.edit_case.pack(side=LEFT)
        self.edit_case.focus_set()

    def show_form(self):
        # self.root.geometry(self.get_centr_screen())
        self.root.update_idletasks()
        self.root.mainloop()

    def get_centr_screen(self):
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        size = tuple(x for x in self.root.geometry().split('+')[0].split('x'))
        return f'{size[0]}x{size[1]}+{w // 2 - int(size[0]) // 2}+{h // 2 - int(size[1]) // 2}'