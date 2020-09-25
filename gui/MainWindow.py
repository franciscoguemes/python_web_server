#!/usr/bin/env python3

import tkinter
from tkinter import ttk
from tkinter import filedialog


class MainWindow:

    def __init__(self):
        window = tkinter.Tk()
        window.geometry("731x557")
        window.resizable(0, 0)
        window.title("PyWebServer")