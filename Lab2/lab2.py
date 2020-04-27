
from dataclasses import dataclass
from typing import Union
import sys
import pickle

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
        say = "say = " + str(lab2Ada.getSay(self))
        nums = "YEN/YNL/NEN/NNL = " + str(len(self.yesEN)) + "/" + str(len(self.yesNL)) + "/" + str(len(self.noEN)) + "/" + str(len(self.noNL))
        return "(" + feat + ", " + ym + ", " + nm + ", " + say + ", " + nums + ")"
    def freeze(self):
        self.yesEN = frozenset(self.yesEN)
        self.yesNL = frozenset(self.yesNL)
        self.noEN = frozenset(self.noEN)
        self.noNL = frozenset(self.noNL)
        self.frozen = True

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


def exportDataStruct(data, filename):
    outfile = open(filename, 'wb')
    pickle.dump(data, outfile)
    outfile.close()

def importDataStruct(filename):
    infile = open(filename, 'rb')
    new_dict = pickle.load(infile)
    infile.close()
    return new_dict

'''
There are 2 ways to run the program:

1.  train <examples> <hypothesisOut> <learning-type> should read in labeled examples and perform some sort of training.
        - <examples> is a file containing labeled examples.
        - <hypothesisOut> specifies the file name to write your model to.
        - <learning-type> specifies the type of learning algorithm you will run, it is either "dt" or "ada". 
        You should use (well-documented) constants in the code to control additional learning parameters 
        like max tree depth, number of stumps, etc.

2.  predict <hypothesis> <file> Your program should classify each line as either English or 
Dutch using the specified model. Note that this must not do any training, but should take a model and make a 
prediction about the input. For each input example, your program should simply print its predicted label on a 
newline. It should not print anything else.
        - <hypothesis> is a trained decision tree or ensemble created by your train program
        - <file> is a file containing lines of 15 word sentence fragments in either English or Dutch. For example.
'''
if __name__ == "__main__":

    import lab2DT
    import lab2Ada

    if len(sys.argv) == 5:
        # run training
        examples = sys.argv[1]
        hypotOut = sys.argv[2]
        learnType = sys.argv[3]

        if learnType == "dt":
            tree = lab2DT.trainDT(examples)
            exportDataStruct(tree, hypotOut)
        else:
            forest = lab2Ada.trainAda(examples)
            exportDataStruct(forest, hypotOut)

    elif len(sys.argv) == 4:
        hypot = sys.argv[2]
        tree = importDataStruct(hypot)
        file = sys.argv[3]

        # run DT or ada prediction accordingly
        if isinstance(tree, treeNode):
            lab2DT.predictFile(tree, file)
        else:
            lab2Ada.predictFile(tree, file)
    else:
        print("Usage:\n"
              "train <examples> <hypothesisOut> <learning-type>\n"
              "predict <hypothesis> <file>")
