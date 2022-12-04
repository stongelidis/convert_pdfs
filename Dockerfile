FROM alpine:latest

# Update all packages on OS
RUN apk upgrade -U --available

# Updates the package index and installs python3 in the alpine container
RUN apk --update add python3 ocrmypdf py3-pip

# Create app directory
RUN mkdir -p /app

# Create source directory
RUN mkdir -p /source

# Create destination directory
RUN mkdir -p /destination

# Change working dir to /usr/src/app
WORKDIR /app

# Copy source files to working directory
COPY . .

# install python requirements
RUN python3 -m pip install -r /app/requirements.txt

# Executes python3 with /opt/hello-docker.py as the only parameter
CMD ["python3", "/app/ocr_pdf.py", "/source", "/destination"]