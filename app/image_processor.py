import time

from pathlib import Path
from iiif_prezi.factory import ManifestFactory
from iiif.static import IIIFStatic

from .column_keys import ColumnKeys
from .image_reader import ImageReader
from .settings import *


class ImageProcessor:

    def __init__(self):
        self._manifest_factory = ManifestFactory()
        self._tile_generator = IIIFStatic(dst=IMAGE_FILE_OUTPUT_DIR, prefix=IMAGE_BASE_URL)

        # Where the resources live on the web
        self._manifest_factory.set_base_prezi_uri(MANIFEST_BASE_URL)

        # Where the resources live on disk
        if not os.path.exists(MANIFEST_OUTPUT_DIR):
            os.makedirs(MANIFEST_OUTPUT_DIR)
        self._manifest_factory.set_base_prezi_dir(MANIFEST_OUTPUT_DIR)

        self._manifest_factory.set_base_image_uri(IMAGE_BASE_URL)
        self._manifest_factory.set_iiif_image_info(2.0, 1)  # Version, ComplianceLevel

        self._image_reader = ImageReader(IMAGE_SOURCE_DIR)

    def generate_iiif_resources(self, manuscript_data):
        for manuscript in manuscript_data:
            self._process_manuscript(manuscript)

    def _process_manuscript(self, manuscript):
        mhs_number = manuscript.get(ColumnKeys.MHS_NUMBER)

        if Path(f"{MANIFEST_OUTPUT_DIR}/{mhs_number}.json").is_file():
            print(f"{manuscript} already processed. Skipping")
            return

        manifest = self._create_manifest(manuscript)

        self._add_canvases(manuscript, manifest)

        manifest.toFile(compact=False)

    def _create_manifest(self, manuscript):
        mhs_number = manuscript.get(ColumnKeys.MHS_NUMBER)
        alternative_name = manuscript.get(ColumnKeys.ALTERNATIVE_NAME)

        print(f"creating manifest for {mhs_number}")
        manifest = self._manifest_factory.manifest(label=f"{mhs_number} - {alternative_name}", ident=mhs_number)

        # add all non-empty fields as metadata (excluding "No" field as this is just internal
        manifest.set_metadata({k: v for (k, v) in manuscript.items() if v and k != ColumnKeys.NO})
        manifest.description = alternative_name
        return manifest

    def _add_canvases(self, manuscript, manifest):
        manuscript_images = self._image_reader.get_files_for_manuscript(manuscript)
        mhs_number = manuscript.get(ColumnKeys.MHS_NUMBER)

        image_count = len(manuscript_images)

        print(f"creating {image_count} canvases for {mhs_number}..")

        seq = manifest.sequence()

        for p in range(image_count):
            image_id = f"{mhs_number}-{p}"
            start = time.time()
            print(f"processing {image_id}..")
            cvs = seq.canvas(ident=image_id, label=f"Page {p}")

            # Create an annotation on the Canvas
            annotation = cvs.annotation(ident=f"page-{p}")

            # set source of image data
            img = annotation.image(image_id, iiif=True)

            # Set image height and width, and canvas to same dimensions
            image_file = manuscript_images[p]
            self._generate_image_pyramid(image_file, image_id)
            img.set_hw_from_file(image_file)
            cvs.height = img.height
            cvs.width = img.width

            end = time.time()
            print(f"processed {image_id} in {end - start} secs")

    def _generate_image_pyramid(self, image_file, image_id):
        self._tile_generator.generate(src=image_file, identifier=image_id)

        # generate a 90-wide thumb for UV (see: https://github.com/UniversalViewer/universalviewer/issues/102)
        self._tile_generator.generate_tile("full", [90, None])
