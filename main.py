#!/usr/bin/env python3

import os
import logging
import subprocess
import datetime


def list_folder_content(dir):
    for root, dirs, files in os.walk(dir):
        for d in dirs:
            list_folder_content(d)
            log(d)
            os.rmdir(d)

        for file in files:
            abs_path_file = '/'.join([root, file])
            if is_file_older_than_four_days(abs_path_file):
                remove_file(abs_path_file)


def is_file_older_than_four_days(file):
    date_byte = subprocess.check_output(["date", "-r", file, "+%D"])
    date_string = date_byte.decode('utf-8')
    month, day, year = date_string.split('/')
    date_date = datetime.date(int(year) + 2000, int(month), int(day))
    today = datetime.datetime.today().date()

    age = (today - date_date).days
    is_older = True if age > 0 else False
    return is_older


def remove_file(file):
    log(file)
    os.remove(file)


def log(file):
    logging.basicConfig(filename=r'/home/danilo/log/clearDownloads', level=logging.INFO)
    logging.info(f'REMOVED: file or dir {file} at {datetime.datetime.now()}')


if __name__ == '__main__':
    os.chdir('/home/danilo/Downloads')
    list_folder_content(os.getcwd())
