
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilenames
from spotify import SpotifyCustomer
from tkinter.messagebox import showwarning
from tkinter.messagebox import showinfo
from utils import copy_csv_to_another
from exceptions import SongError
from exceptions import ComponentError

import csv
import tkinter
import customtkinter


class Controller:

    def __init__(self, view, sp_client:SpotifyCustomer) -> None:
        self.view = view
        self.sp_client = sp_client
        self.search_songs = []
       
    def open_file(self):
        """ get csv file path """

        filetypes = (('csv files', '*.csv'), ('All files', '*.csv'))
        file_path = askopenfilename(
            title='ouvrir un fichier', 
            filetypes=filetypes
        )
        return file_path
        
    def is_mp3(self, file: str):
        return file.endswith('.mp3')

    def open_file_mp3(self):
        """ get mp3 file path """

        filetypes = (('mp3 files', '*.mp3'), ('All songs files', '*.mp3'))
        file_mp3_path = askopenfilename(
            title='ouvrir un fichier audio', 
            filetypes=filetypes
        )
        return file_mp3_path

    async def read_sng(self, query: str):
        """search a song on spotify and return song link """

        spotify_link, artist_name, song_title = self.sp_client.search_song(query)
        if query is None or spotify_link is None:
            pass
        else:
            self.search_songs.append({
                'song_link': spotify_link,
                'artist': artist_name,
                'title': song_title
            })
        return spotify_link
    
    async def read_unique_file(self, file_path):
        """read song on csv file and print response on screen """

        song_title, count = [], 0
        self.search_songs = []
        progress = 0
        if file_path:
            with open(file_path, mode='r', encoding="utf8", errors='ignore') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    new_row = row[0].split(";")
                    if new_row[1] != 'Listen num':
                        song_title.append(new_row[1])

            self.view.progressbar.configure(determinate_speed=1)
            for song in song_title:
                try:
                    await self.read_sng(song)
                    if self.view.textbox_csv:
                        self.view.textbox_csv.insert(tkinter.INSERT, '\t' + str(count) + '. ' + song + '\n')
                        self.view.update()
                        self.view.progressbar.start()
                        progress = 1 / len(song_title) + progress
                        self.view.progressbar.set(progress)
                        count += 1
                except Exception:
                    raise SongError
            self.view.progressbar.stop()
            showinfo('Success', f'Opération terminée')
            self.initialise_entry()
        else:
            showwarning('message', 'Veuillez choisir un fichier!')

    def initialise_entry(self):
        """ initialise csv entries """

        try:
            self.view.file_path.set('')
            self.view.csv_entry.delete(0, tkinter.END)
            self.view.textbox_csv.delete("0.0", "end")
            self.view.progressbar.set(0)
        except:
            raise ComponentError

    def song_panel(self, song_list=None):
        """ print all song extract from csv in transfert song panel """

        try:
            row = 2
            pad = 85    
            for _ in range(0, 10):
                customtkinter.CTkCheckBox(self.view.scrollable_sons_frame, text="son1").grid(row=row, column=1, sticky='nw', pady=pad, padx=25)
                row +=1 
                pad += 10
                #print(self.checkbox_1)
        except:
            raise ComponentError
    
     
    def make_copy_file(self, files: list):
        dest_file = files[0]
        for i in range(1, len(files)):
            copy_csv_to_another(source_file=files[i], dest_file=dest_file)
        return dest_file
        
            