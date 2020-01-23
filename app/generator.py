import xlrd
import unicodedata
import logging
import time

from app.image_processor import ImageProcessor
from app.settings import *

# passing in headers as they are split over 2 rows in doc
column_headers = "MHS_NUMBER,ALTERNATIVE_NAME,PAPER_NUMBER,ASSOCIATED_ATOLL,ASSOCIATED_ISLAND,PLACE,SCRIPT,LANGUAGE," \
                 "TYPE,DATE,PAGES,HEIGHT,WIDTH,MATERIAL,ASSOCIATED_PERSONS,COMMENTS"


def process_workbook():
    logging.debug("processing workbook..")
    workbook = xlrd.open_workbook(WORKBOOK)
    worksheet = workbook.sheet_by_index(0)

    headers = column_headers.split(",")

    # transform the workbook to a list of dictionary
    data = []
    for row in range(START_ROW, END_ROW):
        image_record = {
            headers[0]: unicodedata.normalize("NFKD", worksheet.cell_value(row, 0)).replace(" ", "")
        }

        for col in range(1, worksheet.ncols):
            value = worksheet.cell_value(row, col)
            image_record[headers[col]] = unicodedata.normalize("NFKD", str(value))

        data.append(image_record)

    return data


def main():
    start = time.time()
    # process the workbook to get data
    data = process_workbook()

    # iterate through dictionary
    image_processor = ImageProcessor()

    logging.debug("generating IIIF resources..")
    image_processor.generate_iiif_resources(data)

    end = time.time()
    print(f"elapsed time {end - start} secs")


if __name__ == '__main__':
    main()
