import re

from typing import Sequence

from .settings import *
from .column_keys import ColumnKeys, ManuscriptRow


class ImageReader:
    """Provides functionality to read all images associated with manuscript."""
    _image_extension = IMAGE_EXTENSION

    def __init__(self, base_dir: str):
        """Inits ImageReader using specified base directory.

        :param base_dir:root directory containing manuscript images.
        """
        self._base_dir = base_dir

    def get_files_for_manuscript(self, manuscript: ManuscriptRow) -> Sequence[str]:
        """Get a list of all image locations for specified manuscript.

        :param manuscript:dictionary object containing
        :return:a sequence containing path of all matching images.
        """
        folder = self._get_folder_key(manuscript)

        image_files = []
        for root, dirs, files in os.walk(f"{self._base_dir}/{folder}"):
            files.sort(key=self._natural_keys)
            for file in files:
                if file.endswith(self._image_extension):
                    abs_path = os.path.abspath(os.path.join(root, file))
                    image_files.append(abs_path)

        print(f"Got {len(image_files)} images in {folder}")
        return image_files

    @staticmethod
    def _get_folder_key(manuscript: ManuscriptRow) -> str:
        return f"{manuscript.get(ColumnKeys.NO)}. {manuscript.get(ColumnKeys.MHS_NUMBER)}"

    @staticmethod
    def _natural_keys(text):
        # see: https://stackoverflow.com/a/5967539/83096
        return [ImageReader._atoi(c) for c in re.split(r'(\d+)', text)]

    @staticmethod
    def _atoi(text):
        return int(text) if text.isdigit() else text
