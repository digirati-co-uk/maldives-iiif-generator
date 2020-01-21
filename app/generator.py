import xlrd
import unicodedata
from iiif_prezi.factory import ManifestFactory

# take these as vars
start_row = 7
end_row = 95  # or process until end?

# passing in headers as they are split over 2 rows in doc
column_headers = "MHS_NUMBER,ALTERNATIVE_NAME,PAPER_NUMBER,ASSOCIATED_ATOLL,ASSOCIATED_ISLAND,PLACE,SCRIPT,LANGUAGE," \
                 "TYPE,DATE,PAGES,HEIGHT,WIDTH,MATERIAL,ASSOCIATED_PERSONS,COMMENTS"


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


def process_images(data):
    # TODO group images by id
    fac = ManifestFactory()

    # Where the resources live on the web
    # fac.set_base_prezi_uri("https://maldivesheritage.oxcis.ac.uk/object/")

    # Where the resources live on disk
    fac.set_base_prezi_dir(r"c:\temp\maldives\output")

    fac.set_base_image_uri("https://maldivesheritage.oxcis.ac.uk/image/api/")
    fac.set_iiif_image_info(2.1, 1)  # Version, ComplianceLevel


def main():
    # process the workbook to get data
    data = process_workbook()

    # iterate through dictionary
    # get image file for current entry
    # build service description + manifest


if __name__ == '__main__':
    main()
