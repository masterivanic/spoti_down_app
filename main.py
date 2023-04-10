from tkinter import tix
from tkinter.messagebox import showerror

import requests.exceptions as internetException

from authentication.views.user_form import AuthForm
from custom_tk import App
from window import ApplicationInterface


def launch_app():
    main_app = AuthForm()
    main_app.mainloop()
    if main_app.is_destroy:
        name = main_app.user_login
        app = App(name)
        app.mainloop()

    # try:
    #     app = App()
    #     app.mainloop()
    # except internetException.ConnectionError as err:
    #     showerror(
    #         'Erreur', 'mauvaise connexion \n Vérifier votre connexion internet puis relancer')


# -------launch application
launch_app()
