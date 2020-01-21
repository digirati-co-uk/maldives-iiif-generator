from iiif_prezi.factory import ManifestFactory
from itertools import groupby


class ImageProcessor:
    def __init__(self):
        fac = ManifestFactory()

        # Where the resources live on the web
        # fac.set_base_prezi_uri("https://maldivesheritage.oxcis.ac.uk/object/")

        # Where the resources live on disk
        fac.set_base_prezi_dir(r"c:\temp\maldives\output")

        fac.set_base_image_uri("https://maldivesheritage.oxcis.ac.uk/image/api/")
        fac.set_iiif_image_info(2.0, 1)  # Version, ComplianceLevel

    def generate_iiif_resources(self, data):
        # iterate through the images. Group them first
        grouped_data = self.get_grouped_data(data)

    def get_grouped_data(self, data):
        groups = []

        # order by MHS_NUMBER, before "."
        # assuming rows are in order post-"." in data
        so = sorted(data, key=lambda item: item["MHS_NUMBER"].split(".")[0])
        for key, group in groupby(so, lambda item: item["MHS_NUMBER"].split(".")[0]):
            groups.append(list(group))

        return groups
