import os
from time import sleep
import argparse

def find_pfd_files(file_path):

    path_list = []

    # use built-in method to find all files
    for root, _, files in os.walk(file_path):
        if root[len(file_path):].count(os.sep) < 1:
            for name in files:
                if name.find('.pdf') >= 0:
                    path_list.append(os.path.join(root, name))

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

        # check source for spaces
        if f.find(' ') >= 0:
            f = '"%s"' % f
        
        # get original source file name and force lower case in destination
        dest_filename = os.path.basename(f)
        dest_filename = dest_filename.lower()
        
        # form destination path
        destination_path = os.path.join(args.destination, dest_filename)

        # check destination path for spaces. skip trailing quote
        if destination_path.find(' ') >= 0:
            destination_path = '"%s' % destination_path

        # command to ocr files
        cmd = 'ocrmypdf --deskew %s %s' % (f, destination_path)
        os.system(cmd)
        sleep(1)

        # if delete argument is true, then test file existence and delete
        if args.delete:

            if os.path.exists(destination_path.replace('"', '')):
                os.remove(f.replace('"', ''))
