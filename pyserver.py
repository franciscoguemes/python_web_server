#!/usr/bin/python3

# The entire UI has been designed using the Pencil project: https://pencil.evolus.vn/
# By using this UI designer is it possible to see the coordinates and dimensions of each widget in the UI,
# therefore I have used the place method with absolute coordinates to place the widgets in the UI.

from tkinter import Tk, PhotoImage
from gui.MainWindow import MainWindow


def main():
    root = Tk()
    icon = PhotoImage(file="resources/webserver.png")
    root.iconphoto(True, icon)
    root.title("PyWebServer")
    root.resizable(0, 0)
    main_window = MainWindow(root)
    main_window.pack()
    root.mainloop()


if __name__ == "__main__":
    main()