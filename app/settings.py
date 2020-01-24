import os

# Base URL for resources
BASE_URL = os.environ.get("BASE_URL", "http://0080ab99.ngrok.io")

# Location within base URL where IIIF image resources stored
IMAGE_BASE_SLUG = os.environ.get("IMAGE_BASE_SLUG", "/images/api")

# Base URL for IIF image resources
IMAGE_BASE_URL = BASE_URL + IMAGE_BASE_SLUG

# Output dir for generated image pyramid files
IMAGE_FILE_OUTPUT_DIR = os.environ.get("IMAGE_FILE_OUTPUT_DIR", r"c:\temp\maldives\output\images\api")

# Folder containing subfolder per manuscript
IMAGE_SOURCE_DIR = os.environ.get("IMAGE_SOURCE_DIR", r"c:\clients\maldives\mhs_digitized_mss")

# Location within base URL where IIIF manifests stored
MANIFEST_BASE_SLUG = os.environ.get("MANIFEST_BASE_SLUG", "/manifest")

# Base URL for manifests
MANIFEST_BASE_URL = BASE_URL + MANIFEST_BASE_SLUG

# Output dir for generated IIIF manifests. This must already exist.
MANIFEST_OUTPUT_DIR = os.environ.get("IMAGE_FILE_OUTPUT_DIR", r"c:\temp\maldives\output\manifest")

# Location of Workbook containing image data
WORKBOOK = os.environ.get("IMAGE_BASE_URL", r"C:\Clients\Maldives\MHS_Digitized_MSS\Maldives MSS IIIF - Batch for Digirati (Revised 23012020).xlsx")

# First row in workbook to process (0-based)
START_ROW = os.environ.get("START_ROW", 7)

# Last row in workbook to process (0-based)
END_ROW = os.environ.get("END_ROW", 95)
