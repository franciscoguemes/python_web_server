import tkinter
from tkinter import Toplevel
from tkinter import ttk


class PortsWindow(Toplevel):
    DEFAULT_HEIGHT = 500
    DEFAULT_WIDTH = 300

    def __init__(self, master):
        self.__master = master
        Toplevel.__init__(self, master, height=self.DEFAULT_HEIGHT, width=self.DEFAULT_WIDTH)
        self.resizable(0,0)
        self.title("Ports in use")
        # ports_window = tkinter.Toplevel(self.master)
        # ports_window.geometry("500x300")
        # ports_window.resizable(0, 0)
        # ports_window.title("Ports in use")
        self.__add_components()

    def __add_components(self):
        pass
        # self.__add_directory_components()
        # self.__add_port_components()
        # self.__add_server_components()