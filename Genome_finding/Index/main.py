from sequence import Sequence
from sequence import mainSeq


import math
import os

path = r'D:\Programming\Python\Genome_finding\Data'


def getFiles(path):
    l = []
    for roots, dirs, files in os.walk(path):
        for file in files:
            location = f"{roots}/{file}".replace('\\', '/')
            l.append(location)
    return l


def getLines(file):
    s = ''
    with open(file, 'r') as file:
        for i, line in enumerate(file):
            if i:
                s += line
    return s


def findSequence(genome: list[str], sequence, start, end, failSpace):
    for i in range(start, end-1):
        past = i
        failCounter = 0
        for x in range(past, len(sequence) + past):
            try:
                if genome[x] == sequence[x-past]:
                    failCounter += 1
            except:
                return [0, 0]
        if failCounter >= failSpace:
            return [x-len(sequence), x]
    return [0, 0]


def checkDiff(objList, sequenceIndex):
    if objList[sequenceIndex].space[1] == 0:
        #print(objList[sequenceIndex], "IN FUNCTION")
        return 1
    diff = objList[sequenceIndex].cord[0] - objList[sequenceIndex-1].cord[1]
    if diff >= objList[sequenceIndex].space[0] and diff <= objList[sequenceIndex].space[1]:
        return 1
    else:
        return 0


def goThrough(genomes):
    endList = ['TAA', 'TAG', 'TGA']
    sequenceList = ['TTGACA', 'TATAAT', 'AGGAGGT', 'AGT']
    start = 0
    genomeList = []
    for i in range(len(genomes[0])-1):
        obj = []
        found = 0
        for seqIndex, sequence in enumerate(sequenceList):
            tmpObj = Sequence(sequence)
            beg, end = findSequence(
                genomes[0], sequence, start, len(genomes[0]), tmpObj.failSpace)
            tmpObj.cord = [beg, end]
            if beg == 0 and end == 0:
                return genomeList
            obj.append(tmpObj)
            start = obj[seqIndex].cord[1]

            if seqIndex == 1 and checkDiff(obj, seqIndex):
                found += 1
            elif seqIndex == 2 and found == 1 and checkDiff(obj, seqIndex):
                found += 1
            elif seqIndex == 3 and found == 2:
                if checkDiff(obj, seqIndex):
                    for ending in endList:

                        beg, end = findSequence(
                            genomes[0], ending, start, start+1100, len(ending))
                        if beg == 0 and end == 0:
                            continue
                        else:
                            obj.append(Sequence('END', cord=[beg, end]))
                        if checkDiff(obj, seqIndex):
                            print([obj[0].cord[0], obj[seqIndex].cord[1]])
                            genomeList.append(
                                [obj[0].cord[0], obj[seqIndex].cord[1]])
                            break
                        else:
                            obj.pop(-1)
        start = obj[0].cord[1]
        mainSeq.resetCount(mainSeq)


if __name__ == '__main__':
    files = getFiles(path)
    genomes = []

    for file in files:
        genomes.append(getLines(file))

    genomeList = goThrough(genomes)
    for i, genes in enumerate(genomeList):
        print(i+1, genes)
