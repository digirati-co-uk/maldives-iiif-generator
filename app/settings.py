import os

# Base URL for resources
BASE_URL = os.environ.get("BASE_URL", "http://61a60bc3.ngrok.io")

# Location within base URL where IIIF image resources stored
IMAGE_BASE_SLUG = os.environ.get("IMAGE_BASE_SLUG", "/images/api")

# Base URL for IIF image resources
IMAGE_BASE_URL = BASE_URL + IMAGE_BASE_SLUG

# Output dir for generated image pyramid files
IMAGE_FILE_OUTPUT_DIR = os.environ.get("IMAGE_FILE_OUTPUT_DIR", r"c:\temp\maldives\output\images\api")

# Location within base URL where IIIF manifests stored
MANIFEST_BASE_SLUG = os.environ.get("MANIFEST_BASE_SLUG", "/manifest")

# Base URL for manifests
MANIFEST_BASE_URL = BASE_URL + MANIFEST_BASE_SLUG

# Output dir for generated IIIF manifests. This must already exist.
MANIFEST_OUTPUT_DIR = os.environ.get("IMAGE_FILE_OUTPUT_DIR", r"c:\temp\maldives\output\manifest")

# Location of Workbook containing image data
WORKBOOK = os.environ.get("IMAGE_BASE_URL", r"C:\temp\Maldives\Maldives.xlsx")

# First row in workbook to process (0-based)
START_ROW = os.environ.get("IMAGE_BASE_URL", 62)  # 7

# Last row in workbook to process (0-based)
END_ROW = os.environ.get("IMAGE_BASE_URL", 63)  # 95
