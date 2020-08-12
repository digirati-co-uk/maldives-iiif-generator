# maldives-iiif-generator

Script to ingest images and accompanying metadata to produce IIIF resources

## Technology :rocket:

- Python 3.8
- Docker

### Running Application

The entry point of the application is `generator.py`. This will:

1. Parse metadata from the specified \*.xlsx file and store in a dictionary.
2. Iterate through every row from above dictionary, for each row (where a row represents a manuscript):

- Create a static [image pyramid](https://northstar-www.dartmouth.edu/doc/idl/html_6.2/Image_Tiling.html) and Level 0 [IIIF Image API Service Description](https://iiif.io/api/image/2.0/) per images.
- Create a [IIIF Manifest](https://iiif.io/api/presentation/2.0/) per manuscript, containing manuscript metadata and references to the image service(s).

The easiest way to run the script is via Docker. This will ensure all dependencies are present.

2x volume mounts are required for running the script:

- `/path/to/images/` - this is a local folder containing the manuscript images to be processed. These relate to rows in spreadsheet and must be in format `"{NO}. {MHS_NUMBER}"` (e.g. "1. MLE-ARC-MS3", "2. MLE-ARC-MS4").
- `/path/for/output/` - this is where all generated manifests and image tiles will be output to. The final output will generate `/iamges/api` and `/manifest` folders underneath here.

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

- Columns - the same columns, in the same order, must be present in xlsx file. These can be found in `column_keys.py`. Folder format. Volume mounts
- Images folders - as specified above, the images must be in folders that match names in spreadsheet using `"{NO}. {MHS_NUMBER}"` format. These should all be within the `/path/to/images/` folder. E.g.

```bash
images/
  1. MLE-ARC-MS3/
    MLE-ARC-MS3.jpg
  5. MLE-ARC-MS7/
    MLE-ARC-MS7.1.jpg
    MLE-ARC-MS7.2.jpg
    MLE-ARC-MS7.3.jpg
```

- Image format - some of the larger images are slow to convert (~100s). This is likely due to decompression/recompression from JPEG. To mitigate this, the files can be converted to TIFF prior to processing (e.g. by ImageMagick).
- To avoid unnecessary re-processing of resources on further runs (for example, if the process was stopped halfway through) manuscripts are skipped if a manifest.json file exists for that manuscript. Saving of manifest is the final step in processing so assumption is that if it made it that far then it's generate the image tiles.

#### Settings

`settings.py` contains a list of environment variables that can be used to alter generation process. These all have fallback values if they are not provided. The available options are:

| Name | Description | Fallback |
| --- | --- | --- |
| BASE_URL | The base URL where the IIIF resources will be hosted. Assumes both manifests and images will share same base. | https://maldivesheritage.oxcis.ac.uk/ |
| IMAGE_BASE_SLUG | Appended to `BASE_URL` to make root path to where images hosted. | /images/api |
| IMAGE_FILE_OUTPUT_DIR | Output directory for generated images resources. | ./output/images/api |
| IMAGE_SOURCE_DIR | Directory containing all images. See above for expected format. | ./data/image |
| MANIFEST_BASE_SLUG | Appended to `BASE_URL` to make root path to where manifests hosted. | /manifest |
| MANIFEST_OUTPUT_DIR | Output directory for generated manifest resources. | ./output/manifest |
| WORKBOOK | Location of xlsx workbook containing manuscript data | ./data/image/Maldives.xlsx |
| START_ROW | First row in workbook to start processing (0-based) | 7 |
| END_ROW | Last row in workbook to start processing (0-based) | 95 |
| IMAGE_EXTENSION | Image type to use for generating images | .jpg |
| GENERATE_IMAGES | If True, generates image pyramid. Else only manifests are generated. | True |


## Infrastructure

The `/infrastructure` folder contains [Terraform](https://www.terraform.io/) scripts used to generate the required infrastructure (S3 buckets) to upload generating resources to. _Current TF version at time of writing: Terraform 0.12.0_

After IIIF resources have been generated and tested locally they can be uploaded to S3 via the [`aws cli sync`](https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html) command.

```bash
cd /path/for/output

aws s3 sync . s3://mhs-iiif-output/ --acl public-read
```
