from abc import ABC
from abc import abstractmethod

import eyed3
from pydub.utils import mediainfo

class ExcelUtils(ABC):
    """ define here  """

    @abstractmethod
    def get_file_metadata(self, dir_path:str) -> dict:
        """
        get a mp3 file metadata
        :param: dir_path as string type
        :return metadata as type dict

        """
        NotImplemented




class ExcelFileHandler(ExcelUtils):

    """
    this class with describe how to fill an excel file
    for beelive
    """
    def __init__(self) -> None:
        pass

    def get_files_metadata(self, dir_path:str) -> None:
        pass

    def get_file_metadata(self, dir_path: str) -> dict:
        media_data = dict()
        if dir_path.endswith('.mp3'):
            media_data = mediainfo(dir_path)
        return media_data


if __name__ == "__main__":
    excel = ExcelFileHandler()
    #excel.get_file_metadata(dir_path="D:/ekilaRadio_nouvelle_version/ekila/spotifyStream/EkilaDownloader/ADAM.mp3")
    excel.get_file_metadata(dir_path="D:/ekilaRadio_nouvelle_version/ekila/spotifyStream/EkilaDownloader/ava.mp3")
