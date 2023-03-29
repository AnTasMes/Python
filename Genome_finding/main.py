import math
import os


def getFile(path):
    FILE_LIST = []
    for roots, dirs, files in os.walk(path):
        for file in files:
            filePath = f"{roots}/{file}".replace('\\', '/')
            FILE_LIST.append(filePath)
    return FILE_LIST


def getLines(file):
    string = ''
    for i, lines in enumerate(file):
        if i:
            string += lines
    return string


def findOne(code, start=0,  failPercTTG=0.8, failPercTAT=0.8, failPercAAG=0.9, failPercATG=1, failPerctStop=1, **kwargs):
    # print(f"{start=}")
    stringTTG = 'TTGACA'
    stringTAT = 'TATAAT'  # 16-19
    stringAGG = 'AGGAGGT'  # UNDEF
    stringATG = 'ATG'  # 5-8
    stopStrings = ['TAA', 'TAG', 'TGA']  # 900-1000

    failSpaceTTG = math.floor(failPercTTG*len(stringTTG))
    failSpaceTAT = math.floor(failPercTAT*len(stringTAT))
    failSpaceAGG = math.floor(failPercAAG*len(stringAGG))
    failSpaceATG = math.floor(failPercATG*len(stringATG))
    # 'string': [stringTTG, stringTAT, stringAGG, stringATG],
    STRING_LSIT = {
        'string': [stringTTG, stringTAT, stringAGG, stringATG],
        'failSpace': [failSpaceTTG, failSpaceTAT, failSpaceAGG, failSpaceATG]
    }

    currentPos = [0, 0]
    pastPos = [0, 0]
    tracker = 0
    genomeStart = 0
    genomeEnd = 0
    for i in range(len(code)):
        for index, sequence in enumerate(STRING_LSIT['string']):
            for j in range(start, len(code)):
                past = j
                freeCounter = 0
                for x in range(past, len(sequence)+past):
                    try:
                        if sequence[x-past] == code[x]:
                            freeCounter += 1
                    except:
                        return 0, x
                if freeCounter >= STRING_LSIT['failSpace'][index]:
                    currentPos = [past, past+len(sequence)-1]
                    break
            diff = currentPos[0] - pastPos[1]
            if sequence == 'TTGACA':
                genomeStart = currentPos[0]
                start = currentPos[1] + 14
            if sequence == 'TATAAT' and diff >= 15 and diff <= 19:
                tracker += 1
                start = x
            if sequence == 'AGGAGGT' and tracker == 1:
                tracker += 1
                start = currentPos[1]+3
            if sequence == 'ATG' and tracker == 2 and diff >= 5 and diff <= 8:

                cp = currentPos[1]
                for stop in stopStrings:
                    for i in range(cp, cp+1100):
                        past = i
                        freeCounter = 0
                        for x in range(past, len(stop)+past):
                            try:
                                if code[x] == stop[x-past]:
                                    freeCounter += 1
                            except:
                                #print(x, len(code))
                                return 0, x

                        if freeCounter == len(stop):
                            currentPos = [past, past+len(stop)-1]
                            diff = currentPos[0] - cp
                            if diff >= 900 and diff <= 1100:
                                print(f'FOUND AT {currentPos}')
                                return genomeStart, currentPos[1]
            pastPos = currentPos

        start = genomeStart+len(STRING_LSIT['string'][0])-3
        #start = currentPos[1] + 1
        tracker = 0
    print()


# FROM: AGGAGGT = [1040612, 1040618] TO ATG = [1040623, 1040625] ==> 5
# 1040070 1040663
if __name__ == "__main__":
    DATA = r'D:\Programming\Python\Genome_finding\Data'
    FILES = getFile(DATA)
    CODE = []
    for path in FILES:
        with open(path, 'r') as file:
            CODE.append(getLines(file))

    genomes = []
    first = 0
    last = 0
    for code in CODE:
        while last < len(code):
            first, last = findOne(code, last+2)
            genomes.append([first, last])
            #print(first, last)
    genomes.pop(-1)

    print("LISTING GENOME POSITIONS BELOW:")
    for i, gen in enumerate(genomes):
        print(f"{i+1} ==> START: {gen[0]} ; END {gen[1]}")
