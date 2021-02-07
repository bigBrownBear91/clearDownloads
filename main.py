#!/usr/bin/env python3

import os
import logging
import subprocess
import datetime
import argparse


def list_folder_content_and_delete_it(dir):
    for root, dirs, files in os.walk(dir):
        for d in dirs:
            list_folder_content_and_delete_it(d)
            try:
                logging.info(f'REMOVED: file or dir {d} at {datetime.datetime.now()}')
                os.rmdir(d)
            except OSError:
                logging.exception(f'EXCEPTION: {d} contains files that are not old enough to be deleted. Hence, the '
                                  f'directory remains.')

        for file in files:
            abs_path_file = '/'.join([root, file])
            if is_file_older_than_t_days(abs_path_file):
                logging.info(f'REMOVED: file or dir {abs_path_file} at {datetime.datetime.now()}')
                os.remove(abs_path_file)


def is_file_older_than_t_days(file):
    date_as_byte = subprocess.check_output(["date", "-r", file, "+%D"])
    date_as_string = date_as_byte.decode('utf-8')
    month, day, year = date_as_string.split('/')
    date_as_date = datetime.date(int(year) + 2000, int(month), int(day))
    today = datetime.datetime.today().date()

    age = (today - date_as_date).days
    return age > FILE_AGE


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-dir', '--directory', default='/home/danilo/Downloads', type=str, dest='directory')
    parser.add_argument('-t', '--file-age', default=4, type=int, dest='file_age')
    args = vars(parser.parse_args())

    DIRECTORY = args['directory']
    FILE_AGE = args['file_age']

    logging.basicConfig(filename=r'/home/danilo/log/clearDownloads', level=logging.INFO)
    os.chdir(DIRECTORY)
    list_folder_content_and_delete_it(os.getcwd())
