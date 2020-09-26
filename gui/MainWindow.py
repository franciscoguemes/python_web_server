import os
import subprocess
import sys
import threading
import time
import tkinter
from tkinter import Frame
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

    web_server_process = None
    thread_event_handler = None

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
        self.__directory_entry = tkinter.Entry(self, textvariable=self.__directory_text)
        self.__directory_entry.place(x=161, y=43, width=350, height=21)

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
        port_scanner = PortScanner()
        progressbar_window = ProgressBarWindow(self, port_scanner)
        thread = threading.Thread(target=port_scanner.scan)
        thread.start()
        while not port_scanner.is_scan_finished():
            progress = port_scanner.get_progress()
            # print(f"progress={progress}")
            progressbar_window.set_progress(progress)
            time.sleep(0.1)

        if not port_scanner.is_scan_cancelled():
            progressbar_window.set_progress(100)
            thread.join()
            progressbar_window.close_window()
            report = port_scanner.get_report()
            ports_window = PortsWindow(self, report)

    def __add_server_components(self):
        self.__start_button_text = tkinter.StringVar()
        self.__start_button_text.set("Start Web Server")
        self.__start_button = tkinter.Button(self, textvariable=self.__start_button_text, command=self.__start_server)
        self.__start_button.place(x=250, y=169, width=168, height=24)

        # output = tkinter.StringVar()
        # output.set('Console for showing HTTP server output...')
        # console_label = tkinter.Label(window,  anchor='nw', justify='left', bg='white', textvariable=output)
        # console_label.place(x=45, y=212, width=648, height=317)

        self.__console_text = tkinter.Text(self, bg='white', state='disabled')
        self.__console_text.place(x=45, y=212, width=648, height=317)
        scrollbar = tkinter.Scrollbar(self.__console_text, command=self.__console_text.yview)
        self.__console_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

    def __start_server(self):
        #global web_server_process

        # Update start_button...
        self.__start_button_text.set("Stop Web Server")
        self.__start_button.configure(command=self.__stop_server)
        # Gather the information...
        directory = self.__directory_entry.get()
        port = self.__get_selected_port()
        print(f"python3 -m http.server {port} --directory {directory}")
        # Change to the directory...
        subprocess.run(["cd", directory], shell=True, check=True)
        # Start the web server...   --> https://stackoverflow.com/questions/3516007/run-process-and-dont-wait
        #                           --> https://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/
        #                           --> https://www.aeracode.org/2018/02/19/python-async-simplified/

        # web_server_process = subprocess.Popen(['python3', '-m', 'http.server', str(port)],
        #                          stdin=None,
        #                          stdout=None,
        #                          stderr=None,
        #                          close_fds=True)
        # print(web_server_process.pid)

        # global thread_event_handler
        self.__thread_event_handler = threading.Thread(target=self.__execute_server, args=(port, directory))
        self.__thread_event_handler.start()

    def __get_selected_port(self):
        if self.__selected_radio_button.get() == 1:
            return self.DEFAULT_PORT
        else:  # TODO: Improve the conversion, handle errors...
            return int(self.__port_entry.get())

    def __stop_server(self):
        # loop.stop()
        # loop.close()
        self.__start_button_text.set("Start Web Server")
        self.__start_button.configure(command=self.__start_server)

        # https://www.reddit.com/r/learnpython/comments/52scfk/what_is_the_difference_between_popens_terminate/d7mx12b/
        self.__web_server_process.kill()
        # https://askubuntu.com/a/427222/227301
        self.__web_server_process.wait()

        # Close subprocess' file descriptors.
        self.__web_server_process.stdout.close()
        self.__web_server_process.stderr.close()

    def __execute_server(self, port, directory):
        # global web_server_process
        # Change to the http path to serve: https://stackoverflow.com/a/39801780/1866109
        web_dir = os.path.join(directory)
        os.chdir(web_dir)
        # Start the server...
        # The -u parameter is needed in order the http.server to not buffer the output: https://stackoverflow.com/a/43250818/1866109
        command = ['python3', '-u', '-m', 'http.server', str(port)]
        self.__web_server_process = subprocess.Popen(command,
                                              stdin=None,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE,
                                              close_fds=True)
        print(self.__web_server_process.pid)
        # Start the threads that reads from the pipes...
        thread_read_stdout = threading.Thread(target=self.__read_stdout, args=(self.__web_server_process, self.__show_text))
        thread_read_stderr = threading.Thread(target=self.__read_stderr, args=(self.__web_server_process, self.__show_text))
        thread_read_stdout.start()
        thread_read_stderr.start()
        print("After starting the threads")
        thread_read_stdout.join()
        thread_read_stderr.join()
        print("After joining")

    def __read_stdout(self, child_process, call_back):
        while child_process.poll() is None:
            out_stdout = child_process.stdout.readline()
            # print("I am in stdout")
            if out_stdout != b'':
                call_back(out_stdout, True)
                # print(out_stdout.decode(sys.stdout.encoding))
                sys.stdout.write(out_stdout.decode(sys.stdout.encoding))
                sys.stdout.flush()

    def __read_stderr(self, child_process, call_back):
        while child_process.poll() is None:
            out_stderr = child_process.stderr.readline()
            # print("I am in stderr")
            if out_stderr != b'':
                call_back(out_stderr, False)
                # print(out_stderr.decode(sys.stderr.encoding))
                sys.stdout.write(out_stderr.decode(sys.stderr.encoding))
                sys.stdout.flush()

    def __show_text(self, line, is_stdout):
        self.__console_text.config(state='normal')

        if is_stdout is True:
            self.__console_text.insert(tkinter.END, line)
        else:
            # TODO: Add here your syntax higlighter for stderr
            self.__console_text.insert(tkinter.END, line)

        self.__console_text.config(state='disabled')

    def print_stdout(line):
        print(f"STDOUT:{line}")

    def print_stderr(line):
        print(f"STDERR:{line}")