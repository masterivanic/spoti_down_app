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
            self._artist = song_data["TAG"]["artist"]
        except KeyError:
            self._artist = "Unknow artist"
        try:
            self._album = song_data["TAG"]["album"]
        except KeyError:
            self._album = "Unknow artist"
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
    def artist(self):
        return self._artist

    @property
    def album(self):
        return self._album

    @property
    def album_artist(self):
        return self._album_artist

    @property
    def publisher(self):
        return self._publisher

    @property
    def date(self):
        return self._date
