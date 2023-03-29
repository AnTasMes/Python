import numpy as np


def GetData(path):
    with open(path, 'r') as file:
        firstLine = file.readline()
        args = firstLine.replace(' ', '').replace(
            ')\n', '').split('(')[1].split(',')
        print(args)
        for index, line in enumerate(file):
            key, arg = TrimData(line)
            print(key, arg)


def TrimData(line):
    line = line[3:].replace(' ', '').replace('\n', '')
    key, arg = line.split('-->')
    key = key.split(',')
    arg = arg.split(',')
    return key, arg


if __name__ == "__main__":
    GetData(r'./data.txt')
