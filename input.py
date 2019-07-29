import output

def isInt(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

def getInput(prompt):
    return input("<" + prompt + "> ")

def getInt(prompt, lowerBound, upperBound):
    choice = getInput(prompt)
    while not isInt(choice) or int(choice) < lowerBound or int(choice) > upperBound:
        output.say("Please enter an integer between 1 and " + str(upperBound) + ".")
        choice = getInput(prompt)
    return int(choice)

# Get input from a list of options. Special logic for how to display the option can be passed, and if necessary, a function can be passed that returns whether an option is valid.
def inputFromOptions(prompt, options, mapOption = lambda option: str(option), condition = lambda option: True, warning = ""):
    if len(options) == 0:
        return None
    output.outputList(options, mapOption)
    choice = getInput(prompt)
    while not isInt(choice) or int(choice) > len(options) or int(choice) < 1 or not condition(options[int(choice) - 1]):
        if not isInt(choice) or int(choice) > len(options) or int(choice) < 1:
            output.say("Please enter an integer between 1 and " + str(len(options)) + ".")
        else:
            output.say(warning)
        choice = getInput(prompt)
    return options[int(choice) - 1]

def yesNo():
    while True:
        choice = getInput("yes/no").lower()
        if choice == "yes" or choice == "y":
            return True
        elif choice == "no" or choice == "n":
            return False
        else:
            output.say("Please enter yes or no.")
