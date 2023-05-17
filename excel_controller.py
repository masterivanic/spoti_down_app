from abc import ABC
from abc import abstractmethod

import openpyxl
from pydub.utils import mediainfo

from metadata import MetaData


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

    @abstractmethod
    def read_xlsx_file(self, file_dir:str) -> None:
        """
        read a xlsx file
        :param: file_dir as string type (file path)
        :return
        """
        NotImplemented




class ExcelFileHandler(ExcelUtils):

    """
    this class with describe how to fill an excel file
    for beelive
    """

    def get_files_metadata(self, dir_path:str) -> None:
        pass

    def get_file_metadata(self, dir_path: str) -> dict:
        media_data:dict = dict()
        if dir_path.endswith('.mp3'):
            media_data = mediainfo(dir_path)
        return media_data

    def wrte_in_xlsx_file(self):
        pass

    def read_xlsx_file(self, file_dir:str) -> None:
        workbook = openpyxl.load_workbook(file_dir)
        worksheet = workbook["Metadatas"]
        idx = 1
        for row in worksheet.iter_rows(min_row = 3, max_row = 3, min_col = 1, max_col = 30):
            for cell in row:
                cell.value = f"value {idx}"
                print(cell.value)
                idx += 1
        try:
            workbook.save(file_dir)
            print("write successfully in file")
        except PermissionError as error:
            raise error

    def get_object_metadata(self, data) -> MetaData:
        return MetaData(data)


if __name__ == "__main__":
    import json
    excel = ExcelFileHandler()
    #excel.get_file_metadata(dir_path="D:/ekilaRadio_nouvelle_version/ekila/spotifyStream/EkilaDownloader/ADAM.mp3")
    #data = excel.get_file_metadata(dir_path="D:/ekilaRadio_nouvelle_version/ekila/spotifyStream/EkilaDownloader/Billie Eilish - Bored.mp3")
    # with open("data.json", "w") as file:
    #     file.write(json.dumps(data))
    #     print(data)
    # obj = excel.get_object_metadata(data=data)
    excel.read_xlsx_file("D:/ekilaRadio_nouvelle_version/ekila/spotifyStream/static/tab.xlsx")
