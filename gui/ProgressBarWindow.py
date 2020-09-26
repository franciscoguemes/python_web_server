import tkinter
from tkinter import Toplevel
from tkinter import ttk
from tkinter import messagebox
import threading
import time

from utils.PortScanner import PortScanner


class ProgressBarWindow(Toplevel):
    DEFAULT_HEIGHT = 100
    DEFAULT_WIDTH = 250

    def __init__(self, master, port_scaner):
        self.__master = master
        self.__port_scaner = port_scaner
        Toplevel.__init__(self, master, height=self.DEFAULT_HEIGHT, width=self.DEFAULT_WIDTH)
        self.resizable(0,0)
        self.title("Scanning opened ports...")
        self.__add_components()
        print("After adding components...")

    def __add_components(self):
        self.__progressbar = ttk.Progressbar(self, orient="horizontal", length=self.DEFAULT_WIDTH, mode="determinate")
        self.__progressbar.place(x=25, y=25, width=200, height=20)

        # TODO: Center the button...
        self.__port_button = tkinter.Button(self, text="Cancel", state='active', command=self.__cancel_scan)
        self.__port_button.place(x=25, y=60, width=90, height=24)

    def __cancel_scan(self):
        self.__port_scaner.cancel_scan()
        self.close_window()

    def set_progress(self, progress):
        self.__progressbar['value'] = progress

    def close_window(self):
        self.destroy()
        self.update()