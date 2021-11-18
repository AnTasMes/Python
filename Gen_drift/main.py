#
#   Small project that simulates simple genetic drift by utilizing basic rules
#   This tast was made as practice for creating real simulations of a kind
#   Author: AnTasMes --> Task giver: PetKika
#

import matplotlib.pyplot as plt
import random


def newPopulation(population, selection):
    # If for some reason we try to select more units that we have in population
    if selection > len(population):
        print("SELECTION NUMBER IS HIGHER THAN THE NUMBER OF UNITS")
        return

    # Making a temp population made of random selection from mainPopulation
    #tmpPop = random.choices(population, k=selection)
    tmpPop = randomPopulus(population[:], selection)
    # Calculating neccessary gamete production per unit in order to get the unit number back to len(mainPopulation)
    gameteNo = (len(population)*2)//selection
    ch = ['A', 'a']
    # print(f"mainPopulation len: {len(population)}")
    # print(f"tmpPopulation len: {len(tmpPop)}")
    newPopulation = []
    for elem in tmpPop:  # Making a new populus from given random Units
        if elem == 'AA':
            newPopulation.extend(['A']*gameteNo)
        if elem == 'aa':
            newPopulation.extend(['a']*gameteNo)
        if elem == 'Aa':
            # IF Aa there is around 50% of either A or a coming out
            newPopulation.extend(random.choices(ch, k=gameteNo))

    cAA = 0
    cAa = 0  # Defining unit counters
    caa = 0
    # print(f"newPopulation len: {len(newPopulation)}")
    population = []
    randIndex1 = random.randrange(0, len(newPopulation)-1)
    randIndex2 = random.randrange(0, len(newPopulation)-1)
    while newPopulation:
        # Concatinating strings to get back AA ; Aa ; aa respectively
        unit = newPopulation[randIndex1] + newPopulation[randIndex2]

        newPopulation.pop(randIndex1)
        newPopulation.pop(randIndex2)
        if unit == 'AA':
            cAA += 1
        if unit == 'aa':
            caa += 1
        if unit == 'Aa' or unit == 'aA':  # If concatination produces Aa or aA we set it to be Aa
            unit = 'Aa'
            cAa += 1

        population.append(unit)
        # print(len(newPopulation))
        try:  # Try goes only for the last iteration where array is empty
            randIndex1 = random.randrange(0, len(newPopulation)-1)
            randIndex2 = random.randrange(0, len(newPopulation)-1)
        except:
            pass
    #print(f"population len: {len(population)}")
    print(f"AA: {cAA} ; Aa: {cAa} ; aa: {caa} ; comb: {caa+cAA+cAa}")

    return [population, cAA, cAa, caa]


def randomPopulus(population, selecton):
    randIndex = random.randrange(len(population)-1)
    newPopulation = []
    for x in range(selecton):
        newPopulation.append(population[randIndex])
        population.pop(randIndex)
        randIndex = random.randrange(len(population)-1)
    return newPopulation


if __name__ == "__main__":

    select = 10  # Unit selection number
    iter = 50  # Number of iterations
    AA = ['AA']*200
    Aa = ['Aa']*100  # Number of each unit
    aa = ['aa']*200

    # Defining counting arrays needed for plotting the end data
    lIter = []
    lcAA = []
    lcAa = []
    lcaa = []

    # Making the main population
    mainPopulation = AA + Aa + aa

    for x in range(iter+1):
        lIter.append(x)  # Appending iterations to an array for later plotting
        mainPopulation, cAA, cAa, caa = newPopulation(
            mainPopulation, selection=select)

        # Appending unit numbers to corresponding arrays for later plotting
        lcAA.append(cAA)
        lcaa.append(caa)
        lcAa.append(cAa)

    # MAKING A PLOT DESIGN
    plt.style.use('dark_background')
    fix, ax = plt.subplots()
    ax.set_xlabel('TIME / ITERATIONS')
    ax.set_ylabel('SIZE')
    ax.set_title('GENETIC DRIFT SIMPLE SIMULATION')

    lineAA, = ax.plot(lIter, lcAA, 'r', label='AA')
    LineAa, = ax.plot(lIter, lcAa, 'm', label='Aa')
    Lineaa, = ax.plot(lIter, lcaa, 'w', label='aa')

    ax.legend(handles=[LineAa, lineAA, Lineaa])
    plt.show()
