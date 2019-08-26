#!/usr/bin/python3

# The entire UI has been designed using the Pencil project: https://pencil.evolus.vn/
# By using this UI designer is it possible to see the coordinates and dimensions of each widget in the UI,
# therefore I have used the place method with absolute coordinates to place the widgets in the UI.

import tkinter
from tkinter import filedialog
import subprocess
import os

# Default port to initialize the server...
from subprocess import Popen

DEFAULT_PORT = 8000

DEFAULT_DIRECTORY = '/home/francisco/Pictures'

web_server_process = None


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
    #Update start_button...
    start_button_text.set("Stop Web Server")
    start_button.configure(command=stop_server)
    #Gather the information...
    directory = directory_entry.get()
    port = get_selected_port()
    print(f"python3 -m http.server {port} --directory {directory}")
    # Change to the directory...
    subprocess.run(["cd", directory], shell=True, check=True)
    # Start the web server...   --> https://stackoverflow.com/questions/3516007/run-process-and-dont-wait
    #                           --> https://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/
    web_server_process = subprocess.Popen(['python3', '-m', 'http.server', str(port)],
                             stdin=None,
                             stdout=None,
                             stderr=None,
                             close_fds=True)
    print(web_server_process.pid)


def stop_server():
    start_button_text.set("Start Web Server")
    start_button.configure(command=start_server)
    web_server_process.terminate()


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
