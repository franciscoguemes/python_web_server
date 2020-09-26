import threading
import time
import tkinter
from tkinter import Frame
from tkinter import ttk
from tkinter import filedialog

from gui.PortsWindow import PortsWindow
from gui.ProgressBarWindow import ProgressBarWindow
from utils.PortScanner import PortScanner


class MainWindow(Frame):
    DEFAULT_HEIGHT = 551
    DEFAULT_WIDTH = 731

    DEFAULT_DIRECTORY = '/home/francisco/Pictures'
    # Default port to initialize the server...
    DEFAULT_PORT = 8000
    DEFAULT_SERVER = 'localhost'

    def __init__(self, master):
        self.__master = master
        Frame.__init__(self, master, height=self.DEFAULT_HEIGHT, width=self.DEFAULT_WIDTH)
        self.__add_components()

    def __add_components(self):
        self.__add_directory_components()
        self.__add_port_components()
        self.__add_server_components()

    def __add_directory_components(self):
        directory_label = tkinter.Label(self, anchor='w', justify='left', bd=4, text='Directory:')
        directory_label.place(x=87, y=47, width=70, height=14)

        self.__directory_text = tkinter.StringVar()
        self.__directory_text.set(self.DEFAULT_DIRECTORY)
        directory_entry = tkinter.Entry(self, textvariable=self.__directory_text)
        directory_entry.place(x=161, y=43, width=350, height=21)

        directory_button = tkinter.Button(self, text="...", command=self.__select_directory)
        directory_button.place(x=535, y=43, width=90, height=24)

    def __select_directory(self):
        directory = filedialog.askdirectory()
        #print(type(directory))
        #print(directory)
        if not directory:
            self.__directory_text.set(self.DEFAULT_DIRECTORY)
        else:
            self.__directory_text.set(directory)

    def __add_port_components(self):
        port_label = tkinter.Label(self, anchor='w', justify='left', bd=4, text='Port:')
        port_label.place(x=88, y=83, width=50, height=14)

        self.__selected_radio_button = tkinter.IntVar()
        radio_8000 = tkinter.Radiobutton(self, text=str(self.DEFAULT_PORT), anchor="w",
                                         variable=self.__selected_radio_button,
                                         value=1,
                                         command=lambda: self.__activate_port_selection_widgets(False))
        radio_8000.place(x=162, y=83, width=70, height=14)

        radio_port = tkinter.Radiobutton(self, text="", anchor="w",
                                         variable=self.__selected_radio_button,
                                         value=2,
                                         command=lambda: self.__activate_port_selection_widgets(True))
        radio_port.place(x=162, y=120, width=70, height=14)
        self.__selected_radio_button.set(1)

        self.__port_entry = tkinter.Entry(self, state='disabled')
        self.__port_entry.place(x=184, y=115, width=71, height=21)

        self.__port_button = tkinter.Button(self, text="Scan ports", state='disabled', command=self.__show_opened_ports)
        self.__port_button.place(x=266, y=113, width=90, height=24)

        # TODO: Delete this 2 lines after development...
        self.__selected_radio_button.set(2)
        self.__activate_port_selection_widgets(True)

    def __activate_port_selection_widgets(self, activate=True):
        if activate:
            self.__port_entry.configure(state="normal")
            self.__port_button.configure(state="normal")
        else:
            self.__port_entry.configure(state="disabled")
            self.__port_button.configure(state="disabled")

    def __show_opened_ports(self):
        # Create here a separate thread that will show the progressbar and then the ports window
        thread = threading.Thread(target=self.__show_progressbar, daemon=True)
        thread.start()

    def __show_progressbar(self):
        progressbar_window = ProgressBarWindow(self)

        port_scanner = PortScanner()
        thread = threading.Thread(target=port_scanner.scan)
        print("Before thread start")
        thread.start()
        print("After thread start")
        while not port_scanner.is_scan_finished():
            # Get thread progress
            progress = port_scanner.get_progress()
            print(f"progress={progress}")
            # Set progress in the bar...
            progressbar_window.set_progress(progress)
            # sleep
            time.sleep(0.1)

        progressbar_window.set_progress(100)
        thread.join()

        progressbar_window.destroy()
        progressbar_window.update()
        report = port_scanner.get_report()

        # Show the ports window
        ports_window = PortsWindow(self, report)

    def __add_server_components(self):
        pass
        # start_button_text = tkinter.StringVar()
        # start_button_text.set("Start Web Server")
        # start_button = tkinter.Button(self, textvariable=start_button_text, command=start_server)
        # start_button.place(x=250, y=169, width=168, height=24)
        #
        # # output = tkinter.StringVar()
        # # output.set('Console for showing HTTP server output...')
        # # console_label = tkinter.Label(window,  anchor='nw', justify='left', bg='white', textvariable=output)
        # # console_label.place(x=45, y=212, width=648, height=317)
        #
        # console_text = tkinter.Text(self, bg='white', state='disabled')
        # console_text.place(x=45, y=212, width=648, height=317)
        # scrollbar = tkinter.Scrollbar(console_text, command=console_text.yview)
        # console_text.config(yscrollcommand=scrollbar.set)
        # scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
