#!/usr/bin/python3


import tkinter

window = tkinter.Tk()
window.geometry("731x557")
window.resizable(0,0)
window.title("PyWebServer")

settings_frame = tkinter.Frame(window,bg="blue",bd=5)
settings_frame.place(relx=0.5,rely=0.1, relwidth=0.75, relheight=0.3, anchor="n")

directory_label = tkinter.Label(settings_frame, anchor='w', justify='left', bd=4, text='Directory:')
directory_label.place(relx=0.05, rely=0.1, relwidth=0.2, relheight=0.33)

directory_entry = tkinter.Entry(settings_frame)
directory_entry.place(relx=0.3, rely=0.1, relwidth=0.5, relheight=0.33)

directory_button = tkinter.Button(settings_frame,text="...")
directory_button.place(relx=0.85, rely=0.1, relwidth=0.1, relheight=0.33)


console_frame = tkinter.Frame(window, bg="red",bd=10)
console_frame.place(relx=0.5, rely=0.4, relwidth=0.75, relheight=0.5, anchor="n")

# frame = tkinter.Frame(window,bg="#80c1ff",bd=5)
# frame.place(relx=0.5,rely=0.1, relwidth=0.75, relheight=0.1, anchor="n")

# entry = tkinter.Entry(frame, font=('Courier', 18))
# entry.place(relwidth=0.65, relheight=1) # Ommited parameters such as relx or rely are set to 0
#
# button = tkinter.Button(frame,text="Get Weather", font=('Courier', 12))
# button.place(relx=0.7, relwidth=0.3, relheight=1)
#
# lower_frame = tkinter.Frame(window, bg="#80c1ff",bd=10)
# lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor="n")
#
# label = tkinter.Label(lower_frame, font=('Courier', 14), anchor='nw', justify='left', bd=4)
# label.place(relwidth=1, relheight=1)


window.mainloop()