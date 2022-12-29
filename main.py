from tkinter import *
from window import ApplicationInterface

def launch_app():
    app = Tk()
    gui = ApplicationInterface(app)
    print(ApplicationInterface.__doc__)
    app.mainloop()

#-------launch application
launch_app()