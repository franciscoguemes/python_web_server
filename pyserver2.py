#!/usr/bin/python3

# The entire UI has been designed using the Pencil project: https://pencil.evolus.vn/
# By using this UI designer is it possible to see the coordinates and dimensions of each widget in the UI,
# therefore I have used the place method with absolute coordinates to place the widgets in the UI.

import tkinter
from tkinter import ttk
from tkinter import filedialog
import subprocess
import threading
import sys
import asyncio
import time
import queue
import os
import socket


# Default port to initialize the server...
DEFAULT_PORT = 8000

DEFAULT_DIRECTORY = '/home/francisco/Pictures'

DEFAULT_SERVER = 'localhost' \


web_server_process = None
thread_event_handler = None
loop = None


def read_stdout(child_process, call_back):
    while child_process.poll() is None:
        out_stdout = child_process.stdout.readline()
        # print("I am in stdout")
        if out_stdout != b'':
            call_back(out_stdout, True)
            # print(out_stdout.decode(sys.stdout.encoding))
            sys.stdout.write(out_stdout.decode(sys.stdout.encoding))
            sys.stdout.flush()


def read_stderr(child_process, call_back):
    while child_process.poll() is None:
        out_stderr = child_process.stderr.readline()
        # print("I am in stderr")
        if out_stderr != b'':
            call_back(out_stderr, False)
            # print(out_stderr.decode(sys.stderr.encoding))
            sys.stdout.write(out_stderr.decode(sys.stderr.encoding))
            sys.stdout.flush()


def execute_server(port, directory):
    global web_server_process
    # Change to the http path to serve: https://stackoverflow.com/a/39801780/1866109
    web_dir = os.path.join(directory)
    os.chdir(web_dir)
    # Start the server...
    # The -u parameter is needed in order the http.server to not buffer the output: https://stackoverflow.com/a/43250818/1866109
    command = ['python3', '-u', '-m', 'http.server', str(port)]
    web_server_process = subprocess.Popen(command,
                             stdin=None,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             close_fds=True)
    print(web_server_process.pid)
    # Start the threads that reads from the pipes...
    thread_read_stdout = threading.Thread(target=read_stdout, args=(web_server_process, show_text))
    thread_read_stderr = threading.Thread(target=read_stderr, args=(web_server_process, show_text))
    thread_read_stdout.start()
    thread_read_stderr.start()
    print("After starting the threads")
    thread_read_stdout.join()
    thread_read_stderr.join()
    print("After joining")


def print_stdout(line):
    print(f"STDOUT:{line}")


def print_stderr(line):
    print(f"STDERR:{line}")


def show_text(line, is_stdout):
    console_text.config(state='normal')

    if is_stdout is True:
        console_text.insert(tkinter.END, line)
    else:
        # TODO: Add here your syntax higlighter for stderr
        console_text.insert(tkinter.END, line)

    console_text.config(state='disabled')


def select_directory():
    directory = filedialog.askdirectory()
    #print(type(directory))
    #print(directory)
    if not directory:
        directory_text.set(DEFAULT_DIRECTORY)
    else:
        directory_text.set(directory)


def activate_port_selection_widgets(activate=True):
    if activate:
        port_entry.configure(state="normal")
        port_button.configure(state="normal")
    else:
        port_entry.configure(state="disabled")
        port_button.configure(state="disabled")


def get_opened_ports():
    list_of_ports = ""
    for port in range(1, 65535):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((DEFAULT_SERVER, port))
        if result == 0:
            list_of_ports += "Port {: >5}: 	 Open\n".format(port)
        sock.close()
    return list_of_ports;


def show_opened_ports():
    ports_window = tkinter.Toplevel(window)
    ports_window.geometry("500x300")
    ports_window.resizable(0, 0)
    ports_window.title("Ports in use")

    # TODO: Show a progressbar
    # https://stackoverflow.com/questions/7310511/how-to-create-downloading-progress-bar-in-ttk
    # https://www.programiz.com/python-programming/time/sleep#:~:text=time.-,sleep()%20in%20multithreaded%20programs,whole%20process%20in%20multithreaded%20programs.
    progressbar = ttk.Progressbar(ports_window, orient="horizontal", length=200, mode="indeterminate")
    progressbar.pack(side=tkinter.TOP)
    time.sleep(2)

    scrollbar = tkinter.Scrollbar(ports_window)
    textarea = tkinter.Text(ports_window, height=3, width=50)
    # scrollbar.pack()

    # TODO: Use a thread here while the port scan is taking place...
    ports_in_use = get_opened_ports()
    # quote = """HAMLET: To be, or not to be--that is the question:
    # Whether 'tis nobler in the mind to suffer
    # The slings and arrows of outrageous fortune
    # Or to take arms against a sea of troubles
    # And by opposing end them. To die, to sleep--
    # No more--and by a sleep to say we end
    # The heartache, and the thousand natural shocks
    # That flesh is heir to. 'Tis a consummation
    # Devoutly to be wished."""

    # TODO: Add here the widgets to show the ports in use...
    # https://www.python-course.eu/tkinter_text_widget.php
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    textarea.pack(side=tkinter.LEFT, fill=tkinter.Y)
    scrollbar.config(command=textarea.yview)
    textarea.config(yscrollcommand=scrollbar.set)
    textarea.insert(tkinter.END, ports_in_use)
    textarea.configure(state="disabled")


