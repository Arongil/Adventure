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

def formatNumber(n):
    integerDiff = abs(n) - int(abs(n))
    if integerDiff < 0.1:
        return str(int(n))
    else:
        return str(round(n, 1))

# If necessary, a map between options and strings can be passed. By default, this map is just str.
def outputList(options, mapOption = lambda option: str(option)):
    for i in range(len(options)):
        say("  " + str(i + 1) + ": " + mapOption(options[i]))

def help():
    output("Welcome to Adventure!")
    output("Type 'help' to bring up this message again.")
    output("Commands:", False, True)
    output("help", True)
    output("inventory", True)
    output("town", True)
    output("scavenge", True)
    output("rest", True)
    output("use", True)
    output("Beware of monsters... they prowl the shadows.", False, True)
