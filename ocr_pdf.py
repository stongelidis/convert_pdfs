import os
from time import sleep
import argparse

def find_pfd_files(file_path):

    path_list = []

    contents = os.listdir(file_path)

    for file_name in contents: 

        full_path = os.path.join(file_path, file_name)

        is_file = os.path.isfile(full_path)
        is_pdf = full_path.endswith('.pdf')

        if is_file and is_pdf:
            path_list.append(full_path)

    return path_list



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Scans a PDF using OCR and saves off a copy')
    parser.add_argument('source', help='directory path or file path')
    parser.add_argument('destination', help='destination to save output')
    parser.add_argument('-d', '--delete', action='store_true', help='delete original file after scan')

    # get arguments
    args = parser.parse_args()

    # check the source is a file or a directory
    if os.path.isdir(args.source):
        files = find_pfd_files(args.source)
    else:
        files = [args.source]

    # for each file (file or directory) scan and save to destination
    for f in files:
       
        # get original source file name and force lower case in destination
        dest_filename = os.path.basename(f)
        dest_filename = dest_filename.lower()
        
        # form destination path
        destination_path = os.path.join(args.destination, dest_filename)

        # command to ocr files
        cmd = f'ocrmypdf --deskew "{f}" "{destination_path}"'
        os.system(cmd)
        sleep(1)

        # if delete argument is true, then test file existence and delete
        if args.delete:

            if os.path.exists(destination_path):
                os.remove(f.replace('"', ''))
