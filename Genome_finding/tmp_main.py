import regex as r
import math

from main import FindFiles

randString = 'ATCCCGGCCCCGGCAGAACCGACCTATCGTTCTAACGTAAACGTCAAACACACGTTTGATAACTTCGTTG'


freeCounter = 0
tmpCounter = 0


def FindSequence(string, sequence, rng):
    failPerc = math.floor(len(sequence)*0.8)

    freeCounter = 0

    span = [0, 0]
    for i in range(rng):
        past = i
        span[0] = i
        for x in range(past, len(sequence)+past):

            if string[x] == sequence[x-past]:
                freeCounter += 1
        # print()
        span[1] = x
        if freeCounter >= failPerc:
            break
        freeCounter = 0

    return span


if __name__ == "__main__":
    find = 'TATAAT'
    find2 = 'TTGACA'
    find3 = 'AGGAGGT'

    firstRange = 30
    secondRange = firstRange + 30
    thirdRange = secondRange + 200
    #failPerc = math.floor(len(find2)*0.9)

    spanTAT = FindSequence(randString, find, firstRange)
    print(f"{spanTAT=}")

    spanTTG = FindSequence(randString, find2, secondRange)
    print(f"{spanTTG=}")

    spanTAT = FindSequence(randString, find2, firstRange+19)
    print(spanTAT)

    # print(tmpString)

    # print(fin2)
    # print(string11)
