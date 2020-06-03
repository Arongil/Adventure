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
