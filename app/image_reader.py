import logging
import os

from app.column_keys import ColumnKeys


class ImageReader:
    def __init__(self, base_dir):
        self._base_dir = base_dir

    def get_files_for_manuscript(self, manuscript):
        folder = self._get_folder_key(manuscript)

        image_files = []
        for root, dirs, files in os.walk(f"{self._base_dir}/{folder}"):
            for file in files:
                if file.endswith(".jpg"):
                    abs_path = os.path.abspath(os.path.join(root, file))
                    image_files.append(abs_path)

        logging.debug(f"Got {len(image_files)} images in {folder}")
        return image_files

    @staticmethod
    def _get_folder_key(manuscript):
        return f"{manuscript.get(ColumnKeys.NO)}. {manuscript.get(ColumnKeys.MHS_NUMBER)}"
