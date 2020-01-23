FROM python:3.8.1-alpine3.11

RUN apk add --update --no-cache --virtual=run-deps \
  build-base \
  libxml2-dev \
  libxslt-dev \
  jpeg-dev \
  && rm -rf /var/cache/apk/*

WORKDIR /opt/app
COPY . /opt/app

# Run script to set environment variables
RUN ./env.sh

# Install dependencies
RUN pip3 install --no-cache-dir -r /opt/app/requirements.txt

# Run app
CMD [ "python", "./test.py" ]

