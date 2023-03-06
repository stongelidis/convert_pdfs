import os
import argparse
import logging

from time import sleep
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler


def hold_until_file_is_accessible(file_path):

    while True:
        try:
            file = open(file_path)
            file.close()
            break

        except OSError as e:
            logging.warning(f"{e.strerror}: {e.filename}")
            sleep(5)


def get_unique_filename(file_path):

    destination_path = file_path

    # check if path conflict exists
    if os.path.exists(file_path):
        increment = 1

        base_directory = os.path.dirname(file_path)
        base_filename = os.path.basename(file_path)

        # find extension of file name
        index = base_filename.rfind(".pdf")

        # add a numeric increment to the file name
        updated_file_name = base_filename[:index] + str(increment).zfill(3) + ".pdf"
        updated_destination = os.path.join(base_directory, updated_file_name)

        # keep incrementing until no conflict exists
        while os.path.exists(updated_destination):
            increment += 1
            updated_file_name = base_filename[:index] + str(increment).zfill(3) + ".pdf"
            updated_destination = os.path.join(base_directory, updated_file_name)

            logging.info(
                f"Conflict exists in destination folder. Updating file name to {updated_file_name}"
            )

        # update destination path with new unique filename
        destination_path = updated_destination

    return destination_path


def process_pdfs(list_of_files, destination_directory):

    # for each file (file or directory) scan and save to destination
    for f in list_of_files:

        # get original source file name and force lower case in destination
        dst_filename = os.path.basename(f).lower()

        # form destination path
        destination_path = os.path.join(destination_directory, dst_filename)

        # check if path conflict exists
        destination_path = get_unique_filename(destination_path)

        # check that file is not being used by another process
        logging.info("Checking that file if file is being written")
        hold_until_file_is_accessible(f)

        # command to ocr files
        logging.info(f"Starting OCR on {os.path.basename(f)}")
        cmd = f'ocrmypdf --deskew "{f}" "{destination_path}"'
        os.system(cmd)

        # if delete argument is true, then test file existence in destination directory and delete
        if args.delete:

            if os.path.exists(destination_path):
                logging.info(
                    f"{os.path.basename(f)} found in processing directory {os.path.dirname(destination_path)}"
                )
                logging.warning(f"Deleting original file {os.path.basename(f)}")
                os.remove(f.replace('"', ""))

    logging.info("Waiting for next scan...")


def find_pdf_files(file_path):

    # if event triggered by PDF then only return this specific file
    event_src_is_pdf = file_path.endswith(".pdf")
    if event_src_is_pdf:
        return [file_path]

    # else find all pdfs in source directory
    path_list = []

    src_directory = os.path.dirname(file_path)
    contents = os.listdir(src_directory)

    for file_name in contents:

        full_path = os.path.join(file_path, file_name)

        is_file = os.path.isfile(full_path)
        is_pdf = full_path.endswith(".pdf")

        if is_file and is_pdf:
            logging.info(f"Found file {os.path.basename(full_path)}")
            path_list.append(full_path)

    return path_list


class MonitorFolder(FileSystemEventHandler):
    def __init__(self, destination_directory):
        super(MonitorFolder, self).__init__()
        self.destination_directory = destination_directory

    def on_created(self, event):
        files = find_pdf_files(event.src_path)
        process_pdfs(files, self.destination_directory)


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
    if args.delete:
        logging.info(
            "Delete option detected. Files will be removed from src directory after scanning"
        )

    observer = PollingObserver()
    event_handler = MonitorFolder(args.destination)
    observer.schedule(event_handler, args.source, recursive=False)
    observer.start()

    try:
        while observer.is_alive():
            observer.join(1)

    except KeyboardInterrupt:
        logging.warning("Watchdog service interrupted by keyboard input")

    finally:
        observer.stop()
        observer.join()
        logging.info("Watchdog service terminated")

    logging.warning("***** Service stopped *****")
