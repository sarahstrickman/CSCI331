**Homework 2-P**

2-P.py : Implements a random-restart hill climbing algorithm that solves the Countdown Numbers Game.

I have also included various examples of inputs.  These are located in input-*n*.txt, where n is substituted by a number.  The corresponding outputs for the files is located in output-*n*.txt.  Runs that are done with the same input but different targets are located in the same file.

input-1.txt is the example input from the assignment website.

----

The program is run with:

` python3 2-P.py input-file [target] [time-limit]`

target will default to a randomly generated 4-digit number if left unspecified.

time-limit will be specified in seconds. It can be a float or an int. If there is no time limit specified, the running time limit will default to 1 hour.