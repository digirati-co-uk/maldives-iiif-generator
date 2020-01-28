from typing import Dict

# Type alias for manuscript row
ManuscriptRow = Dict


class ColumnKeys:
    """Contains a list of all column names from manuscript spreadsheet."""
    NO = "NO"
    MHS_NUMBER = "MHS NUMBER"
    ALTERNATIVE_NAME = "ALTERNATIVE NAME"
    PAPER_NUMBER = "PAPER NUMBER"
    ASSOCIATED_ATOLL = "ASSOCIATED ATOLL"
    ASSOCIATED_ISLAND = "ASSOCIATED ISLAND"
    PLACE = "PLACE"
    SCRIPT = "SCRIPT"
    LANGUAGE = "LANGUAGE"
    TYPE = "TYPE"
    DATE = "DATE"
    PAGES = "PAGES"
    HEIGHT = "HEIGHT"
    WIDTH = "WIDTH"
    MATERIAL = "MATERIAL"
    ASSOCIATED_PERSONS = "ASSOCIATED PERSONS"
    COMMENTS = "COMMENTS"

    @staticmethod
    def csv_list() -> str:
        """Get manuscript column names as a CSV list.

        :return:csv list of column names
        """
        return f"{ColumnKeys.NO},{ColumnKeys.MHS_NUMBER},{ColumnKeys.ALTERNATIVE_NAME},{ColumnKeys.PAPER_NUMBER},{ColumnKeys.ASSOCIATED_ATOLL},{ColumnKeys.ASSOCIATED_ISLAND},{ColumnKeys.PLACE},{ColumnKeys.SCRIPT},{ColumnKeys.LANGUAGE},{ColumnKeys.TYPE},{ColumnKeys.DATE},{ColumnKeys.PAGES},{ColumnKeys.HEIGHT},{ColumnKeys.WIDTH},{ColumnKeys.MATERIAL},{ColumnKeys.ASSOCIATED_PERSONS},{ColumnKeys.COMMENTS}"