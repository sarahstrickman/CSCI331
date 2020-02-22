'''
Homewok 2-P : Implement a random-restart hill climbing algorithm that
solves the Countdown Numbers Game.

CSCI-331-02
Sarah Strickman
sxs4599
'''
import sys
import random
import time
import math

ops = "+-*/"

optimalNumbers = []     # optimal numbers so far
optimalOperations = []  # optimal operations so far
optimalDiff = -1    # height of the optimal sequence (lower == better)

numbersList = []    # current list of all numbers being given
operations = []     # current list of all operations
target = 0          # target number

startTime = 0
endTime = 0

'''
From a starting state, climb to find a local "best state".

Finds the local maxima from a given state. This function finds
the first available uphill state, as opposed to the steepest one.
'''
def climb():
    global numbersList
    global operations

    localMaxNums = []   # local max list of numbers
    localMaxOps = []    # local max list of operations
    localMaxDiff = -1

    # set the local max to be the starting state.
    localMaxNums.append(numbersList[0])
    for i in range(0, 98):
        localMaxNums.append(numbersList[i + 1])
        localMaxOps.append(operations[i])
    localMaxNums.append(numbersList[99])
    localMaxDiff = -1

    # swap numbers
    for j in range(0, 99):
        for k in range(j, 99):
            temp = numbersList[j]
            numbersList[j] = numbersList[k]
            numbersList[k] = temp

            currDiff = evaluate(numbersList, operations)
            # you found a better neighboring state
            if (localMaxDiff < 0) or (currDiff < localMaxDiff):
                localMaxNums[0] = numbersList[0]
                for i in range(0, 98):
                    localMaxNums[i + 1] = numbersList[i + 1]
                    localMaxOps[i] = operations[i]
                localMaxNums[99] = numbersList[99]
                localMaxDiff = currDiff
                store = j
            else:
                # swap them back
                temp = numbersList[k]
                numbersList[k] = numbersList[j]
                numbersList[j] = temp

    # change operations
    currIdx = 0
    while currIdx < 98:
        store = operations[currIdx]
        for j in ops:
            operations[currIdx] = j
            currDiff = evaluate(numbersList, operations)

            # you found a better neighboring state
            if (localMaxDiff < 0) or (currDiff < localMaxDiff):
                localMaxNums[0] = numbersList[0]
                for i in range(0, 98):
                    localMaxNums[i + 1] = numbersList[i + 1]
                    localMaxOps[i] = operations[i]
                localMaxNums[99] = numbersList[99]
                localMaxDiff = currDiff
                store = j
                currIdx = -1
            else:
                operations[currIdx] = store
        currIdx += 1
    
    # replace the global with the local max
    localMaxNums[0] = numbersList[0]
    for i in range(0, 98):
        numbersList[i + 1] = localMaxNums[i + 1]
        operations[i] = localMaxOps[i]
    numbersList[99] = localMaxNums[99]


'''
generate a random state while you haven't passed the specified time.
Perform hill climbing on the random state.
'''
def randomRestart():
    global optimalDiff
    global optimalNumbers
    while time.time() < endTime:
        genRandomState()
        climb()     # find the local maxima and compare it to the highest maxima
        currDiff = evaluate(numbersList, operations)
        if (optimalDiff < 0) or (currDiff < optimalDiff):
            optimalNumbers[0] = numbersList[0]
            for i in range(0, 98):
                optimalNumbers[i + 1] = numbersList[i + 1]
                optimalOperations[i] = operations[i]
            optimalDiff = currDiff


'''
generate a random state to start from.

This function shuffles the numbers, and also randomizes each of
the operations that are performed between numbers.
'''
def genRandomState():
    global numbersList
    global operations
    random.shuffle(numbersList)
    for i in range(0,98):
        operations[i] = ops[random.randint(0,3)]


'''
evaluate the current state.
return : the absolute value of the difference between the target and the evaluated state.

lower number == better state
0 is the optimal solution.
'''
def evaluate(numList, opList):
    accum = numList[0]
    for i in range(0,98):
        if (opList[i] == "+"):
            accum = accum + numList[i + 1]
        if (opList[i] == "-"):
            accum = accum - numList[i + 1]
        if (opList[i] == "*"):
            accum = accum * numList[i + 1]
        if (opList[i] == "/"):
            # default to addition as backup to avoid divideByZero
            if (numList[i + 1] == 0):
                opList[i] = "+"
                accum = accum + numList[i + 1]
            else:
                accum = accum / numList[i + 1]
    return abs(target - accum)


'''
read the numbers from a file.
'''
def readNumbers(filename):
    f = open(filename)
    st = f.readline()
    stl = st.split(" ")
    for i in stl:
        numbersList.append(int(i))
    f.close()

'''
print a sequence of numbers/operations.
'''
def printOptimal():
    print("Difference between evaluated sequence and target number:", optimalDiff)

    print("Optimal Sequence found: ", end="")
    for i in range(0, 98):
        print(optimalNumbers[i], optimalOperations[i], end=" ")
    print(optimalNumbers[99])


def main():
    # get 100 1-digit numbers
    global numbersList
    if len(sys.argv) < 2:
        print("Usage: python3 2-P.py inputFile [target] [time-limit]")
        exit()
    readNumbers(sys.argv[1])

    # initialize operations
    global operations
    for i in range(0, 98):
        operations.append("+")

    # get 1 4-digit number
    global target
    target = random.randint(1000, 9999)
    if len(sys.argv) >= 3:
        target = int(sys.argv[2])
    
    # initialize the global maximum
    global optimalNumbers
    global optimalOperations
    global optimalDiff
    optimalNumbers.append(numbersList[0])
    for i in range(0, 98):
        optimalNumbers.append(numbersList[i + 1])
        optimalOperations.append(operations[i])
    optimalNumbers.append(numbersList[99])
    optimalDiff = -1

    # get expiration time
    global startTime
    global endTime
    startTime = time.time()
    endTime = startTime + 3600
    if len(sys.argv) >= 4:
        endTime = startTime + float(sys.argv[3])

    # perform random-restart hill-climb and print the optimal solution
    randomRestart()
    printOptimal()
    

main()