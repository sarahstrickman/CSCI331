"""
This file has all functions relating to training the data.
"""
from dataclasses import dataclass
import re

'''
to keep track of each example
'''


@dataclass
class trainExample:
    lang: str
    text: str


'''
open a file. take all the things in the file and make them into trainExample objects
'''
def readFile(filename: str):
    examples = []
    try:
        fp = open(filename)
        for line in fp:
            l = line.split("|")
            examples.append(trainExample(l[0], l[1]))
            pass
        fp.close()
        return examples
    except:
        print("Error: invalid file or file format.")


'''
train the data
'''
def train(examples: list[trainExample]):
    print(examples)
    pass


def hasHET(sample):
    return " het " in sample.lower(), "nl"

def hasNAAR(sample):
    return " naar " in sample.lower(), "nl"

def hasDAT(sample):
    return " dat " in sample.lower(), "nl"

def hasHEEFT(sample):
    return " heeft " in sample.lower(), "nl"

def hasARE(sample):
    return " are " in sample.lower(), "en"

def hasZIJN(sample):
    return " zijn " in sample.lower(), "nl"

def hasNIET(sample):
    return " niet " in sample.lower(), "nl"

def hasA(sample):
    # it has to be a lowercase a. (case sensitive)
    return " a " in sample, "en"

def hasBE(sample):
    return " be " in sample.lower(), "en"

def hasDE(sample):
    return " de " in sample.lower(), "en"

def hasIJCons(sample):
    return re.match("ij[b-df-hj-np-tv-z]", sample.lower()) is not None, "nl"

def hasUmlaut(sample):
    return re.match("[ÄäËëÏïÖöÜüŸÿ]", sample) is not None, "nl"

def hasConsDE(sample):
    return re.match("[b-df-hj-np-tv-z]de ", sample.lower()) is not None, "nl"

def hasVowECons(sample):
    return re.match("[aiou]e[b-df-hj-np-tv-z]", sample.lower()) is not None, "nl"

def has2VowCons(sample):
    return (re.match("aa[b-df-hj-np-tv-z]", sample.lower()) is not None) or \
           (re.match("ee[b-df-hj-np-tv-z]", sample.lower()) is not None) or \
           (re.match("ii[b-df-hj-np-tv-z]", sample.lower()) is not None) or \
           (re.match("oo[b-df-hj-np-tv-z]", sample.lower()) is not None) or \
           (re.match("uu[b-df-hj-np-tv-z]", sample.lower()) is not None), "nl"

def hasIJ(sample):
    return "ij" in sample.lower(), "nl"

def avgLen4(sample):
    txt = sample.replace("."," ")
    txt = sample.replace(",", " ")
    txt = txt.split(" ")
    length = len(txt)
    sum = 0
    for item in txt:
        sum += len(item)
    avg = sum / length
    return avg >= 4, "nl"



































