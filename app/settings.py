import os

from urllib.parse import urljoin

# Base URL for resources
BASE_URL = os.environ.get("BASE_URL", "https://maldivesheritage.oxcis.ac.uk/")

# Location within base URL where IIIF image resources stored
IMAGE_BASE_SLUG = os.environ.get("IMAGE_BASE_SLUG", "/images/api")

# Base URL for IIF image resources
IMAGE_BASE_URL = urljoin(BASE_URL, IMAGE_BASE_SLUG)

# Output dir for generated image pyramid files
IMAGE_FILE_OUTPUT_DIR = os.environ.get("IMAGE_FILE_OUTPUT_DIR", r"./output/images/api")

# Folder containing subfolder per manuscript
IMAGE_SOURCE_DIR = os.environ.get("IMAGE_SOURCE_DIR", r"./data/image")

# Location within base URL where IIIF manifests stored
MANIFEST_BASE_SLUG = os.environ.get("MANIFEST_BASE_SLUG", "/manifest")

# Base URL for manifests
MANIFEST_BASE_URL = urljoin(BASE_URL, MANIFEST_BASE_SLUG)

# Output dir for generated IIIF manifests. This must already exist.
MANIFEST_OUTPUT_DIR = os.environ.get("MANIFEST_OUTPUT_DIR", r"./output/manifest")

# Location of Workbook containing image data
WORKBOOK = os.environ.get("WORKBOOK", "./data/image/Maldives.xlsx")

# First row in workbook to process (0-based)
START_ROW = int(os.environ.get("START_ROW", 7))

# Last row in workbook to process (0-based)
END_ROW = int(os.environ.get("END_ROW", 95))

# The image type used for generating image pyramids
IMAGE_EXTENSION = os.environ.get("IMAGE_EXTENSION", ".jpg")
