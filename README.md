# OCR PDF Images
 Many scanners and apps convert images to PDF for easy scanning but those do not allow searching the text within the document. This project will take those PDF scans and convert them into searchable PDFS using `ocrmypdf` 

## Application
The application is built around the Watchdog package in python. This package allows the application to watch a `source` directory for new files and then run function when new files are present. In this case a `source` directory is watched for new PDF files; they are scanned; and then moved to the `destination` directory. There is an option to delete the files once the searchable PDFs appear in the `destination` directory
## Run the Python Application
To run this as a python application, install the required python packages
```
python -m pip install -r requirements.txt
```
Also ensure `ocrmypdf` is installed on the system. 

To run the application
```
python3 ocrmypdf.py <SOURCE DIRECTORY> <DESTINATION DIRECTORY>
```
The `-d` or `--delete` arguments can be added if you want the file deleted after it is moved to the `destination` directory

## Run as a Docker Container
To build the docker image, use the command
```
docker build -t ocr_pdf .
```
To run the docker container from the command line

```
docker run -d --restart=unless-stopped -v "<insert source directory>:/source" -v "<insert destination directory:/destination" --name <insert name here> ocr_pdf
```
