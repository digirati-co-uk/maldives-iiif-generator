import xlrd
import unicodedata

# take these as vars - or process until end?
start_row = 7
end_row = 95
column_headers = "MHS_NUMBER,ALTERNATIVE_NAME,PAPER_NUMBER,ASSOCIATED_ATOLL,ASSOCIATED_ISLAND,PLACE,SCRIPT,LANGUAGE," \
                 "TYPE,DATE,PAGES,HEIGHT,WIDTH,MATERIAL,ASSOCIATED_PERSONS,COMMENTS "


def process_workbook():
    workbook = xlrd.open_workbook(r"C:\temp\Maldives\Maldives.xlsx")
    worksheet = workbook.sheet_by_index(0)

    first_row = column_headers.split(",")

    # transform the workbook to a list of dictionary
    data = []
    for row in range(start_row, end_row):
        image_record = {}
        for col in range(worksheet.ncols):
            value = worksheet.cell_value(row, col)
            if isinstance(value, str):
                image_record[first_row[col]] = unicodedata.normalize("NFKD", value)
            else:
                image_record[first_row[col]] = value
        data.append(image_record)

    return data


def main():
    process_workbook()


if __name__ == '__main__':
    main()
