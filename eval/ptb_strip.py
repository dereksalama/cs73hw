import re

ptbFile = open("/Users/jakeleichtling/Desktop/ptb/combined-small.pos", "r")
combinedOutputFile = open("/Users/jakeleichtling/Desktop/ptb/combined-small.txt", "w")
transFile = open("/Users/jakeleichtling/Desktop/ptb/trans-small.txt", "w")
emisFile = open("/Users/jakeleichtling/Desktop/ptb/emis-small.txt", "w")

stateSet = set()
obsSet = set()

for line in ptbFile:
    # Skip empty lines and =====...
    if line is None:
        continue

    line = line.replace("[", "")
    line = line.replace("]", "")
    line = line.lstrip()
    line = line.rstrip()

    if line.replace("=", "") is "" and line is not "":
        combinedOutputFile.write("\n")
        continue

    tokens = line.split()
    tokenPairs = map(lambda token: re.split(r"(?<!\\)/", token, 1), tokens)

    for tokenPair in tokenPairs:
        if tokenPair[0] != tokenPair[1] and re.sub("[^a-zA-Z0-9]", "", tokenPair[0]) != "":
            combinedOutputFile.write(tokenPair[0] + " ")

            states = re.split("\|", tokenPair[1])
            for state in states:
                stateSet.add(state)

            obsSet.add(tokenPair[0])

for fromState in stateSet:
    for toState in stateSet:
        transFile.write(fromState + " " + toState + "\n")

    for obs in obsSet:
        emisFile.write(fromState + " " + obs + "\n")

combinedOutputFile.close()
transFile.close()
emisFile.close()
