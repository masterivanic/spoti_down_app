from tkinter import tix
from window import ApplicationInterface
import requests.exceptions as internetException
from tkinter.messagebox import showerror

from custom_tk import App
from authentication.views.user_form import AuthForm 


def launch_app():
    main_app = AuthForm()
    main_app.mainloop()
    if main_app.is_destroy:
        name = main_app.user_login
        app = App(name)
        app.mainloop()

    # try:
    #     app = App()
    #     # app = tix.Tk()
    #     # gui = ApplicationInterface(app)
    #     app.mainloop()
    # except internetException.ConnectionError as err:
    #     showerror(
    #         'Erreur', 'mauvaise connexion \n Vérifier votre connexion internet puis relancer')

# -------launch application
launch_app()
