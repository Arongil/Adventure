# cut off print after some point, but never over a word
def _printNoCutoff(string, prefix, cutoff):
    lines = []
    words = string.split(" ")
    curLength = 0
    lineStart = 0
    for i, word in enumerate(words):
        l = len(str(word)) + 1 # add 1 for the space
        curLength += l
        if curLength > cutoff:
            lines.append(" ".join(words[lineStart:i]))
            lineStart = i
            curLength = l
    lines.append(" ".join(words[lineStart:]))
    for line in lines:
        print(prefix + line)

def printNoCutoff(string, prefix="", cutoff=100):
    if prefix == "\t":
        cutoff -= 8
    blocks = str(string).split("\n")
    for block in blocks:
        _printNoCutoff(block, prefix, cutoff)

def separate():
    print("")

def say(string):
    printNoCutoff(string)

def declare(string):
    printNoCutoff(string, prefix="\t")

def exclaim(string):
    separate()
    printNoCutoff(string, prefix="\t")

def bellow(string):
    separate()
    printNoCutoff(string, prefix="\t")
    separate()

def proclaim(string):
    separate()
    printNoCutoff(string)

def bar():
    print("_" * 100)
    print("")

powers = [10**i for i in range(0, 10)]
invPowers = [10**(-i) for i in range(0, 10)]
def formatNumber(n, digits=1):
    if abs(int(n) - n) < invPowers[digits]:
        return str(int(n))
    return str(int(n * powers[digits]) / powers[digits])

# If necessary, a map between options and strings can be passed. By default, this map is just str.
def outputList(options, mapOption = lambda option: str(option)):
    for i, option in enumerate(options):
        say("  " + str(i + 1) + ": " + mapOption(option))
