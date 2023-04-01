from tkinter import tix
from window import ApplicationInterface
import requests.exceptions as internetException
from tkinter.messagebox import showerror

from custom_tk import App

def launch_app():
    try:
        app = App()
        # app = tix.Tk()
        # gui = ApplicationInterface(app)
        app.mainloop()
    except internetException.ConnectionError as err:
        showerror(
            'Erreur', 'mauvaise connexion \n Vérifier votre connexion internet puis relancer')

# -------launch application
launch_app()
