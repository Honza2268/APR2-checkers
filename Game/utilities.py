from constants import *
import csv
import shutil


def debug_print(message):
    if DEBUG_OUT:
        print(message)


def save_dict_csv(data, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        for k, v in data.items():                        
            writer.writerow((k,v))


def load_dict_csv(filename):
    data = {}
    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            data[row[0]] = row[1]
    return data


def clear_screen():
    print('\x1B[H\x1B[2J', end='')


def get_boxed_text(content: str | list, width: int = 0, height: int = 0, line_set: Line_Types = ascii_light):
    max_length = 0
    line_count = 0

    lines = content.split('\n')

    for line in lines:
        if len(line) > max_length:
            max_length = len(line)
        line_count += 1

    lines_to_append = 0
    lines_to_prepend = 0

    if line_count < height:
        lines_to_prepend = (height - line_count) // 2
        lines_to_append = (height - line_count) - lines_to_prepend

    if width <= max_length:
        width = max_length + 2
    if height <= line_count:
        height = line_count

    top_line = f'{line_set.top_left}{line_set.horizontal*width}{line_set.top_right}\n'
    bottom_line = f'{line_set.bottom_left}{line_set.horizontal*width}{line_set.bottom_right}'

    output = top_line

    for _ in range(lines_to_prepend):
        output += f'{line_set.vertical}{" "*width}{line_set.vertical}\n'

    for line in lines:
        output += f'{line_set.vertical}{line.strip().center(width, " ")}{line_set.vertical}\n'

    for _ in range(lines_to_append):
        output += f'{line_set.vertical}{" "*width}{line_set.vertical}\n'

    output += bottom_line

    return output


def get_terminal_size():
    return shutil.get_terminal_size((80, 20))
