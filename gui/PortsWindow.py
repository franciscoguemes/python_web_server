import tkinter
from tkinter import Toplevel
from tkinter import ttk


class PortsWindow(Toplevel):
    DEFAULT_HEIGHT = 500
    DEFAULT_WIDTH = 300

    def __init__(self, master, report):
        self.__master = master
        Toplevel.__init__(self, master, height=self.DEFAULT_HEIGHT, width=self.DEFAULT_WIDTH)
        self.resizable(0, 0)
        self.title("Ports in use")
        self.__add_components(report)

    def __add_components(self, report):
        scrollbar = tkinter.Scrollbar(self)
        textarea = tkinter.Text(self)
        # textarea = tkinter.Text(self, height=3, width=50)
        # scrollbar.pack()

        # https://www.python-course.eu/tkinter_text_widget.php
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        textarea.pack(side=tkinter.LEFT, fill=tkinter.Y)
        scrollbar.config(command=textarea.yview)
        textarea.config(yscrollcommand=scrollbar.set)
        textarea.insert(tkinter.END, report)
        textarea.configure(state="disabled")
