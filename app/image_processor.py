from iiif_prezi.factory import ManifestFactory
from itertools import groupby


class ImageProcessor:
    def __init__(self):
        self.fac = ManifestFactory()

        # Where the resources live on the web
        self.fac.set_base_prezi_uri("https://maldivesheritage.oxcis.ac.uk/object/")

        # Where the resources live on disk
        self.fac.set_base_prezi_dir(r"c:\temp\maldives\output")

        self.fac.set_base_image_uri("https://maldivesheritage.oxcis.ac.uk/image/api/")
        self.fac.set_iiif_image_info(2.0, 1)  # Version, ComplianceLevel

    def generate_iiif_resources(self, data):
        # iterate through the images. Group them first
        grouped_data = self.get_grouped_data(data)

        for image_group in grouped_data:
            self.process_group(image_group)

    def get_grouped_data(self, data):
        groups = []

        # order by MHS_NUMBER, before "."
        # assuming rows are in order post-"." in data
        so = sorted(data, key=lambda item: self.get_mhs_number_root(item))
        for key, group in groupby(so, lambda item: self.get_mhs_number_root(item)):
            groups.append(list(group))

        return groups

    def get_mhs_number_root(self, item):
        return item["MHS_NUMBER"].split(".")[0]

    def process_group(self, image_group):
        manifest = self.create_manifest(image_group[0])

        self.add_canvases(image_group, manifest)

        manifest.toFile(compact=False)

    def create_manifest(self, image):
        mhs_number = self.get_mhs_number_root(image)
        manifest = self.fac.manifest(label="Manifest for " + mhs_number, ident=mhs_number)

        # add all the metadata fields manifest
        manifest.set_metadata(image)
        manifest.description = "This is a description for " + mhs_number

        return manifest

    def add_canvases(self, images, manifest):
        seq = manifest.sequence()

        for p in range(len(images)):
            # Create a canvas with uri slug of page-1, and label of Page 1
            cvs = seq.canvas(ident="page-%s" % p, label="Page %s" % p)

            # Create an annotation on the Canvas
            anno = cvs.annotation()

            # Add Image: http://www.example.org/path/to/image/api/p1/full/full/0/native.jpg
            img = anno.image("p%s" % p, iiif=True)

            # Set image height and width, and canvas to same dimensions
            # imagefile = "/path/to/images/p%s.jpg" % p
            # img.set_hw_from_file(imagefile)
            cvs.height = 10 # img.height
            cvs.width = 20 # img.width
