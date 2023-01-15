import openpyxl


class File:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def modify_excel_file(self):
        wb = openpyxl.load_workbook(self.file_path)
        sheet = wb.active
        for row in sheet.iter_rows(min_row=3, max_row=5, min_col=1, max_col=5):
            for cell in row:
                print(cell(row=1, column=2))


if __name__ == "__main__":
    File("D:\output\michier.xlsx").modify_excel_file()
