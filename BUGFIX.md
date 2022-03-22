# Bugfix
This file contains a list of bugs to fix in the application

---- 
## BUG-0001 

When the application is executed directly from its python file in a different directory than
the directory where the application resides, then there is an error regarding the icon.

As example:

```shell
francisco@francisco-XPS-13-9370:~$ /home/francisco/git/Francisco/github/python_web_server/pyserver.py
Traceback (most recent call last):
  File "/home/francisco/git/Francisco/github/python_web_server/pyserver.py", line 23, in <module>
    main()
  File "/home/francisco/git/Francisco/github/python_web_server/pyserver.py", line 13, in main
    icon = PhotoImage(file="resources/webserver.png")
  File "/usr/lib/python3.6/tkinter/__init__.py", line 3545, in __init__
    Image.__init__(self, 'photo', name, cnf, master, **kw)
  File "/usr/lib/python3.6/tkinter/__init__.py", line 3501, in __init__
    self.tk.call(('image', 'create', imgtype, name,) + options)
_tkinter.TclError: couldn't open "resources/webserver.png": no such file or directory
francisco@francisco-XPS-13-9370:~$ set-title Error
```
This error is generated when trying to open the application from DbWS, but
the error is reproducible just by typing the following command in a terminal window:

```shell
/home/francisco/git/Francisco/github/python_web_server/pyserver.py
```

I suspect the error has to do with the fact that the pwd is not the same as where the
app is located _/home/francisco/git/Francisco/github/python_web_server_, I am trying
to execute the app from an external directory.

---- 
## BUG-0002



---- 
## BUG-0003 



---- 
## BUG-0004 



---- 
## BUG-0005 



