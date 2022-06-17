from constants import *
import csv


def debug_print(message):
    if DEBUG_OUT:
        print(message)


def save_dict_csv(data, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        for k, v in data:
            writer.writerow(f'{k},{v}')


def load_dict_csv(filename):
    data = {}
    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            data[row[0]] = row[1]
    return data
