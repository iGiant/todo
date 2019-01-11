from .views import GuiForm


def start_program():
    gui_form = GuiForm('todo_list.log')
    gui_form.show_form()
