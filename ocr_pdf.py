import os
import argparse
import logging
import time

from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def process_pdfs(list_of_files):

    # for each file (file or directory) scan and save to destination
    for f in list_of_files:

        # get original source file name and force lower case in destination
        dest_filename = os.path.basename(f)
        dest_filename = dest_filename.lower()

        # form destination path
        destination_path = os.path.join(args.destination, dest_filename)

        logging.info(f"Starting OCR on {os.path.basename(f)}")

        # command to ocr files
        cmd = f'ocrmypdf --deskew "{f}" "{destination_path}"'
        os.system(cmd)
        sleep(1)

        # if delete argument is true, then test file existence and delete
        if args.delete:

            if os.path.exists(destination_path):
                logging.info(
                    f"{os.path.basename(f)} found in processing directory {os.path.dirname(destination_path)}"
                )
                logging.warning(f"Deleting original file {os.path.basename(f)}")
                os.remove(f.replace('"', ""))


def find_pfd_files(file_path):

    path_list = []

    contents = os.listdir(file_path)

    for file_name in contents:

        full_path = os.path.join(file_path, file_name)

        is_file = os.path.isfile(full_path)
        is_pdf = full_path.endswith(".pdf")

        if is_file and is_pdf:
            logging.info(f"Found file {os.path.basename(full_path)}")
            path_list.append(full_path)

    return path_list


class MonitorFolder(FileSystemEventHandler):
    def on_created(self, event):
        print(event.src_path, event.event_type)
        files = find_pfd_files(args.source)
        process_pdfs(files)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Scans a PDF using OCR and saves off a copy"
    )
    parser.add_argument("source", help="directory path or file path")
    parser.add_argument("destination", help="destination to save output")
    parser.add_argument(
        "-d", "--delete", action="store_true", help="delete original file after scan"
    )

    # get arguments
    args = parser.parse_args()

    logging.info("Processing arguments")

    if not os.path.isdir(args.source):
        assert False, "Error: source needs to be a directory path"

    if not os.path.isdir(args.destination):
        assert False, "Error: destination needs to be a directory path"

    logging.info(f"Starting Watchdog service on {args.source}")

    observer = Observer()
    event_handler = MonitorFolder()
    observer.schedule(event_handler, args.source, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logging.warning("Watchdog service interrupted by keyboard input")

    finally:
        observer.stop()
        observer.join()
        logging.info("Watchdog service terminated")
