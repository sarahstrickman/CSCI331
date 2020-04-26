'''
This file has all functions and definitions relating to adaboosting with
decision stumps.
'''

import os
from dataclasses import dataclass
import re
import pickle
from typing import Union
import math
from lab2DT import hasFeature

@dataclass
class textEntity:
    def __init__(self,
                 text: str = "",
                 lang: str = "",
                 weight: float = 0.0):
        self.text = text
        self.lang = lang
        self.weight = weight
    def __hash__(self):
        st = self.text + str(self.weight) + self.lang
        return st.__hash__()

@dataclass
class stump:
    def __init__(self,
                 feature: str = "",
                 yesMaj: str = "nl",
                 noMaj: str = "en",
                 yesEN: set = set(),
                 yesNL: set = set(),
                 noEN: set = set(),
                 noNL: set = set()):
        self.feature = feature
        self.yesMaj = yesMaj
        self.noMaj = noMaj
        self.yesEN = yesEN
        self.yesNL = yesNL
        self.noEN = noEN
        self.noNL = noNL
    def __hash__(self):
        return self.feature.__hash__()

'''
given a filename, get all the samples. Assign default weight to sample

return a set containing all samples.
'''
def readFile(filename):
    sampleSet = set()
    try:
        fp = open(filename, encoding="utf-8")
        lines = fp.readlines()
        totEntries = len(lines)
        for line in lines:
            l = line.strip().split("|")
            sampleSet.add(textEntity(text=l[1], lang=l[0], weight= (1 / totEntries)))
        fp.close()
        return sampleSet
    except:
        print("Error: invalid filename or file format.")
        exit()

'''
generate stumps. return a set of the stumps
'''
def generateStumps(samples, featurelist=None):
    if featurelist is None:
        featurelist = {"hasHET",
                       "hasNAAR",
                       "hasDAT",
                       "hasHEEFT",
                       "hasARE",
                       "hasZIJN",
                       "hasNIET",
                       "hasA",
                       "hasBE",
                       "hasDE",
                       "hasIJCons",
                       "hasUmlaut",
                       "hasConsDE",
                       "hasVowECons",
                       "has2VowCons",
                       "hasIJ",
                       "avgLen4"}
    stumps = set()
    for feature in featurelist:
        stumps.add(makeStump(samples, feature))
    return stumps

'''
create a stump.

samples: samples to include in the creation of the stump
feature: the feature associated with this stump
'''
def makeStump(samples, feature):
    s = stump(feature=feature)
    for sample in samples:
        if hasFeature(sample, feature):
            if sample.lang == "en":
                s.yesEN.add(sample)
            else:
                s.yesNL.add(sample)
        else:
            if sample.lang == "en":
                s.noEN.add(sample)
            else:
                s.noNL.add(sample)

    if len(s.yesEN) > len(s.yesNL):
        s.yesMaj = "en"
    else:
        s.yesMaj = "nl"

    if len(s.noEN) > len(s.noNL):
        s.noMaj = "en"
    else:
        s.noMaj = "nl"

    return s

'''
find the stump with the lowest gini score
'''
def lowestStumpGini(stumps):
    minStump = None
    minGini = 100.00
    for s in stumps:
        sgini = stumpGini(s)
        if sgini < minGini:
            minGini = sgini
            minStump = s
    return s

'''
return the gini value of a single stump.
'''
def stumpGini(s: stump):
    numyesEN = len(s.yesEN)    # has feature and is english
    numyesNL = len(s.yesNL)    # has feature and is dutch
    totyes = numyesEN + numyesNL
    numnoEN = len(s.noNL)      # doesn't have feature and is english
    numnoNL = len(s.noNL)      # doesn't have feature and is dutch
    totno = numnoEN + numnoNL
    tot = totno + totyes

    yesgini = currGini(totyes, numyesEN, numyesNL)
    yesWeighted = (totyes / tot) * yesgini

    nogini = currGini(totno, numnoEN, numnoNL)
    noWeighted = (totno / tot) * nogini

    return yesWeighted + noWeighted
def currGini(tot, numEN, numNL):
    if tot == 0:
        return 0
    pEN = numEN / float(tot)
    pNL = numNL / float(tot)
    return 1.0 - (pEN ** 2.0) - (pNL ** 2.0)

'''
how much say does this stump get?
'''
def getSay(s : stump):
    totErr = getTotError(s)
    if totErr <= 0.0:
        totErr = 0.001
    elif totErr >= 1.0:
        totErr = 0.999
    return .5 * math.log((1.0 - totErr) / totErr)

def lowestStumpTotError(stumps):
    minStump = None
    minGini = 100.00
    for s in stumps:
        sgini = getTotError(s)
        if sgini < minGini:
            minGini = sgini
            minStump = s
    return s

'''
get the total error of a stump (will be a float)
'''
def getTotError(s : stump):
    weight = 0.0
    if s.yesMaj == "en":
        for sample in s.yesNL:
            weight += sample.weight
    else:   # yesMaj is NL
        for sample in s.yesEN:
            weight += sample.weight

    if s.noMaj == "en":
        for sample in s.noNL:
            weight += sample.weight
    else:   # noMaj is ML
        for sample in s.noEN:
            weight += sample.weight

    return weight

