import xlrd
import unicodedata
import logging
import time

from app.column_keys import ColumnKeys
from app.image_processor import ImageProcessor
from app.settings import *


def process_workbook():
    logging.debug("processing workbook..")
    workbook = xlrd.open_workbook(WORKBOOK)
    worksheet = workbook.sheet_by_index(0)

    headers = ColumnKeys.csv_list().split(",")

    # transform the workbook to a list of dictionary
    data = []
    for row in range(START_ROW, END_ROW):
        image_record = {}

        for col in range(len(headers)):
            value = worksheet.cell_value(row, col)
            col_name = headers[col]

            if col_name == ColumnKeys.NO:
                value = int(value)
            elif col_name == ColumnKeys.MHS_NUMBER:
                value = value.replace(" ", "")

            image_record[col_name] = unicodedata.normalize("NFKD", str(value))

        data.append(image_record)

    return data


def main():
    start = time.time()
    data = process_workbook()

    logging.debug("generating IIIF resources..")
    image_processor = ImageProcessor()
    image_processor.generate_iiif_resources(data)

    end = time.time()
    print(f"elapsed time {end - start} secs")


if __name__ == '__main__':
    main()
