
import sys
import lab2DT
import lab2Ada


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
        examples = sys.argv[1]
        hypotOut = sys.argv[2]
        learnType = sys.argv[3]

        if learnType == "dt":
            tree = lab2DT.trainDT(examples)
            lab2DT.exportTree(tree, hypotOut)
        else:
            forest = lab2Ada.trainAda(examples)
            lab2Ada.exportForest(forest, hypotOut)
            print("i havent implemented that because im stupid :/")
            exit(0)

    elif len(sys.argv) == 3:
        hypot = sys.argv[1]
        tree = lab2DT.importTree(hypot)
        file = sys.argv[2]

        # run DT or ada prediction accordingly
        if isinstance(tree, lab2DT.treeNode):
            lab2DT.predictFile(file)
        else:
            lab2Ada.predictFile(file)
    else:
        print("Usage:\n"
              "train <examples> <hypothesisOut> <learning-type>\n"
              "predict <hypothesis> <file>")
