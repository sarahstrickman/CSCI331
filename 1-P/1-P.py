"""
The submission for homework 1-P.

You will be given two words (strings) and a dictionary of legal 
English words.

At each step, you can change any single letter in the word to any 
other letter, provided that the result is a word in the dictionary. 
Print the shortest list of words that connects the two given words 
in this way.

Implementation of the queue was from CSCI 141.

CSCI.331.02         (1:00pm section)
Sarah Strickman     sxs4599
"""


from Queue import *


'''
create the dictionary of words from a file.

precondition : there are no empty words.
return : the word dictionary
'''
def makeDictionary(filename):
    words = dict()
    file = open(filename)
    for line in file:
        word = line.strip()
        for i in range(0, len(word)):
            redacted = word[:i] + "_" + word[i+1:]
            if redacted in words:
                words[redacted] += [word]
            else:
                words[redacted] = [word]
    return words


'''
Perform BFS on the dictionary or words.

return : -1 if no path was able to be found
return : a list of the path, if a valid path was found
'''
def processWords(start, end, wordDict):
    currWord = ""
    queue = make_empty_queue()
    visited = set()
    pred = dict()

    enqueue(queue, start)
    pred[start] = None

    while not is_empty(queue):
        currWord = dequeue(queue)
        visited.add(currWord)
        for i in range(0,len(currWord)):
            redacted = currWord[:i] + "_" + currWord[i+1:]
            for entry in wordDict[redacted]:
                if entry not in pred.keys():
                    enqueue(queue, entry)
                    pred[entry] = currWord
    
    fl = []
    w = end
    if end not in pred:
        return -1
    while w != None:
        fl = [w] + fl
        w = pred[w]
    return fl


def main():
    wordDict = makeDictionary("exampleWords.txt")
    start = input("input a starting word: ")
    target = input("input a target word: ")
    lst = processWords(start, target, wordDict)
    if lst == -1:
        print("no path was found")
    else:
        for item in lst:
            print(item)
        print("total length :", len(lst))


main()