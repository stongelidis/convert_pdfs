FROM alpine:latest

# Update all packages on OS
RUN apk upgrade -U --available

# Updates the package index and installs python3 in the alpine container
RUN apk --update add python3 ocrmypdf py3-pip

# Create app, source, and destination directories
RUN mkdir -p /app && mkdir -p /app/source && mkdir -p /app/destination

# setup python virtual environment
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Change working dir to /usr/src/app
WORKDIR /app

# Copy source file and requirements to working directory
COPY ocr_pdf.py .
COPY requirements.txt .

# install python requirements
RUN pip install --upgrade pip
RUN python3 -m pip install --use-pep517 -r /app/requirements.txt

# Executes python3 with ocr process
CMD ["python", "ocr_pdf.py", "/app/source", "/app/destination"]