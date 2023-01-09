FROM python:3.11.1-slim-bullseye

# update packages and install necessary applications
RUN apt-get update \
 && apt-get install -y ocrmypdf python3-venv

# Create app, source, and destination directories
RUN mkdir -p /app && mkdir -p /app/source && mkdir -p /app/destination

# setup python virtual environment
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Change working dir to /usr/src/app
WORKDIR /app

# update python pip and install requirements
COPY requirements.txt .
RUN pip install --upgrade pip && python3 -m pip install --use-pep517 -r /app/requirements.txt

# Copy source file and requirements to working directory
COPY ocr_pdf.py .

# Executes python3 with ocr process
CMD ["python", "ocr_pdf.py", "/app/source", "/app/destination", "--delete"]