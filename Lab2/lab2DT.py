"""
This file has all functions relating to training the data and decision trees.

maximum tree depth is 14. this is because I have 14 attributes
"""
import os
from dataclasses import dataclass
import re
import pickle
from typing import Union


MAX_DEPTH = 20

'''
to keep track of each example
'''
@dataclass
class textEntity:
    def __init__(self,
                 lang: Union[None, str] = None,
                 text: str = ""):
        self.lang = lang
        self.text = text

@dataclass
class treeNode:
    def __init__(self,
                 dataset: list = [],                # list of textEntities
                 feature: Union[None, str] = None,  # leaf nodes will not have a feature associated with them.
                 majority: str = "",
                 yes: Union[None, 'treeNode'] = None,
                 no: Union[None, 'treeNode'] = None):
        self.dataset = dataset
        self.feature = feature
        self.majority = majority
        self.yes = yes
        self.no = no

'''
test how accurate this program is.
This program expects a file full of samples that are in the same language

    lang        : the language expected of the samples
    treefile    : the file containing the serialized tree you are using to predict
    samplefile  : the file containign text samples to test

prints all incorrect samples, then prints the accuracy as a percentage.
returns accuracy (as a float)
'''
def testAccuracyDT(lang, tree, samplefile):
    numIncorrect = 0
    fp = open(samplefile, encoding="utf-8")
    samples = fp.readlines()
    totalSamples = len(samples)
    for sample in samples:
        if predictDT(sample, tree) != lang:
            print(str(numIncorrect) + ".\t" +sample.strip())
            numIncorrect += 1
    accuracy = (totalSamples - numIncorrect) / totalSamples
    print("---------\naccuracy:\t" + str(accuracy * 100) + "%")
    fp.close()
    return accuracy

def predictFile(filename):
    for line in open(filename):
        print(predictDT(line))

'''
predict if a sample is english or dutch, given a sample
'''
def predictDT(sample, tree):
    sampleText = textEntity(lang=None, text=sample)
    while tree is not None:
        if (tree.feature == None) or (tree.yes == None and tree.no == None):    # you're at a leaf node
            return tree.majority
        else:
            has = hasFeature(sampleText, tree.feature)    # does sample have feature?
            if has:
                tree = tree.yes
            else:
                tree = tree.no
    return "en"

'''
given a filename, return a tree
'''
def trainDT(filename):
    samples = readFile(filename)
    tree = makeTree(samples)
    return tree

'''
open a file. take all the things in the file and make them into textEntity objects
'''
def readFile(filename: str):
    examples = []
    try:
        fp = open(filename, encoding="utf-8")
        for line in fp:
            l = line.strip().split("|")
            examples.append(textEntity(lang = l[0], text = l[1]))
            pass
        fp.close()
        return examples
    except:
        print("Error: invalid filename or file format.")
        exit()

'''
make the tree.

leaf nodes will not have a feature associated with them.
'''
def makeTree(dataset, featurelist=None, currdepth = 0):
    if featurelist is None:
        featurelist = {"hasHET",
                       "hasAT",
                       "hasVAN",
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
    # if no data to analyze, return node with no feature. just majority
    if len(dataset) == 0:
        return treeNode(dataset=dataset, majority="en", feature=None,yes=None,no=None)

    # if you have run out of features, return a treenode with the majority language
    elif len(featurelist) == 0 or currdepth >= MAX_DEPTH:
        numEn = 0
        numNL = 0
        for item in dataset:
            if item.lang == "en":
                numEn += 1
            else:
                numNL += 1
        if numEn >= numNL:
            return treeNode(dataset=dataset, majority="en", feature=None, yes=None, no=None)
        return treeNode(dataset=dataset, majority="nl", feature=None, yes=None, no=None)

    # calculate gini index for all features in featurelist.
    # keep track of the lowest one
    lowestGini = 100.00
    lowestFeature = ""
    for feature in featurelist:
        tempGini = featureGini(feature, dataset)
        if tempGini < lowestGini:
            lowestGini = tempGini
            lowestFeature = feature

    curr = treeNode(dataset=dataset, majority="en", feature=lowestFeature, yes=None, no=None)

    # split dataset on feature with lowest gini
    yesList, noList = featureSplit(lowestFeature, dataset)

    tempdataset = featurelist.remove(lowestFeature)
    # for hasFeature and NOHasFeature, check remaining ginis. create tree accordingly
    curr.yes = makeTree(yesList, tempdataset, currdepth + 1)
    curr.no = makeTree(noList, tempdataset, currdepth + 1)
    featurelist.add(lowestFeature)

    return curr

'''
split a dataset on a feature.

return 2 lists: 1 HAS feature, 2 DOESN'T have feature
'''
def featureSplit(feature, dataset):
    yes = []
    no = []
    for item in dataset:
        if hasFeature(item, feature):
            yes.append(item)
        else:
            no.append(item)
    return yes, no

'''
split a dataset on a given feature
'''
def split(feature, dataset):
    yes = []
    no = []
    for item in dataset:
        if hasFeature(item, feature):
            yes.append(item)
        else:
            no.append(item)
    return yes, no

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
    pEN = numEN / float(tot)
    pNL = numNL / float(tot)
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
        if hasFeature(item, feature):
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
sample is a textEntity.
'''
def hasFeature(sample, feature):
    if feature == "hasHET":
        return hasHET(sample)
    elif feature == "hasVAN":
        return hasVAN(sample)
    elif feature == "hasAT":
        return hasAT(sample)
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

'''
functions for the features
'''
def hasHET(sample):
    return " het " in sample.text.lower()
def hasAT(sample):
    return " at " in sample.text.lower()
def hasVAN(sample):
    return " van " in sample.text.lower()
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


def exportTree(data, filename):
    outfile = open(filename, 'wb')
    pickle.dump(data, outfile)
    outfile.close()

def importTree(filename):
    infile = open(filename, 'rb')
    new_dict = pickle.load(infile)
    infile.close()
    return new_dict


if __name__ == "__main__":
    tree = None
    o = input("load file name: ")
    if len(o) > 0:
        o = "knowledge_base/" + o
        tree = importTree(o)
    else:
        print("re-training...")
        filename = "training_data/train_master.dat" #input("filename: ")
        tree = trainDT(filename)

    s = input("save file name: ")
    if len(s) >0:
        s = "knowledge_base/" + s
        exportTree(tree, s)

    t = input("test file name: ")
    l = input("test lang: ")
    if len(t) > 0:
        testAccuracyDT(l, tree, t)
    else:
        text = input("sample text (qq for escape): ")
        while text != "qq":
            lang = predictDT(text, tree)
            print(lang + "\t|\t"+text)
            text = input("sample text (qq for escape): ")

































