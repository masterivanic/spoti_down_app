
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilenames
from spotify import SpotifyCustomer
from tkinter.messagebox import showwarning
from tkinter.messagebox import showinfo
from exceptions import SongError
from exceptions import ComponentError
from utils import Utils

import csv
import tkinter
import customtkinter
import asyncio


class Controller:

    def __init__(self, view, sp_client:SpotifyCustomer) -> None:
        self.view = view
        self.sp_client = sp_client
        self.state = {
            'search_songs': []
        }
        self.search_songs = []
    
    def create_playlist(self):
        """ permit a user to create a playlist"""

        pass

    def open_file(self):
        """ get csv file path """

        filetypes = (('csv files', '*.csv'), ('All files', '*.csv'))
        file_path = askopenfilename(
            title='ouvrir un fichier', 
            filetypes=filetypes
        )
        return file_path
        
    
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


    async def song_panel(self):
        """ print all song extract from csv in transfert song panel """

        try:
            self.check_var = tkinter.StringVar()
            self.header = customtkinter.CTkCheckBox(
                self.view.scrollable_sons_frame, 
                text="Headers",
                variable=self.check_var,
                command=self.select_checkboxes,
                onvalue="on", 
                offvalue="off"
            )
            self.header.grid(row=0, column=0, pady=(0, 10), sticky='nw')

            self.scrollable_frame_switches = []
            self.checkbox_value = tkinter.StringVar()

            for i, songs in enumerate(self.search_songs):
                await self.checkbox_song_output(songs, i)
                print('execute this action.')
                self.view.update()
        
        except Exception as err:
            print(err)

    async def checkbox_song_output(self, songs, index):
        try:
            checkbox = customtkinter.CTkCheckBox(
                self.view.scrollable_sons_frame, 
                text=songs['artist'] + '- ' + songs['title'],
                variable=self.checkbox_value,
                onvalue=songs['song_link'],
                offvalue='off', 
            )
            checkbox.grid(row=index+1, column=0, pady=(0, 10), sticky='nw', padx=30)
            self.scrollable_frame_switches.append(checkbox)
        except Exception as error:
            raise error

    async def select_and_deselect(self):
        self.current_header_state = self.check_var.get()
        if self.current_header_state == "on":
            for checkbox in self.scrollable_frame_switches:
                await Utils.select_checkbox()
                self.view.update()
        elif self.current_header_state == "off":
            for checkbox in self.scrollable_frame_switches:
                await Utils.deselect_checkbox(checkbox)
                self.view.update()
    
    def select_checkboxes(self):
        asyncio.run(self.select_and_deselect())

    def checkbox_playlist_output(self):
        """ print all user's playlist in transfert song panel """

        all_playlist = self.sp_client.get_user_plalists() # store this in cache
        self.playlist_var = tkinter.StringVar()
        self.scrollable_playlist_switches = []
        for i, playlist in enumerate(all_playlist):
            checkbox =  customtkinter.CTkCheckBox(
                self.view.scrollable_sons_list, 
                text=playlist['name'],
                onvalue=playlist['id'],
                offvalue='off',
                variable=self.playlist_var,
                command=self.selected_playlist
            )
            checkbox.grid(row=i, column=0, pady=(0, 10), sticky='nw', padx=30)
            self.scrollable_playlist_switches.append(checkbox)


    def selected_playlist(self):
        print("selectd playlist:: ", self.playlist_var.get())
        

 

    

    



        
    
 
