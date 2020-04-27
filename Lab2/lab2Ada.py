'''
This file has all functions and definitions relating to adaboosting with
decision stumps.
'''

import os
from dataclasses import dataclass
import re
import pickle
import math

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
        return self.text.__hash__()
    def __str__(self):
        return "(text=" + self.text + ", lang = " + self.lang + ", weight = " + str(self.weight) + ")"

@dataclass
class stump:
    def __init__(self,
                 feature: str = "",
                 yesMaj: str = "",
                 noMaj: str = "",
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
    def __str__(self):
        feat = "feat =" + self.feature
        ym = "yesMaj = " + self.yesMaj
        nm = "noMaj = " + self.noMaj
        say = "say = " + str(getSay(self))
        nums = "YEN/YNL/NEN/NNL = " + str(len(self.yesEN)) + "/" + str(len(self.yesNL)) + "/" + str(len(self.noEN)) + "/" + str(len(self.noNL))
        return "(" + feat + ", " + ym + ", " + nm + ", " + say + ", " + nums + ")"
    def freeze(self):
        self.yesEN = frozenset(self.yesEN)
        self.yesNL = frozenset(self.yesNL)
        self.noEN = frozenset(self.noEN)
        self.noNL = frozenset(self.noNL)
        self.frozen = True


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
        fp.close()

        fp = open(filename, encoding="utf-8")
        for line in fp:
            l = line.strip().split("|")
            t = textEntity(text=l[1], lang=l[0], weight= (1 / totEntries))
            sampleSet.add(t)
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
        s = makeStump(samples, feature)
        stumps.add(s)
    return stumps

'''
create a stump.

samples: samples to include in the creation of the stump
feature: the feature associated with this stump
'''
def makeStump(samples, feature):
    s = stump(feature=feature, yesEN=set(), yesNL=set(), noEN=set(),noNL=set())

    for sample in samples:
        newsamp = sample
        if hasFeature(sample, feature):
            if newsamp.lang == "en":
                s.yesEN.add(newsamp)
            else:
                s.yesNL.add(newsamp)
        else:
            if newsamp.lang == "en":
                s.noEN.add(newsamp)
            else:
                s.noNL.add(newsamp)

    if len(s.yesEN) > len(s.yesNL):
        s.yesMaj = "en"
    else:
        s.yesMaj = "nl"

    if len(s.noEN) > len(s.noNL):
        s.noMaj = "en"
    else:
        s.noMaj = "nl"
    s.freeze()
    return s

# def populateValues(samples, s : stump):
#     for sample in samples:
#         if hasFeature(sample, s.feature):
#             if sample.lang == "en":
#                 s.yesEN.add(sample)
#             else:
#                 s.yesNL.add(sample)
#         else:
#             if sample.lang == "en":
#                 s.noEN.add(sample)
#             else:
#                 s.noNL.add(sample)
#
#     if len(s.yesEN) > len(s.yesNL):
#         s.yesMaj = "en"
#     else:
#         s.yesMaj = "nl"
#
#     if len(s.noEN) > len(s.noNL):
#         s.noMaj = "en"
#     else:
#         s.noMaj = "nl"
#     return s

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
    return minStump

'''
return the gini value of a single stump.
'''
def stumpGini(s: stump):
    numyesEN = float(len(s.yesEN))    # has feature and is english
    numyesNL = float(len(s.yesNL))    # has feature and is dutch
    totyes = numyesEN + numyesNL
    numnoEN = float(len(s.noNL))      # doesn't have feature and is english
    numnoNL = float(len(s.noNL))      # doesn't have feature and is dutch
    totno = numnoEN + numnoNL
    tot = totno + totyes

    yesgini = currGini(totyes, numyesEN, numyesNL)
    yesweights = 0.0
    for item in s.yesEN:
        yesweights += item.weight
    for item in s.yesNL:
        yesweights += item.weight
    yesWeighted = yesweights * yesgini

    nogini = currGini(totno, numnoEN, numnoNL)
    noweights = 0.0
    for item in s.noEN:
        noweights += item.weight
    for item in s.noNL:
        noweights += item.weight
    noWeighted = noweights * nogini

    return yesWeighted + noWeighted
def currGini(tot, numEN, numNL):
    if tot == 0.0:
        return 0.0
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

# def lowestStumpTotError(stumps):
#     minStump = None
#     minGini = 100.00
#     for s in stumps:
#         sgini = getTotError(s)
#         if sgini < minGini:
#             minGini = sgini
#             minStump = s
#
#     return s

'''
get the total error of a stump (will be a float)

How many entities did this stump get wrong?
'''
def getTotError(s : stump):
    w = 0.00
    if s.yesMaj == "en":
        for sample in s.yesNL:
            w += sample.weight
    else:   # yesMaj is NL
        for sample in s.yesEN:
            w += sample.weight

    if s.noMaj == "en":
        for sample in s.noNL:
            w += sample.weight
    else:   # noMaj is NL
        for sample in s.noEN:
            w += sample.weight

    return w

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
                   "avgLen4",
                   "hasVAN",
                   "hasAT"}
    while len(featurelist) > 0:
        stumps = generateStumps(samples, featurelist)
        s = lowestStumpGini(stumps)
        forest.add(s)
        featurelist.remove(s.feature)

        updateWeights(s)
        normalizeWeights(s)

        samples.clear()     # update samples to have new weights
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

