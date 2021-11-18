import matplotlib.pyplot as plt
import random


def GetPopulation(population: list[str], selection):
    cAA = 0
    cAa = 0
    caa = 0
    AaChoice = ['a', 'A']

    tmpPop = random.choices(population, k=selection)
    newPop = []
    for x in tmpPop:
        if x == 'AA':
            newPop.extend('A' for x in range(10))
        elif x == 'aa':
            newPop.extend('a' for x in range(10))
        elif x == 'Aa':
            newPop.extend(random.choice(AaChoice) for x in range(10))
    #print(f"LEN newPop: {len(newPop)}")
    rIndex1 = random.randrange(0, len(newPop))
    rIndex2 = random.randrange(0, len(newPop))
    population = []
    for x in range(len(newPop)):
        while not newPop[rIndex1] and not newPop[rIndex2]:
            rIndex1 = random.randrange(0, len(newPop))
            rIndex2 = random.randrange(0, len(newPop))
        string = newPop[rIndex1] + newPop[rIndex2]
        if string == 'AA':
            cAA += 1
        elif string == 'Aa' or string == 'aA':
            string = 'Aa'
            cAa += 1
        elif string == 'aa':
            caa += 1
        population.append(string)
        rIndex1 = random.randrange(0, len(newPop))
        rIndex2 = random.randrange(0, len(newPop))

    cnt = caa + cAA + cAa
    # print(cnt)
    return [population, caa, cAA, cAa]


# def makeGraph(units: list[int]):


if __name__ == "__main__":
    randomSelection = 125

    lAA = ['AA'] * 0
    lAa = ['Aa'] * 250
    laa = ['aa'] * 0

    caa = len(laa)
    cAa = len(lAa)
    cAA = len(lAA)
    x = 0
    lpop = laa + lAA + lAa
    lcAA = []
    lcaa = []
    lcAa = []
    while cAa:
        lpop, caa, cAA, cAa = GetPopulation(lpop, randomSelection)
        if not caa and not cAa:
            break
        if not cAA and not cAa:
            break
        lcAA.append(cAA)
        lcaa.append(caa)
        lcAa.append(cAa)
        print(f"Iteration: {x} ==> AA: {cAA} ; Aa: {cAa} ; aa: {caa}")
        x += 1
    print(f"Iteration: {x} ==> AA: {cAA} ; Aa: {cAa} ; aa: {caa}")

    plt.plot(range(x), lcaa, 'k')
    plt.plot(range(x), lcAa, 'm')
    plt.plot(range(x), lcAA, 'r')
    plt.show()

'''
newPop2 = []
randIndex1 = 0
randIndex2 = 0
for x in range(0, 1000):
    if newPop[randIndex1] and newPop[randIndex2]:
        randIndex1 = random.randrange(0, len(newPop))
        randIndex2 = random.randrange(0, len(newPop))
        print(newPop[randIndex1], newPop[randIndex2])
        # tmpString = newPop[randIndex1]+newPop[randIndex2]
        # newPop2.append(tmpString)

        newPop[randIndex1] = ''
        newPop[randIndex2] = ''

print(newPop2)
'''
