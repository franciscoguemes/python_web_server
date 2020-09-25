import tkinter
from tkinter import Toplevel
from tkinter import ttk
from tkinter import messagebox


class ProgressBarWindow(Toplevel):
    DEFAULT_HEIGHT = 100
    DEFAULT_WIDTH = 250

    def __init__(self, master):
        self.__master = master
        Toplevel.__init__(self, master, height=self.DEFAULT_HEIGHT, width=self.DEFAULT_WIDTH)
        self.resizable(0,0)
        self.title("Scanning opened ports...")
        # ports_window = tkinter.Toplevel(self.master)
        # ports_window.geometry("500x300")
        # ports_window.resizable(0, 0)
        # ports_window.title("Ports in use")
        self.__add_components()

    def __add_components(self):
        progressbar = ttk.Progressbar(self, orient="horizontal", length=self.DEFAULT_WIDTH, mode="indeterminate")
        progressbar.place(x=25, y=25, width=200, height=20)

        # TODO: Center the button...
        self.__port_button = tkinter.Button(self, text="Cancel", state='active', command=self.__cancel_scan)
        self.__port_button.place(x=25, y=60, width=90, height=24)

    def __cancel_scan(self):
        # TODO: Delete this message once the functionality is working
        messagebox.showwarning("Cancel scan", "Scan cancelled")