def get_selected_port():
    if selected_radio_button.get() == 1:
        return DEFAULT_PORT
    else: # TODO: Improve the conversion, handle errors...
        return int(port_entry.get())


def start_server():
    global web_server_process
    # Update start_button...
    start_button_text.set("Stop Web Server")
    start_button.configure(command=stop_server)
    # Gather the information...
    directory = directory_entry.get()
    port = get_selected_port()
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

    global thread_event_handler
    thread_event_handler = threading.Thread(target=execute_server, args=(port, directory))
    thread_event_handler.start()


def stop_server():
    # loop.stop()
    # loop.close()
    start_button_text.set("Start Web Server")
    start_button.configure(command=start_server)

    # https://www.reddit.com/r/learnpython/comments/52scfk/what_is_the_difference_between_popens_terminate/d7mx12b/
    web_server_process.kill()
    # https://askubuntu.com/a/427222/227301
    web_server_process.wait()

    # Close subprocess' file descriptors.
    web_server_process.stdout.close()
    web_server_process.stderr.close()


window = tkinter.Tk()
window.geometry("731x557")
window.resizable(0,0)
window.title("PyWebServer")

directory_label = tkinter.Label(window, anchor='w', justify='left', bd=4, text='Directory:')
directory_label.place(x=87, y=47, width=70, height=14)

directory_text = tkinter.StringVar()
directory_text.set(DEFAULT_DIRECTORY)
directory_entry = tkinter.Entry(window, textvariable=directory_text)
directory_entry.place(x=161, y=43, width=350, height=21)

directory_button = tkinter.Button(window, text="...", command=select_directory)
directory_button.place(x=535, y=43, width=90, height=24)

port_label = tkinter.Label(window, anchor='w', justify='left', bd=4, text='Port:')
port_label.place(x=88, y=83, width=50, height=14)

selected_radio_button = tkinter.IntVar()
radio_8000 = tkinter.Radiobutton(window, text=str(DEFAULT_PORT), anchor="w", variable=selected_radio_button, value=1,
                                 command=lambda: activate_port_selection_widgets(False))
radio_8000.place(x=162, y=83, width=70, height=14)
radio_port = tkinter.Radiobutton(window, text="", anchor="w", variable=selected_radio_button, value=2,
                                 command=lambda: activate_port_selection_widgets(True))
radio_port.place(x=162, y=120, width=70, height=14)
selected_radio_button.set(1)

port_entry = tkinter.Entry(window, state='disabled')
port_entry.place(x=184, y=115, width=71, height=21)

port_button = tkinter.Button(window, text="Scan ports", state='disabled', command=show_opened_ports)
port_button.place(x=266, y=113, width=90, height=24)

start_button_text = tkinter.StringVar()
start_button_text.set("Start Web Server")
start_button = tkinter.Button(window, textvariable=start_button_text, command=start_server)
start_button.place(x=250, y=169, width=168, height=24)

#output = tkinter.StringVar()
#output.set('Console for showing HTTP server output...')
#console_label = tkinter.Label(window,  anchor='nw', justify='left', bg='white', textvariable=output)
#console_label.place(x=45, y=212, width=648, height=317)

console_text = tkinter.Text(window, bg='white', state='disabled')
console_text.place(x=45, y=212, width=648, height=317)
scrollbar = tkinter.Scrollbar(console_text, command=console_text.yview)
console_text.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

# quote = """
# To be, or not to be, that is the question:
# Whether 'tis Nobler in the mind to suffer
# The Slings and Arrows of outrageous Fortune,
# Or to take Arms against a Sea of troubles,
# """
# console_text.config(state='normal')
# console_text.insert(tkinter.END, quote, 'color')
# console_text.insert(tkinter.END, 'follow-up\n', 'follow')
# console_text.config(state='disabled')

window.mainloop()



