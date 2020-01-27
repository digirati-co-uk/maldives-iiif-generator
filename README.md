# maldives-iiif-generator

Script to ingest images and accompanying metadata to produce IIIF resources

## Technology :rocket:

* Python 3.8
* Docker

### Running Application

The entry point of the application is `generator.py`. This will:

1. Parse metadata from the specified *.xlsx file and store in a dictionary.
2. Iterate through every row from above dictionary, for each row (where a row represents a manuscript):
  * Create a static [image pyramid](https://northstar-www.dartmouth.edu/doc/idl/html_6.2/Image_Tiling.html) and Level 0 [IIIF Image API Service Description](https://iiif.io/api/image/2.0/) per images.
  * Create a [IIIF Manifest](https://iiif.io/api/presentation/2.0/) per manuscript, containing manuscript metadata and references to the image service(s).

The easiest way to run the script is via Docker. This will ensure all dependencies are present. 

2x volume mounts are required for running the script:
* `/path/to/images/` - this is a local folder containing the manuscript images to be processed. These relate to rows in spreadsheet and must be in format `"{NO}. {MHS_NUMBER}"` (e.g. "1. MLE-ARC-MS3", "2. MLE-ARC-MS4").
* `/path/for/output` - this is where all generated manifests and image tiles will be output to. The final output will generate `/iamges/api` and `/manifest` folders underneath here.

To run via Docker:

```bash
cd /maldives-iiif-generator

# 1. build the docker image
docker build --tag=maldives .

# 2. run the docker image, specifying 2 volumes
docker run \
  -v /path/to/images/:/opt/app/data/image \
  -v /path/for/output:/opt/app/output \
maldives

# 3. (optional) env vars can be used to customise run via docker -e flag
#    see app/settings.py for full list of env vars and defaults
docker run \
  -v /path/to/images/:/opt/app/data/image \
  -v /path/for/output:/opt/app/output \
  -e IMAGE_EXTENSION=.tiff # use .tiff images (default: .jpg)
maldives
```

#### Assumptions/Notes

This script has been run using provided resources. The following states assumptions made for future runs and other implementation notes.

* Columns - the same columns, in the same order, must be present in xlsx file. These can be found in `column_keys.py`. Folder format. Volume mounts
* Images folders - as specified above, the images must be in folders that match names in spreadsheet using `"{NO}. {MHS_NUMBER}"` format. These should all be within the `/path/to/images/` folder. E.g.
```bash
images/
  1. MLE-ARC-MS3/
    MLE-ARC-MS3.jpg
  5. MLE-ARC-MS7/
    MLE-ARC-MS7.1.jpg
    MLE-ARC-MS7.2.jpg
    MLE-ARC-MS7.3.jpg
```
* Image format - some of the larger images are slow to convert (~100s). This is likely due to decompression/recompression from JPEG. To mitigate this, the files can be converted to TIFF prior to processing (e.g. by ImageMagick).
* To avoid unnecessary re-processing of images on further runs (for example, if the process was stopped halfway through) manuscripts are skipped if a manifest.json file exists for that manuscript. Saving of manifest is the final step in processing so assumption is that if it made it that far then it's generate the image tiles.

## Infrastructure

The `/infrastructure` folder contains [Terraform](https://www.terraform.io/) scripts used to generate the required infrastructure (e.g. S3 buckets) to upload generating resources to. _Current TF version at time of writing: Terraform 0.12.0_

 