import os
import math

path = r'D:\Programming\Python\Genome_finding\Data'


def FindFiles(path):
    filePrefix = []
    locs = []
    for roots, dirs, files in os.walk(path):
        for file in files:
            filePrefix.append(file.split('.')[0])
            locs.append(f'{roots}/{file}'.replace('\\', '/'))

    FILE = {
        'prefix': filePrefix,
        'path': locs
    }
    return FILE


def FindSequence(string, sequence, start, stop, perc=0.8):
    failPerc = math.floor(len(sequence)*perc)

    freeCounter = 0

    span = [0, 0]
    for i in range(start, stop):
        past = i
        span[0] = i
        for x in range(past, len(sequence)+past):
            #print(string[x], sequence[x-past])
            if string[x] == sequence[x-past]:
                freeCounter += 1
        # print()
        span[1] = x
        if freeCounter >= failPerc:
            break
        freeCounter = 0

    if freeCounter < failPerc:
        print("Couldnt find anything in those ranges")
        return 0

    return span


if __name__ == "__main__":
    find1 = 'TATAAT'
    find2 = 'TTGACA'
    find3 = 'AGGAGGT'
    find4 = 'ATG'
    find51 = 'TAA'
    find52 = 'TAG'
    find53 = 'TGA'

    firstRange = [0, 30]
    secondRange = [firstRange[1], firstRange[1] + 30]
    thirdRange = [secondRange[1], secondRange[1] + 200]
    fourthRange = [thirdRange[1], thirdRange[1] + 10]

    files = FindFiles(path)
    genome = ''
    for file in files['path']:
        with open(file, 'r') as file:
            for i, line in enumerate(file):
                if i == 0:
                    continue
                genome += line
    #Provera duzina 
    #IZMEDJU 'TATAAT' - 'TTGACA' 16-19
    #IZMEDJU 'TATAAT' - 'TTGACA' 16-19
    spanTTG = FindSequence(genome, find1, firstRange[0], firstRange[1])
    print(f"{spanTTG=}")
    secondRange = [spanTTG[1], spanTTG[1]+30]
    spanTAT = FindSequence(genome, find2, secondRange[0], secondRange[1])
    print(f"{spanTAT=}")
    thirdRange = [spanTAT[1], spanTAT[1]+200]
    spanAAG = FindSequence(genome, find3, thirdRange[0], thirdRange[1])
    print(f"{spanAAG=}")
    fourthRange = [spanAAG[1], spanAAG[1]+20]
    spanATG = FindSequence(genome, find4, fourthRange[0], fourthRange[1], 1)
    print(f"{spanATG=}")
    fifthRange = [spanATG[1], spanATG[1]+1000]
    print('TAA _______')
    spanTAA = FindSequence(genome, find51, fifthRange[0], fifthRange[1], 1)
    print('TAG _______')
    spanTAG = FindSequence(genome, find52, fifthRange[0], fifthRange[1], 1)
    print('TGA _______')
    spanTGA = FindSequence(genome, find53, fifthRange[0], fifthRange[1], 1)

    if spanTAA:
        print(f"{spanTAA=}")
    if spanTAG:
        print(f"{spanTAG=}")
    if spanTGA:
        print(f"{spanTGA=}")
