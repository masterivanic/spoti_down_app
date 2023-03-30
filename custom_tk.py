
from tkinter import Menu
from PIL import Image
from controller import Controller
from spotify import SpotifyCustomer
from spotify import APIConfig
from settings import settings

import tkinter as tk
import os
import tkinter
import tkinter.messagebox
import customtkinter
import asyncio


# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("green")

def get_api_configuration():
    conf = APIConfig
    conf.SPOTIFY_CLIENT_ID = settings.SPOTIFY_CLIENT_ID
    conf.USER_ID = settings.USER_ID
    conf.SPOTIPY_REDIRECT_URI = settings.SPOTIPY_REDIRECT_URI
    conf.SPOTIFY_CLIENT_SECRET_KEY = settings.SPOTIFY_CLIENT_SECRET_KEY
    conf.scopes = settings.scopes
    return conf


class App(customtkinter.CTk):
    """ main application interface """

    GLIPH_ICON_WIDTH = 20
    GLIPH_ICON_HEIGHT = 30

    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
    icon_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images/icon")
    logo = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logos1.png")), size=(250, 85))
    logo_welcome = customtkinter.CTkImage(Image.open(os.path.join(image_path, "panel.jpg")), size=(850, 85))
    pub_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(250, 100))

    #button logo's
    search_image = customtkinter.CTkImage(
        Image.open(os.path.join(image_path, "icon/rechercher.png")), 
        size=(GLIPH_ICON_WIDTH, GLIPH_ICON_HEIGHT)
    )
    transfert_image = customtkinter.CTkImage(
        Image.open(os.path.join(image_path, "icon/transférer.png")),
        size=(GLIPH_ICON_WIDTH, GLIPH_ICON_HEIGHT)
    )
    download_image = customtkinter.CTkImage(
        Image.open(os.path.join(image_path, "icon/télécharger.png")),
        size=(GLIPH_ICON_WIDTH, GLIPH_ICON_HEIGHT)
    )
    convert_image = customtkinter.CTkImage(
        Image.open(os.path.join(image_path, "icon/convertir.png")),
        size=(GLIPH_ICON_WIDTH, GLIPH_ICON_HEIGHT)
    )
    quit_image = customtkinter.CTkImage(
        Image.open(os.path.join(image_path, "icon/quitter.png")),
        size=(GLIPH_ICON_WIDTH, GLIPH_ICON_HEIGHT)
    )

    conf = get_api_configuration()
    
    def __init__(self):
        super().__init__()

        self.title("Ekila Downloader App")
        self.geometry(f"{1129}x{620}")
        self.resizable(1, 1)
        self.grid_rowconfigure(6, weight=2)
        self.columnconfigure(0, weight=0)

        self.menu_bar()
        self.header()
        self.sidebar()
        self.extrat_csv_son_panel()
        self.button_list()
        self.footer()
        sp_client = SpotifyCustomer(config=self.conf)
        self.controller = Controller(view=self, sp_client=sp_client)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(
            text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def get_path_file(self):
        """ get file path and insert in entry """

        path = self.controller.open_file()
        if self.csv_entry:
            if self.csv_entry.get() != '': self.csv_entry.delete(0, tkinter.END)
            self.csv_entry.insert(0, str(path))
            

    def sidebar(self):
        """ Setup side bar of the application """

        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0,width=250)
        self.sidebar_frame.grid(row=2, column=0, sticky="w")
        self.tabview = customtkinter.CTkTabview(self.sidebar_frame,width=250)
        self.tabview.grid(row=2, column=0)
        self.tabview.add("Actualités")
        self.tabview.add("Communiqués")

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, 
            text="Appearance Mode:", 
            anchor="w"
        )
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.pub = customtkinter.CTkLabel(self.sidebar_frame, text="", width=250, image=self.pub_image)
        self.pub.grid(row=7, column=0)
 
    def menu_bar(self):
        """ Setup menu bar of the application """

        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        menu_file = Menu(menu_bar, tearoff=0)
        menu_help = Menu(menu_bar, tearoff=0)

        menu_bar.add_cascade(label='Fichier', menu=menu_file)
        menu_bar.add_cascade(label='Aide', menu=menu_help)

        menu_file.add_cascade(label='Ouvrir un fichier csv', command=self.get_path_file)
        menu_file.add_cascade(label='Ouvrir un fichier audio', command=None)
        menu_file.add_cascade(label='Ouvrir un dossier contenant les sons',command=None)
        menu_file.add_separator()
        menu_file.add_cascade(label='Créer une playlist ekila', command=None)
        menu_file.add_cascade(
            label='Copier le lien de la playlist', command=None)
        menu_file.add_cascade(label='Supprimer une playlist', command=None)
        menu_file.add_separator()
        menu_file.add_cascade(label='Vider', command=None)
        menu_file.add_separator()
        menu_file.add_cascade(label='Quitter', command=self.quit)
        menu_help.add_command(label='A propos', command=self.about)

    def dashboard_title(self, frame):
        """ Print title on all dashboard interface """

        self.title_dash = customtkinter.CTkLabel(
            frame, 
            text="TABLEAU DE BORD",          
            font=customtkinter.CTkFont(size=15, weight="bold")
        )
        self.title_dash.grid(row=0, column=1, padx=250)
        
    def header(self):
        """ define the header of the application """

        self.user_label = customtkinter.CTkLabel(master=self, text="Username")
        self.user_label.grid(row=0, column=0, sticky="nw", padx=2)
        self.date_label = customtkinter.CTkLabel(master=self, text="Mardi 0/1/2")
        self.date_label.grid(row=0, column=1, ipadx=20, padx=50,  sticky="e")

        self.logo_container = customtkinter.CTkFrame(self, corner_radius=0, width=1100)
        self.logo_container.grid(row=1, column=0, columnspan=2)
        self.logo_label = customtkinter.CTkLabel(self.logo_container, text="", image=self.logo, width=250)
        self.logo_label.grid(row=0, column=0)
        self.panel_logo_label = customtkinter.CTkLabel(self.logo_container, text="",  width=850, image=self.logo_welcome)
        self.panel_logo_label.grid(row=0, column=1, padx=10)

    def extrat_csv_son_panel(self):
        """ main dashboard interface for read csv file """

        self.dashboard_frame = customtkinter.CTkFrame(self, corner_radius=0, width=850)
        self.dashboard_frame.grid(row=2, column=1, rowspan=4, columnspan=2, sticky="nsew")
        self.dashboard_title(self.dashboard_frame)

        self.file_path = tkinter.StringVar()
        customtkinter.CTkLabel(self.dashboard_frame, text="Fichier csv:").grid(column=1, row=1, sticky='w', pady=15, padx=5)
        self.csv_entry = customtkinter.CTkEntry(self.dashboard_frame, width=500, textvariable=self.file_path)
        self.csv_entry.grid(column=1, row=1, sticky='w', pady=15, padx=100)
        self.textbox_csv = customtkinter.CTkTextbox(self.dashboard_frame, width=800, height=250)
        self.textbox_csv.grid(row=2, column=1, pady=5, sticky="nw")
        self.generate_button = customtkinter.CTkButton(
            self.dashboard_frame, 
            corner_radius=15, 
            fg_color=("white", "#81f542"), 
            border_width=2, 
            text_color=("white", "#ffffff"), 
            text="Generer",
            command = lambda: self.generate_song(self.file_path.get())
        )
        self.generate_button.grid(row=3, column=1, pady=5, sticky="nw")
        self.progressbar = customtkinter.CTkProgressBar(
            self.dashboard_frame, 
            height=30,
            width=350,
            progress_color=('orange','#FFA500')
        )
        self.progressbar.grid(row=3, column=1, padx=150, sticky="nw")
        self.progressbar.set(0)
        # self.percentage = customtkinter.CTkLabel(self.dashboard_frame, text="1%", justify='center',
        # fg_color='transparent').grid(row=3, column=1,padx=250 , sticky='w')

    def generate_song(self, path:str):
        asyncio.run(self.controller.read_unique_file(path))
        
    
    def transfert_son_panel(self):
        """ dashboard interface for transfert sons in playlist """

        self.transfert_frame = customtkinter.CTkFrame(self, corner_radius=0, width=850)
        self.transfert_frame.grid(row=2, column=1, rowspan=4, columnspan=3, sticky="nsew")
        self.transfert_frame.columnconfigure(0, weight=1)
        self.transfert_frame.columnconfigure(1, weight=1)
        self.dashboard_title(self.transfert_frame)
     
        self.scrollable_sons_frame = customtkinter.CTkScrollableFrame(
            self.transfert_frame,
            label_text="Liste des sons",
            height=250,
        )
        self.scrollable_sons_frame.grid(row=1, column=1, sticky=tk.W+tk.E, pady=15)
        self.scrollable_sons_frame.grid_columnconfigure(0, weight=1)

        self.scrollable_sons_list = customtkinter.CTkScrollableFrame(
            self.transfert_frame,
            label_text="Liste de playlist",
            height=250,
        )
        self.scrollable_sons_list.grid(row=1,column=2, pady=15, sticky=tk.W+tk.E)
        self.scrollable_sons_list.grid_columnconfigure(0, weight=1)

        self.button_frame = customtkinter.CTkFrame(self.transfert_frame, corner_radius=0)
        self.button_frame.grid(row=2, column=1, sticky="w")
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)

        self.transfert_button = customtkinter.CTkButton(
            self.button_frame, 
            text="Transférer"
        )
        self.supprimer_button = customtkinter.CTkButton(
            self.button_frame, 
            text="Supprimer"
        )
        self.progressbar = customtkinter.CTkProgressBar(
            self.button_frame, 
            height=30, 
            width=350, 
            progress_color=('orange','#FFA500')
        )

        self.transfert_button.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.supprimer_button.grid(row=0, column=1, sticky=tk.W+tk.E, padx=3)
        self.progressbar.grid(row=0, column=2, sticky=tk.W+tk.E, padx=3)

    def download_son_panel(self):
        """ dashboard interface for download song """

        self.download_frame = customtkinter.CTkFrame(self, corner_radius=0, width=850)
        self.download_frame.grid(row=2, column=1, rowspan=4, columnspan=3, sticky="nsew")
        self.dashboard_title(self.download_frame)
        customtkinter.CTkLabel(self.download_frame, text="Lien playlist:").grid(
            column=1, 
            row=1,  
            sticky='w', 
            pady=15,
            padx=5
        )
        self.link_entry = customtkinter.CTkEntry(self.download_frame, width=500)
        self.link_entry.grid(column=1, row=1,  sticky='nsew', pady=15, padx=100)
        self.textbox = customtkinter.CTkTextbox(self.download_frame, width=800, height=250)
        self.textbox.grid(row=2, column=1, pady=5,  sticky='nw')
        self.download_sons_button = customtkinter.CTkButton(
            self.download_frame, 
            corner_radius=15,
            fg_color=("white", "#81f542"),
            border_width=2, 
            text_color=("white", "#ffffff"), 
            text="Télécharger"
        ).grid(row=3, column=1, pady=5,  sticky='nw')

        self.progressbar = customtkinter.CTkProgressBar(
            self.download_frame, 
            height=30, 
            width=350, 
            progress_color=('orange','#FFA500')
        ).grid(row=3, column=1, padx=150,  sticky='nw')

    def conversion_son_panel(self):
        """ dashboard interface for convert song in wav """

        self.conversion_frame = customtkinter.CTkFrame(self, corner_radius=0, width=850)
        self.conversion_frame.grid(row=2, column=1, rowspan=4, columnspan=3, sticky="nsew")
        self.dashboard_title(self.conversion_frame)
        customtkinter.CTkLabel(self.conversion_frame, text="sons mp3:").grid(
            column=1, 
            row=1,  
            sticky='w', 
            pady=15,
            padx=5
        )
        self.son_path_entry = customtkinter.CTkEntry(self.conversion_frame, width=500)
        self.son_path_entry.grid(column=1, row=1,  sticky='nsew', pady=15, padx=100)
        self.textbox = customtkinter.CTkTextbox(self.conversion_frame, width=800, height=250)
        self.textbox.grid(row=2, column=1, pady=5,  sticky='nw')
        self.menu_button = customtkinter.CTkFrame(self.conversion_frame, corner_radius=0)
        self.menu_button.grid(row=3, column=1, pady=5,  sticky='nw')

        self.menu_button.columnconfigure(0, weight=1)
        self.menu_button.columnconfigure(1, weight=1)
        self.menu_button.columnconfigure(2, weight=1)

        self.metadata_button = customtkinter.CTkButton(
            self.menu_button, 
            corner_radius=15,
            fg_color=("white", "#81f542"),
            border_width=2, 
            text_color=("white", "#ffffff"), 
            text="Metadata"
        )

        self.convert_sons_button = customtkinter.CTkButton(
            self.menu_button, 
            corner_radius=15,
            fg_color=("white", "#81f542"),
            border_width=2, 
            text_color=("white", "#ffffff"), 
            text="Convertir en wav"
        )

        self.progressbar = customtkinter.CTkProgressBar(
            self.menu_button, 
            height=30, 
            width=350, 
            progress_color=('orange','#FFA500')
        )

        self.metadata_button.grid(row=0, column=0, sticky=tk.W+tk.E, padx=10)
        self.convert_sons_button.grid(row=0, column=1, sticky=tk.W+tk.E, padx=10)
        self.progressbar.grid(row=0, column=2, sticky=tk.W+tk.E)

    def button_list(self):
        """ all pagination button for application """

        self.button_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.button_frame.grid(row=6, column=1, sticky="w")
        self.search_button = customtkinter.CTkButton(
            self.button_frame, 
            corner_radius=10, 
            text_color=("black", "#000000"), 
            text="Recherche fichier",
            image=self.search_image, 
            height=60,
            font=customtkinter.CTkFont(size=12, weight="bold"),
            command=lambda:self.paginate('Recherche fichier')
        )

        self.transfert_button = customtkinter.CTkButton(
            self.button_frame,
            corner_radius=10, 
            text_color=("black", "#000000"), 
            text="Transfert sons", 
            image=self.transfert_image, 
            height=60,
            font=customtkinter.CTkFont(size=12, weight="bold"),
            command=lambda:self.paginate('Transfert sons')
        )

        self.download_button = customtkinter.CTkButton(
            self.button_frame,
            corner_radius=10, 
            text_color=("black", "#000000"), 
            text="Télécharger sons", 
            image=self.download_image, 
            height=60,
            font=customtkinter.CTkFont(size=12, weight="bold"),
            command=lambda:self.paginate('Télécharger sons')
        )

        self.convert_button = customtkinter.CTkButton(
            self.button_frame,
            corner_radius=10, 
            text_color=("black", "#000000"), 
            text="Conversion sons", 
            image=self.convert_image, 
            height=60,
            font=customtkinter.CTkFont(size=12, weight="bold"),
            command=lambda:self.paginate('Conversion sons')
        )

        self.quit_button = customtkinter.CTkButton(
            self.button_frame, 
            corner_radius=10,
            text_color=("black", "#000000"), 
            text="Quitter", 
            image=self.quit_image,  
            height=60,
            font=customtkinter.CTkFont(size=12, weight="bold"),
            command=self.quit
        )

        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.columnconfigure(3, weight=1)
        self.button_frame.columnconfigure(4, weight=1)
    
        self.search_button.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.transfert_button.grid(row=0, column=1, sticky=tk.W+tk.E, padx=3)
        self.download_button.grid(row=0, column=2, sticky=tk.W+tk.E, padx=3)
        self.convert_button.grid(row=0, column=3, sticky=tk.W+tk.E, padx=3)
        self.quit_button.grid(row=0, column=4, sticky=tk.W+tk.E)

    def paginate(self, text):
        if text == 'Transfert sons':
            self.transfert_son_panel()
            self.controller.checkbox_playlist_output()
            asyncio.run(self.controller.song_panel())
        elif text == 'Télécharger sons':
            self.download_son_panel()
        elif text == 'Conversion sons':
            self.conversion_son_panel()
        elif text == 'Recherche fichier':
            self.extrat_csv_son_panel()

    def aside_element(self):
        """ Aside element for notification  """

        self.aside_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.aside_frame.grid(row=2, column=0, rowspan=4, padx=3)

        self.tabview = customtkinter.CTkTabview(self.aside_frame, width=250)
        self.tabview.grid(row=0, column=0, sticky='nw')
        self.tabview.add("Actualités")
        self.tabview.add("Communiqués")
        self.pub = customtkinter.CTkLabel(
            self.aside_frame, 
            text="", 
            image=self.pub_image
        )
        self.pub.grid(row=1, column=0, sticky='nw')

    def footer(self):
        """ application footer """

        self.footer_frame = customtkinter.CTkFrame(self)
        self.footer_frame.grid(row=9, column=1, sticky="nsew")
        self.footer_label = customtkinter.CTkLabel(
            self.footer_frame, text="Copyright MNLV Tous droits réservés",
            font=customtkinter.CTkFont(size=8, weight="bold")
        )
        self.footer_label.grid(row=0, column=1, columnspan=2, sticky='e', padx=300)

    def quit(self):
        """ to exit from application """

        from tkinter.messagebox import askyesno
        entry = askyesno(title='Exit', message='Etes vous sur de vouloir quitter?')
        if entry: self.destroy()

    def about(self):
        """ about application """

        from tkinter.messagebox import showinfo
        showinfo(
            title='A propos',
            message='Ekila Downloader v0.1, copyright MNLV Africa \n Droits réservés'
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
