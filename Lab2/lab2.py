
import sys
import numpy
import pandas
from sklearn import *
from lab2training import *


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
def main():
    if len(sys.argv) == 4:
        # run training
        pass
    elif len(sys.argv) == 3:
        # run prediction
        pass
    else:
        print("Usage:\n"
              "train <examples> <hypothesisOut> <learning-type>\n"
              "predict <hypothesis> <file>")
    pass
