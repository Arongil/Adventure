def say(string):
    print(string)

def declare(string):
    print("\t" + string)

def exclaim(string):
    print("\n\t" + string)

def bellow(string):
    print("\n\t" + string + "\n")

def proclaim(string):
    print("\n" + string)

def bar():
    print("_" * 75)
    print("")

def separate():
    print("")

def formatNumber(n, digits=1):
    integerDiff = abs(n) - int(abs(n))
    if integerDiff < 10**(-digits):
        return str(int(n))
    else:
        return str(round(n, digits))

# If necessary, a map between options and strings can be passed. By default, this map is just str.
def outputList(options, mapOption = lambda option: str(option)):
    for i, option in enumerate(options):
        say("  " + str(i + 1) + ": " + mapOption(option))
