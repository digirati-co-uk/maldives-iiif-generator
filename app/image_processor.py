from iiif_prezi.factory import ManifestFactory
from itertools import groupby
from iiif.static import IIIFStatic
import logging


class ImageProcessor:
    def __init__(self):
        self._manifest_factory = ManifestFactory()
        self._tile_generator = IIIFStatic(dst=r"c:\temp\maldives\output")

        # Where the resources live on the web
        self._manifest_factory.set_base_prezi_uri("https://maldivesheritage.oxcis.ac.uk/object/")

        # Where the resources live on disk
        self._manifest_factory.set_base_prezi_dir(r"c:\temp\maldives\output")

        self._manifest_factory.set_base_image_uri("https://maldivesheritage.oxcis.ac.uk/image/api/")
        self._manifest_factory.set_iiif_image_info(2.0, 1)  # Version, ComplianceLevel

    def generate_iiif_resources(self, data):
        # iterate through the images. Group them first
        grouped_data = self._get_grouped_data(data)

        for image_group in grouped_data:
            self._process_group(image_group)

    def _get_grouped_data(self, data):
        groups = []

        # order by MHS_NUMBER, before "."
        # assuming rows are in order post-"." in data
        so = sorted(data, key=lambda item: self._get_mhs_number_root(item))
        for key, group in groupby(so, lambda item: self._get_mhs_number_root(item)):
            groups.append(list(group))

        return groups

    def _get_mhs_number_root(self, item):
        return item["MHS_NUMBER"].split(".")[0]

    def _process_group(self, image_group):
        manifest = self._create_manifest(image_group[0])

        self._add_canvases(image_group, manifest)

        manifest.toFile(compact=False)

    def _create_manifest(self, image):
        mhs_number = self._get_mhs_number_root(image)
        logging.debug("creating manifest for %s" % mhs_number)
        manifest = self._manifest_factory.manifest(label="Manifest for %s" % mhs_number, ident=mhs_number)

        # add all the metadata fields manifest
        manifest.set_metadata({k: v for k, v in image.items() if v})
        manifest.description = image["ALTERNATIVE_NAME"]

        return manifest

    def _add_canvases(self, images, manifest):
        image_count = len(images)

        logging.debug("creating %d canvases" % image_count)

        seq = manifest.sequence()

        for p in range(image_count):
            # Create a canvas with uri slug of page-1, and label of Page 1
            image_id = images[p]["MHS_NUMBER"]
            cvs = seq.canvas(ident=image_id, label="Page %s" % p)

            # Create an annotation on the Canvas
            annotation = cvs.annotation(ident="page-%s" % p)

            # Add Image: http://www.example.org/path/to/image/api/p1/full/full/0/native.jpg
            img = annotation.image("p%s" % p, iiif=True)

            # Set image height and width, and canvas to same dimensions
            # TODO - read correct images
            image_file = r"C:\temp\Maldives\imgs\HAF-IVD-1-MS1.1-P5.JPG" if p % 2 == 0 else r"C:\temp\Maldives\imgs\MHS-MS-1206-P41.jpg"
            self._tile_generator.generate(image_file, image_id)
            img.set_hw_from_file(image_file)
            cvs.height = img.height
            cvs.width = img.width
