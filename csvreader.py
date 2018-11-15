import csv

global csv_reader


def cvr_init_with_header(filename, delimiter=','):
    global csv_reader

    return csv.DictReader(open(filename), delimiter=delimiter)
