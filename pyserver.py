#!/usr/bin/python3

# The entire UI has been designed using the Pencil project: https://pencil.evolus.vn/
# By using this UI designer is it possible to see the coordinates and dimensions of each widget in the UI,
# therefore I have used the place method with absolute coordinates to place the widgets in the UI.

import tkinter
from tkinter import filedialog
import subprocess
import threading
import sys
import asyncio
import time
import queue


# Default port to initialize the server...
DEFAULT_PORT = 8000

DEFAULT_DIRECTORY = '/home/francisco/Pictures'

web_server_process = None
thread_event_handler = None
loop = None


class AsynchronousFileReader(threading.Thread):
    """
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    """
    def __init__(self, fd, que):
        assert isinstance(que, queue.Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._que = que

    def run(self):
        """ The body of the tread: read lines and put them on the queue."""
        for line in iter(self._fd.readline, b''):
            if line != b'':
                self._que.put(line)

    def eof(self):
        """Check whether there is no more content to expect."""
        return not self.is_alive() and self._que.empty()


# def read_stdout(child_process):
#     while child_process.poll() is None:
#         out_stdout = child_process.stdout.readline()
#         #print("I am in stdout")
#         if out_stdout != b'':
#             #print(out_stdout.decode(sys.stdout.encoding))
#             sys.stdout.write(out_stdout.decode(sys.stdout.encoding))
#             sys.stdout.flush()


# def read_stderr(child_process):
#     while child_process.poll() is None:
#         out_stderr = child_process.stderr.readline()
#         #print("I am in stderr")
#         if out_stderr != b'':
#             #print(out_stderr.decode(sys.stderr.encoding))
#             sys.stdout.write(out_stderr.decode(sys.stderr.encoding))
#             sys.stdout.flush()


# def execute_server(port, directory):
#     global web_server_process
#     web_server_process = subprocess.Popen(['python3', '-m', 'http.server', str(port)],
#                              stdin=None,
#                              stdout=subprocess.PIPE,
#                              stderr=subprocess.PIPE,
#                              close_fds=True)
#     print(web_server_process.pid)
#     thread_read_stdout = threading.Thread(target=read_stdout, args=(web_server_process,))
#     thread_read_stderr = threading.Thread(target=read_stderr, args=(web_server_process,))
#     thread_read_stdout.start()
#     thread_read_stderr.start()
#     print("After starting the threads")
#     # global loop
#     # loop = asyncio.get_event_loop()
#     # loop.call_soon(_stream_subprocess(['python3', '-m', 'http.server', str(port)], print_stdout, print_stderr))
#     # loop.run_forever()
#     thread_read_stdout.join()
#     thread_read_stderr.join()
#     print("After joining")


def execute_server(port, directory):
    global web_server_process
    # The -u parameter is needed in order the http.server to not buffer the output: https://stackoverflow.com/a/43250818/1866109
    command = ['python3', '-u', '-m', 'http.server', str(port)]
    #cmd = "ping -c4 www.franciscoguemes.com && sleep 1 && echo this would be an error! 1>&2 "
    #command = ["bash", "-c", cmd]
    web_server_process = subprocess.Popen(command,
                             stdin=None,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             close_fds=True)

    # Launch the asynchronous readers of the process' stdout and stderr.
    stdout_queue = queue.Queue()
    stdout_reader = AsynchronousFileReader(web_server_process.stdout, stdout_queue)
    stdout_reader.start()
    stderr_queue = queue.Queue()
    stderr_reader = AsynchronousFileReader(web_server_process.stderr, stderr_queue)
    stderr_reader.start()

    print("Before the loop")
    # Check the queues if we received some output (until there is nothing more to get).
    while not stdout_reader.eof() or not stderr_reader.eof():
        # Show what we received from standard output.
        while not stdout_queue.empty():
            line = stdout_queue.get()
            if line != b'':
                print(line.decode(sys.stdout.encoding), flush=True)
                #sys.stdout.write(line.decode(sys.stdout.encoding))
                #sys.stdout.flush()

        # Show what we received from standard error.
        while not stderr_queue.empty():
            line = stderr_queue.get()
            if line != b'':
                print(line.decode(sys.stderr.encoding), flush=True)
                #sys.stdout.write(line.decode(sys.stderr.encoding))
                #sys.stdout.flush()

        # Sleep a bit before asking the readers again.
        time.sleep(.1)

    print("Before join")
    # Let's be tidy and join the threads we've started.
    stdout_reader.join()
    stderr_reader.join()


def print_stdout(line):
    print(f"STDOUT:{line}")


def print_stderr(line):
    print(f"STDERR:{line}")


def select_directory():
    directory = filedialog.askdirectory()
    directory_text.set(directory)


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
radio_8000 = tkinter.Radiobutton(window, text=str(DEFAULT_PORT), anchor="w", variable=selected_radio_button, value=1)
radio_8000.place(x=162, y=83, width=70, height=14)
radio_port = tkinter.Radiobutton(window, text="", anchor="w", variable=selected_radio_button, value=2)
radio_port.place(x=162, y=120, width=70, height=14)
selected_radio_button.set(1)

port_entry = tkinter.Entry(window)
port_entry.place(x=184, y=115, width=71, height=21)

port_button = tkinter.Button(window, text="...")
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



