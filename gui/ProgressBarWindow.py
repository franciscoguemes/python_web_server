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

    def __init__(self, master):
        self.__master = master
        Toplevel.__init__(self, master, height=self.DEFAULT_HEIGHT, width=self.DEFAULT_WIDTH)
        self.resizable(0,0)
        self.title("Scanning opened ports...")
        self.__add_components()
        print("After adding components...")

        # TODO: Change this, go for the approach of creating a class for the thread...
        # http://blog.acipo.com/python-threading-progress-indicators/
        # http://softwareramblings.com/2008/06/running-functions-as-threads-in-python.html
        # https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
        # https://realpython.com/intro-to-python-threading/#starting-a-thread

        # self.__opened_ports = None
        # port_scanner = PortScanner()
        # thread = threading.Thread(target=port_scanner.scan)
        # print("Before thread start")
        # thread.start()
        # print("After thread start")
        # while not port_scanner.is_scan_finished():
        #     print("Checking thread is alive...")
        #     # Get thread progress
        #     progress = port_scanner.get_progress()
        #     # Set progress in the bar...
        #     self.__progressbar['value'] = progress
        #     # sleep
        #     time.sleep(0.1)
        #
        # print("Before thread...")
        # thread.join()
        # print("After thread join...")
        #
        # print("At the very end...")

    def __add_components(self):
        self.__progressbar = ttk.Progressbar(self, orient="horizontal", length=self.DEFAULT_WIDTH, mode="determinate")
        self.__progressbar.place(x=25, y=25, width=200, height=20)

        # TODO: Center the button...
        self.__port_button = tkinter.Button(self, text="Cancel", state='active', command=self.__cancel_scan)
        self.__port_button.place(x=25, y=60, width=90, height=24)

    def __cancel_scan(self):
        # TODO: Delete this message once the functionality is working
        messagebox.showwarning("Cancel scan", "Scan cancelled")

    def set_progress(self, progress):
        self.__progressbar['value'] = progress

    # def get_opened_ports(self):
    #     return self.__opened_ports