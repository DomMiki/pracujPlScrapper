import xlsxwriter
import scrapper
from sys import exit

#  Documentation: https://xlsxwriter.readthedocs.io/tutorial01.html


def create_excel_file(url, excel_path="Workbook - pracuj.pl.xlsx"):
    try:
        workbook = xlsxwriter.Workbook(excel_path)
        worksheet = workbook.add_worksheet()
        row = 0

        for offer in scrapper.get_offers_as_list(url):
            col = 0
            for data in offer:
                worksheet.write(row, col, data)
                col += 1
            row += 1

        workbook.close()

    except (PermissionError, xlsxwriter.exceptions.FileCreateError):
        exit(f"Can't create excel file. Please close workbook and try again. \n File location: {excel_path}")


if __name__ == "__main__":
    url = "https://it.pracuj.pl/praca/rpa;kw?sal=1"
    create_excel_file(url)

