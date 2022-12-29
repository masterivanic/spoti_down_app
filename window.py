# coding:utf-8

from tkinter import *
from tkinter.ttk import Treeview
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from tkinter.messagebox import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning, showerror
from spotify import SpotifyCustomer
from exceptions import SpotifyCustomerException
import csv
import asyncio
import logging
import sys
import os
import tkinter
import eyed3
import music_tag
from pydub import AudioSegment
from tkinter import tix
from PIL import Image, ImageTk

__all__ = ["SpotifyCustomerException"]


class ApplicationInterface:

    """
        this file permit us to generate
        a GUI for user to enter information.
    """
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
        filename='error.log',
        level=logging.DEBUG,
        datefmt='%m/%d/%Y %I:%M:%S %p',
    )
    SPOTIFY_TRACK_URI = 'https://open.spotify.com/track/'
    global logger
    logger = logging.getLogger(__name__)

    def __init__(self, master) -> None:
        self.file = None
        self.file_mp3 = None
        self.master = master
        self.search_songs = []
        self.spotify_client = SpotifyCustomer()
        master.title('Spotify Download')
        master.resizable(width=True, height=True)

        # setup toolbar----------------------------------------------------
        menu_bar = Menu(master)

        master.config(menu=menu_bar)

        menu_file = Menu(menu_bar, tearoff=0)
        menu_help = Menu(menu_bar, tearoff=0)

        menu_bar.add_cascade(label='Fichier', menu=menu_file)
        menu_bar.add_cascade(label='Aide', menu=menu_help)

        menu_file.add_cascade(
            label='Ouvrir un fichier csv', command=self.open_file)
        menu_file.add_cascade(
            label='Ouvrir un fichier audio', command=self.open_file_mp3)
        menu_file.add_cascade(label='Ouvrir un dossier',
                              command=self.open_song_folder)
        menu_file.add_separator()
        menu_file.add_cascade(
            label='Creer une playlist spotify', command=self.create_playlists)
        menu_file.add_separator()
        menu_file.add_cascade(label='Vider', command=self.clear_all)
        menu_file.add_separator()
        menu_file.add_cascade(label='Quitter', command=self.quit)
        menu_help.add_command(label='A propos', command=self.about)

        # setup bar navigation----------------------------------------------
        note = ttk.Notebook(master, width=900, height=400)
        note.grid_rowconfigure(0, weight=1)
        note.grid_columnconfigure(0, weight=1)
        note.grid(row=0, pady=10)

        self.page_one = ttk.Frame(note)
        self.page_one.grid(row=0, column=0)

        self.page_two = ttk.Frame(note)
        self.page_two.grid(row=0, column=1)

        self.page_tree = ttk.Frame(note)
        self.page_tree.grid(row=0, column=2)

        note.add(self.page_one, text='Spotify stream')
        note.add(self.page_two, text='Modified music name')
        note.add(self.page_tree, text='Insert song in playlist')

        # setup widget 😀 ----------------------------------------------------

        # Label(self.page_one, text='Welcome to your spotify extrator', font='Helvetica 12 bold').grid(
        #     row=3, columnspan=3, pady=10, padx=15)

        # ---------------------- first window -------------------------------------
        self.file_path = StringVar()
        Label(self.page_one, text="Fichier CSV:", font='Helvetica 10 bold').grid(
            row=4, columnspan=3, pady=10, padx=15)
        self.entry = Entry(self.page_one, width=60,
                           textvariable=self.file_path)
        self.entry.grid(row=4, column=3, pady=10, ipady=6)

        Label(self.page_one, text="Liens spotify:", font='Helvetica 10 bold').grid(
            row=5, columnspan=3, pady=10, padx=15)

        self.text = ScrolledText(
            self.page_one, height=10, width=80, pady=2, padx=3, undo=True)
        self.text.grid(row=5, column=3, pady=10, ipady=6)
        self.text.focus()
        self.text.pack_forget()
        Button(self.page_one, text="Generer", width=10, bg='green',
               command=self.generate_link).grid(row=6, column=1, padx=1, pady=10, ipady=6)

        # ---------------------- second window -------------------------------------
        self.song_path = StringVar()
        Label(self.page_two, text="Fichier mp3:", font='Helvetica 10 bold').grid(
            row=4, columnspan=3, pady=10, padx=15)
        self.entry_song_path = Entry(
            self.page_two, width=60, textvariable=self.song_path, cursor=None)
        self.entry_song_path.grid(row=4, column=3, pady=10, ipady=6)

        Label(self.page_two, text="Fichier renommé:", font='Helvetica 10 bold').grid(
            row=5, columnspan=3, pady=10, padx=15)
        self.song_rename = ScrolledText(
            self.page_two, height=10, width=80, pady=2, padx=3, undo=True)
        self.song_rename.grid(row=5, column=3, pady=10, ipady=6)
        Button(self.page_two, text="Renommer", width=10, bg='red',
               command=self.rename_audio_file).grid(row=6, column=1, padx=10, pady=10, ipady=6)
        Button(self.page_two, text="Modifier metadata", width=15, bg='green',
               command=self.modify_metadata).grid(row=6, column=2, padx=10, pady=10, ipady=6)
        Button(self.page_two, text="Convertir en wav", width=15, bg='white', fg='black',
               command=self.run_song_convert).grid(row=6, column=3, padx=10, pady=10, ipady=6)

        # ---------------------- third window -------------------------------------

        self.frame = Frame(self.page_tree)
        self.frame.grid(row=0, column=0, columnspan=5, padx=5, pady=10)

        self.btn_frame = Frame(self.page_tree)
        self.btn_frame.grid(row=0, column=6, padx=5)

        self.image = Image.open("transfer.png")
        btn_photo = ImageTk.PhotoImage(self.image)
        Button(self.btn_frame, image=btn_photo,
               command=None).pack(side=tkinter.RIGHT)

        self.frame_playlist = Frame(self.page_tree)
        self.frame_playlist.grid(
            row=0, column=8, columnspan=5, padx=150, pady=10)

        self.playlist_panel()

        # Button(self.btn_frame, text="Transferer", width=15, bg='green',
        #        command=None).pack(side=tkinter.BOTTOM, padx=280)

    def create_checklist(self, frame: Frame, name: str, list_title: str):
        self.cl = tix.CheckList(frame, browsecmd=self.select_item)
        self.cl.pack(fill=tkinter.BOTH, side=tkinter.LEFT,
                     padx=5, pady=5, ipady=30, expand=1)
        self.cl.hlist.add(name, text=list_title)
        self.cl.setstatus(name, "off")

    def add_playlist(self, name: str, list_title: str):
        self.cl.hlist.add(name, text=list_title)
        self.cl.setstatus(name, "off")

    def select_item(self, item):
        print(item, self.cl.getstatus(item))

    def make_check_list(self, songs_list: list, name: str):
        if len(songs_list) > 0:
            for obj in songs_list:
                try:
                    self.cl.hlist.add(
                        name + self.seperate_url(obj['song_link']),
                        text=obj['artist'] + ' - ' + obj['title']
                    )
                    self.cl.setstatus(
                        name + self.seperate_url(obj['song_link']), "off")
                    self.cl.config(width=500)
                except:
                    pass

    def seperate_url(self, url: str):
        result = url.split('/')
        return result[len(result)-1]

    def open_file(self):
        filetypes = (('csv files', '*.csv'), ('All files', '*.csv'))
        self.file = askopenfilename(
            title='ouvrir un fichier', filetypes=filetypes)
        self.entry.insert(0, str(self.file))

    def open_file_mp3(self):
        filetypes = (('mp3 files', '*.mp3'), ('All songs files', '*.csv'))
        self.file_mp3 = askopenfilename(
            title='ouvrir un fichier audio', filetypes=filetypes)
        self.entry_song_path.insert(0, str(self.file_mp3))

    def open_song_folder(self):
        path = askdirectory(title='Selectionner un dossier')
        self.entry_song_path.insert(0, str(path))

    def is_mp3(self, file: str):
        return file.endswith('.mp3')

    def playlist_panel(self):
        self.create_checklist(self.frame_playlist, 'CL2',
                              'Listes des playlists')
        self.add_playlist(name='CL2.', list_title='MyPlaylist')

    def rename_audio_file(self):
        path = self.song_path.get()
        if path:
            if os.path.isfile(path):
                path = path.split('/')
                old_path = path[len(path)-1]
                print(old_path)
                sng_path = old_path.split('-')
                sng_path = sng_path[0].upper() + '-' + sng_path[1]
                print(sng_path)
                del path[len(path)-1]
                main_path = "/".join(path)
                try:
                    os.rename(main_path + '/' + old_path,
                              main_path + '/' + sng_path)
                    self.song_rename.insert(
                        "0.0", main_path + '/' + sng_path + '\n')
                    self.entry_song_path.delete(0, END)
                    self.master.update()
                except Exception as error:
                    logger.error(error)
                    showerror('Error', error)
        else:
            showwarning('Warning', 'Veuillez ouvrir un fichier audio')

    async def set_many_songs_metadata(self):
        path = self.song_path.get()
        try:
            if path:
                if path.endswith('.mp3'):
                    await self.set_song_metadata(path)
                else:
                    directory = os.listdir(path)
                    if len(directory) > 0:
                        for file in directory:
                            if file.endswith('.mp3'):
                                await self.set_song_metadata(path + '/'+file)
                                self.song_rename.insert(
                                    "0.0", path + '/'+file + '\n')
                                self.master.update()
                            else:
                                pass
                        showinfo(
                            'info', 'Données du fichier(s) audio(s) modifiées avec succès')
                    else:
                        showerror('Error', 'dossier vide')
                self.entry_song_path.delete(0, END)
            else:
                showwarning(
                    'Attention', 'Veuillez choisir un fichier audio ou un dossier!')
        except Exception as error:
            print(error)
            showerror('Error', error)

    # ajout de la modification de la pochette
    async def set_song_metadata(self, path: str):
        if path:
            audio = music_tag.load_file(path)
            audiofile = eyed3.load(path)
            audio['artist'] = audiofile.tag.artist.upper()
            audio['albumartist'] = audiofile.tag.artist.upper()
            audio['isrc'] = ''
            audio.save()
        else:
            showwarning('Warning', 'Veuillez ouvrir un fichier audio')

    async def read_file(self):
        song_title = []
        path = self.file_path.get()
        if path != '':
            with open(path, mode='r') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    new_row = row[0].split(";")
                    if new_row[1] != 'Listen num':
                        song_title.append(new_row[1])
            for song in song_title:
                sng = await self.read_sng(song)
                self.text.insert("0.0", sng + '\n')
                self.master.update()

            self.create_checklist(self.frame, "CL1", "Listes des songs")
            self.make_check_list(self.search_songs, "CL1.")
            self.cl.autosetmode()
            self.master.update()
            self.entry.delete(0, END)
            showinfo(
                'Success', f'Opération terminée, vous avez téléchargé {len(song_title)} éléments')
        else:
            showwarning('Attention', 'Veuillez choisir un fichier csv!')

    async def read_sng(self, query: str):
        spotify_link, artist_name, song_title = self.spotify_client.search_song(
            query)
        if query is None:
            code = SpotifyCustomerException.ErrorType
            raise SpotifyCustomerException(
                code.NO_CONTENT,
                "Aucune valeur trouve",
                reason='paramètre incorrect'
            )
        else:
            self.search_songs.append({
                'song_link': spotify_link,
                'artist': artist_name,
                'title': song_title
            })
        return spotify_link

    async def mp3_to_wav(self, file: str):
        sound = AudioSegment.from_mp3(file)
        path = file.split('/')
        filename = path[len(path)-1].split('.')[0]
        del path[len(path)-1]
        path = '/'.join(path) + '/'

        try:
            if os.path.isdir(path + 'fichier-wav'):
                sound.export(path + 'fichier-wav' + '/' +
                             filename + '.wav', format='wav')
                print('done in exists')
            else:
                os.mkdir(path + 'fichier-wav')
                sound.export(path + 'fichier-wav' + '/' +
                             filename + '.wav', format='wav')
                print('done in not exist')
        except Exception as error:
            logger.error(error)

    async def convert_mp3_to_wav(self):
        path = self.song_path.get()
        try:
            if path:
                if path.endswith('.mp3'):
                    showwarning(
                        'Warning', 'Veuillez choisir un dossier contenant des fichiers mp3 svp')
                else:
                    directory = os.listdir(path)
                    if len(directory) > 0:
                        for file in directory:
                            is_file_mp3 = self.is_mp3(file)
                            if is_file_mp3:
                                await self.mp3_to_wav(path + '/' + file)
                            else:
                                pass
                        showinfo(
                            'Info', 'Tous les fichiers convertis avec succès')
                    else:
                        showerror('Error', 'Dossier vide')
                self.entry_song_path.delete(0, END)
            else:
                showwarning(
                    'Attention', 'Veuillez choisir un dossier de fichier mp3!')
        except Exception as error:
            logger.error(error)
            showerror('Error', error)

    def create_playlists(self):
        answer = simpledialog.askstring(
            "Titre de la playlist",
            "Entrer le titre de la playlist",
            parent=self.master
        )
        if answer is not None:
            try:
                is_create = self.spotify_client.create_playlists(answer)
                if not is_create:
                    showinfo('Info', 'playlist créee avec succès')
                else:
                    showwarning(
                        'Attention', 'la playlist {} existe déjà'.format(answer))
            except Exception as error:
                logger.error('Error', error)

    def add_track_in_playlist(self, playlist_name: str, tracks: list):
        pass

    def run_song_convert(self):
        asyncio.run(self.convert_mp3_to_wav())

    def generate_link(self):
        asyncio.run(self.read_file())

    def modify_metadata(self):
        asyncio.run(self.set_many_songs_metadata())

    def clear_all(self):
        self.entry.delete(0, END)
        self.text.delete("0.0", END)

    def get_info_entry(self):
        return self.entry.index("0.0")

    def quit(self):
        entry = askyesno(
            title='Exit', message='Are you sure you want to exit?')
        if entry:
            self.master.destroy()

    def about(self):
        showinfo(title='A propos',
                 message='SpotiDown v0.1, copyright @MasterGeek inc.')


# ----------setup application--------------------
if __name__ == "__main__":
    app = tix.Tk()
    gui = ApplicationInterface(app)
    # gui.set_song_metadata(
    #     "C:/Users/MasterGeek/Downloads/Telegram Desktop/Nouveau dossier/son.mp3")
    # gui.set_song_metadata(
    #     "C:/Users/MasterGeek/Downloads/Telegram Desktop/isaac/isaac m. - Nalingaka yo.mp3")
    # print(ApplicationInterface.__doc__)
    # gui.mp3_to_wav(
    #     "C:/Users/MasterGeek/Downloads/Telegram Desktop/Nouveau dossier/eben.mp3")
    # gui.mp3_to_wav(
    #     "C:/Users/MasterGeek/Downloads/Telegram Desktop/Nouveau dossier/son.mp3")
    app.mainloop()
