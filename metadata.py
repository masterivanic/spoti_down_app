class MetaData:
    """ define song metadata models """

    def __init__(self, song_data:dict) -> None:
        self.song_data = song_data

        try:
            self._title = song_data["TAG"]["title"]
        except KeyError:
            self._title = "Unknow title"
        try:
            self._num_track = song_data["TAG"]["track"]
        except KeyError:
            self._num_track = "0"
        try:
            self._disc = song_data["TAG"]["disc"]
        except KeyError:
            self._disc = "0"
        try:
            self._genre = song_data["TAG"]["genre"]
        except KeyError:
            self._genre = "Unknow genre"
        try:
            self._artist = song_data["TAG"]["artist"]
        except KeyError:
            self._artist = "Unknow artist"
        try:
            self._album = song_data["TAG"]["album"]
        except KeyError:
            self._album = "Unknow artist"
        try:
            self._tsrc = song_data["TAG"]["TSRC"]
        except KeyError:
            self._tsrc = "Unknow isrc"
        try:
            self._album_artist = song_data["TAG"]["album_artist"]
        except KeyError:
            self._album_artist = "Unknow album artist"
        try:
            self._publisher = song_data["TAG"]["publisher"]
        except KeyError:
            self._publisher = "Unknow publisher"
        try:
            self._date = song_data["TAG"]["date"]
        except KeyError:
            self._date = "Unknow publisher"

    @property
    def title(self):
        return self._title

    @property
    def num_track(self):
        return self._num_track

    @property
    def disc(self):
        return self._disc

    @property
    def genre(self):
        return self._genre

    @property
    def artist(self):
        return self._artist

    @property
    def album(self):
        return self._album

    @property
    def isrc(self):
        return self._tsrc

    @property
    def album_artist(self):
        return self._album_artist

    @property
    def publisher(self):
        return self._publisher

    @property
    def date(self):
        return self._date


    def __repr__(self) -> str:
        return f"title: {self.title}\n num track:{self.num_track} \n disc:{self.disc} \n\
            artist:{self.artist}\n album:{self.album} \n album artist:{self.album_artist}"

    def __str__(self) -> str:
        return f"{self.title}"
