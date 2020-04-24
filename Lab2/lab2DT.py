"""
This file has all functions relating to training the data.
"""
from dataclasses import dataclass
import re
import math

'''
to keep track of each example
'''


@dataclass
class textEntity:
    lang: str
    text: str


'''
open a file. take all the things in the file and make them into textEntity objects
'''
def readFile(filename: str):
    examples = []
    try:
        fp = open(filename)
        for line in fp:
            l = line.split("|")
            examples.append(textEntity(lang = l[0], text = l[1]))
            pass
        fp.close()
        return examples
    except:
        print("Error: invalid file or file format.")


'''
train the data
'''
def train(examples: list[textEntity]):
    # textEntities = readFile(filename)
    #
    print(examples)
    pass


'''
find the gini index of a dataset.
find the gini impurity of the current node

gini = 1 - P(yes)^2 - P(no)^2
lower number = more pure
higher number = less pure (bad!)

tot : total number of entities
numEN : number of english entities
numNL : number of dutch entities
returns a float.  
'''
def currGini(tot, numEN, numNL):
    if tot == 0:
        return 0
    pEN = numEN / float(len(tot))
    pNL = numNL / float(len(tot))
    return 1.0 - (pEN ** 2.0) - (pNL ** 2.0)


'''
find gini impurity given an feature and a dataset. this is used for non-leaf nodes
this will return the gini impurity of the feature.

feature : the name of the feature we're checking for
dataset : list of entities
'''
def featureGini(feature, dataset):
    yesItems = []
    yesEN = 0   # has feature and is english
    yesNL = 0   # has feature and is dutch
    noItems = []
    noEN = 0    # doesn't have feature and is english
    noNL = 0    # doesn't have feature and is dutch

    for item in dataset:
        if hasFeature(item.text, feature):
            yesItems.append(item)
            if item.lang == "en":
                yesEN += 1
            elif item.lang == "nl":
                yesNL += 1
        else:
            noItems.append(item)
            if item.lang == "en":
                noEN += 1
            elif item.lang == "nl":
                noNL += 1

    # find gini impurity & weight of the left side
    yesGini = currGini(len(yesItems), yesEN, yesNL)
    yesWeighted = (len(yesItems) / len(dataset)) * yesGini

    # find gini impurity & weight of the right side
    noGini = currGini(len(noItems), noEN, noNL)
    noWeighted = (len(noItems) / len(dataset)) * noGini

    # compute weighted average
    return yesWeighted + noWeighted


'''
check if a feature is true for a given sample 
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
    else:
        print("invalid feature")
        return False


def hasHET(sample):
    return " het " in sample.lower()

def hasNAAR(sample):
    return " naar " in sample.lower()

def hasDAT(sample):
    return " dat " in sample.lower()

def hasHEEFT(sample):
    return " heeft " in sample.lower()

def hasARE(sample):
    return " are " in sample.lower()

def hasZIJN(sample):
    return " zijn " in sample.lower()

def hasNIET(sample):
    return " niet " in sample.lower()

def hasA(sample):
    # it has to be a lowercase a. (case sensitive)
    return " a " in sample

def hasBE(sample):
    return " be " in sample.lower()

def hasDE(sample):
    return " de " in sample.lower()

def hasIJCons(sample):
    return re.match("ij[b-df-hj-np-tv-z]", sample.lower()) is not None

def hasUmlaut(sample):
    return re.match("[ÄäËëÏïÖöÜüŸÿ]", sample) is not None

def hasConsDE(sample):
    return re.match("[b-df-hj-np-tv-z]de ", sample.lower()) is not None

def hasVowECons(sample):
    return re.match("[aiou]e[b-df-hj-np-tv-z]", sample.lower()) is not None

def has2VowCons(sample):
    return (re.match("aa[b-df-hj-np-tv-z]", sample.lower()) is not None) or \
           (re.match("ee[b-df-hj-np-tv-z]", sample.lower()) is not None) or \
           (re.match("ii[b-df-hj-np-tv-z]", sample.lower()) is not None) or \
           (re.match("oo[b-df-hj-np-tv-z]", sample.lower()) is not None) or \
           (re.match("uu[b-df-hj-np-tv-z]", sample.lower()) is not None)

def hasIJ(sample):
    return "ij" in sample.lower()

def avgLen4(sample):
    txt = sample.replace("."," ")
    txt = sample.replace(",", " ")
    txt = txt.split(" ")
    length = len(txt)
    summ = 0
    for item in txt:
        summ += len(item)
    avg = summ / length
    return avg >= 4



