def predictFile(filename):
    for line in open(filename):
        print(predictAda(line))

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
    samples= open(samplefile, encoding="utf-8")
    totalSamples = 0
    for sample in samples:
        totalSamples += 1
        if predictAda(sample, forest) != lang:
            print(str(numIncorrect) + ".\t" +sample.strip())
            numIncorrect += 1
    accuracy = (totalSamples - numIncorrect) / totalSamples
    print("---------\naccuracy:\t" + str(accuracy * 100) + "%")
    samples.close()
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



'''
check if a feature is true for a given sample 
sample is a textEntity.
'''
def hasFeature(sample, feature):
    if feature == "hasHET":
        return hasHET(sample)
    elif feature == "hasNAAR":
        return hasNAAR(sample)
    elif feature == "hasDAT":
        return hasDAT(sample)
    elif feature == "hasHEEFT":
        return hasHEEFT(sample)
    elif feature == "hasARE":
        return hasARE(sample)
    elif feature == "hasZIJN":
        return hasZIJN(sample)
    elif feature == "hasNIET":
        return hasNIET(sample)
    elif feature == "hasA":
        return hasA(sample)
    elif feature == "hasBE":
        return hasBE(sample)
    elif feature == "hasDE":
        return hasDE(sample)
    elif feature == "hasIJCons":
        return hasIJCons(sample)
    elif feature == "hasUmlaut":
        return hasUmlaut(sample)
    elif feature == "hasConsDE":
        return hasConsDE(sample)
    elif feature == "hasVowECons":
        return hasVowECons(sample)
    elif feature == "has2VowCons":
        return has2VowCons(sample)
    elif feature == "hasIJ":
        return hasIJ(sample)
    elif feature == "avgLen4":
        return avgLen4(sample)
    elif feature == "hasVAN":
        return hasVAN(sample)
    elif feature == "hasAT":
        return hasAT(sample)
    else:
        print("invalid feature")
        return False

'''
functions for the features
'''
def hasHET(sample):
    return " het " in sample.text.lower()
def hasNAAR(sample):
    return " naar " in sample.text.lower()
def hasDAT(sample):
    return " dat " in sample.text.lower()
def hasHEEFT(sample):
    return " heeft " in sample.text.lower()
def hasARE(sample):
    return " are " in sample.text.lower()
def hasZIJN(sample):
    return " zijn " in sample.text.lower()
def hasNIET(sample):
    return " niet " in sample.text.lower()
def hasA(sample):
    # it has to be a lowercase a. (case sensitive)
    return " a " in sample.text
def hasBE(sample):
    return " be " in sample.text.lower()
def hasDE(sample):
    return " de " in sample.text.lower()
def hasIJCons(sample):
    return re.match("ij[b-df-hj-np-tv-z]", sample.text.lower()) is not None
def hasUmlaut(sample):
    r = re.compile(r'[^\W\d_]', re.U)
    return re.match("[\u00c4-\u00cb-\u00cf-\u00d6-\u00dc-\u00e4-\u00eb-\u00ef-\u00f6-\u00fc-\u00ff-\u0178]", sample.text) is not None
def hasConsDE(sample):
    return re.match("[b-df-hj-np-tv-z]de ", sample.text.lower()) is not None
def hasVowECons(sample):
    return re.match("[aiou]e[b-df-hj-np-tv-z]", sample.text.lower()) is not None
def has2VowCons(sample):
    return (re.match("aa[b-df-hj-np-tv-z]", sample.text.lower()) is not None) or \
           (re.match("ee[b-df-hj-np-tv-z]", sample.text.lower()) is not None) or \
           (re.match("ii[b-df-hj-np-tv-z]", sample.text.lower()) is not None) or \
           (re.match("oo[b-df-hj-np-tv-z]", sample.text.lower()) is not None) or \
           (re.match("uu[b-df-hj-np-tv-z]", sample.text.lower()) is not None)
def hasIJ(sample):
    return "ij" in sample.text.lower()
def avgLen4(sample):
    txt = sample.text.replace("."," ")
    txt = sample.text.replace(",", " ")
    txt = txt.split(" ")
    length = len(txt)
    summ = 0
    for item in txt:
        summ += len(item)
    avg = summ / length
    return avg >= 4
def hasVAN(sample):
    return " van " in sample.text.lower()
def hasAT(sample):
    return " at " in sample.text.lower() or "At " in sample.text.lower()


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
    if len(t) > 0:
        l = input("test lang: ")
        testAccuracyAda(l, forest, t)
    else:
        text = input("sample text (qq for escape): ")
        while text != "qq":
            lang = predictAda(text, forest)
            print(lang + "\t|\t" + text)
            text = input("sample text (qq for escape): ")