'''
update the weights of incorrect samples
'''
def updateWeights(s : stump):
    say = getSay(s)
    if s.yesMaj == "en":
        for sample in s.yesNL:
            prev = sample.weight
            sample.weight = prev * (math.e ** say)
        for sample in s.yesEN:
            prev = sample.weight
            sample.weight = prev * (math.e ** (-say))
    else:
        for sample in s.yesEN:
            prev = sample.weight
            sample.weight = prev * (math.e ** say)
        for sample in s.yesNL:
            prev = sample.weight
            sample.weight = prev * (math.e ** (-say))

    if s.noMaj == "en":
        for sample in s.noNL:
            prev = sample.weight
            sample.weight = prev * (math.e ** say)
        for sample in s.noEN:
            prev = sample.weight
            sample.weight = prev * (math.e ** (-say))
    else:
        for sample in s.noEN:
            prev = sample.weight
            sample.weight = prev * (math.e ** say)
        for sample in s.noNL:
            prev = sample.weight
            sample.weight = prev * (math.e ** (-say))

'''
normalize text weights so that they add up to 1
'''
def normalizeWeights(s : stump):
    weightSum = 0.00
    for sample in s.yesEN:
        weightSum += sample.weight
    for sample in s.yesNL:
        weightSum += sample.weight
    for sample in s.noEN:
        weightSum += sample.weight
    for sample in s.noNL:
        weightSum += sample.weight

    if weightSum <= 0.0:
        weightSum = 0.001

    for sample in s.yesEN:
        prev = sample.weight
        sample.weight = prev / weightSum
    for sample in s.yesNL:
        prev = sample.weight
        sample.weight = prev / weightSum
    for sample in s.noEN:
        prev = sample.weight
        sample.weight = prev / weightSum
    for sample in s.noNL:
        prev = sample.weight
        sample.weight = prev / weightSum

'''
make a stump forest.

while features isn't empty
    generate stumps
    get stump with lowest gini
    add this stump to our forest
    remove associated feature from featurelist
    
    update weights
    normalize weights

:return the forest
'''
def makeForest(samples):
    forest = set()
    featurelist = {"hasHET",
                   "hasNAAR",
                   "hasDAT",
                   "hasHEEFT",
                   "hasARE",
                   "hasZIJN",
                   "hasNIET",
                   "hasA",
                   "hasBE",
                   "hasDE",
                   "hasIJCons",
                   "hasUmlaut",
                   "hasConsDE",
                   "hasVowECons",
                   "has2VowCons",
                   "hasIJ",
                   "avgLen4"}
    while len(featurelist) > 0:
        stumps = generateStumps(samples, featurelist)
        s = lowestStumpTotError(stumps)
        forest.add(s)
        featurelist.remove(s.feature)

        updateWeights(s)
        normalizeWeights(s)

        samples = set()     # update samples to have new weights
        for i in s.yesEN:
            samples.add(i)
        for i in s.yesNL:
            samples.add(i)
        for i in s.noEN:
            samples.add(i)
        for i in s.noNL:
            samples.add(i)
    return forest



def trainAda(filename):
    samples = readFile(filename)
    forest = makeForest(samples)
    return forest

def predictAda(sample, forest):
    numEN = 0.00
    numNL = 0.00
    sample = textEntity(text=sample)
    for s in forest:
        if hasFeature(sample, s.feature):
            if s.yesMaj == "en":
                numEN += (1.00 * getSay(s))
            else:
                numNL += (1.00 * getSay(s))
        else:
            if s.noMaj == "en":
                numEN += (1.00 * getSay(s))
            else:
                numNL += (1.00 * getSay(s))

    if numEN > numNL:
        return "en"
    return "nl"

def testAccuracyAda(lang, forest, samplefile):
    numIncorrect = 0
    fp = open(samplefile, encoding="utf-8")
    samples = fp.readlines()
    totalSamples = len(samples)
    for sample in samples:
        if predictAda(sample, forest) != lang:
            print(str(numIncorrect) + ".\t" +sample.strip())
            numIncorrect += 1
    accuracy = (totalSamples - numIncorrect) / totalSamples
    print("---------\naccuracy:\t" + str(accuracy * 100) + "%")
    fp.close()
    return accuracy

def exportForest(data, filename):
    outfile = open(filename, 'wb')
    pickle.dump(data, outfile)
    outfile.close()

def importForest(filename):
    infile = open(filename, 'rb')
    new_dict = pickle.load(infile)
    infile.close()
    return new_dict


if __name__ == "__main__":
    forest = None
    o = input("load file name: ")
    if len(o) > 0:
        o = "knowledge_base/" + o
        forest = importForest(o)
    else:
        print("re-training...")
        filename = "training_data/train_master.dat"  # input("filename: ")
        forest = trainAda(filename)

    s = input("save file name: ")
    if len(s) > 0:
        s = "knowledge_base/" + s
        exportForest(forest, s)

    t = input("test file name: ")
    l = input("test lang: ")
    if len(t) > 0:
        pass
        testAccuracyAda(l, forest, t)
    else:
        text = input("sample text (qq for escape): ")
        while text != "qq":
            lang = predictAda(text, forest)
            print(lang + "\t|\t" + text)
            text = input("sample text (qq for escape): ")