FROM python:3.8-slim

WORKDIR /opt/app
COPY . /opt/app

# Install dependencies
RUN pip3 install --no-cache-dir -r /opt/app/requirements.txt

# Run app
CMD [ "python", "./generator.py" ]
