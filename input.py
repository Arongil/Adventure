from pynput import keyboard
import globals
import output

# Automatically press <enter> after the user presses a key. That way they can type "12212" instead of "1 <enter> 2 <enter> 2 <enter> 1 <enter 2"
controller = keyboard.Controller()
def instant_input():
    return globals.get_player().settings["instant input"]
# Only instant-type for characters in [1,2,3,4,5,6,7,8,9]
instant_keys = []
for i in range(10):
    instant_keys.append(keyboard.KeyCode(char=str(i)))
def on_release(key):
    if instant_input() and key in instant_keys:
        controller.press(keyboard.Key.enter)
listener = keyboard.Listener(on_release=on_release)
listener.start()
def close():
    listener.stop()

def isInt(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

def getInput(prompt):
    return input("<" + prompt + "> ")

def pause():
    output.separate()
    getInput("...")

def getInt(prompt, lowerBound, upperBound):
    choice = getInput(prompt)
    while not isInt(choice) or int(choice) < lowerBound or int(choice) > upperBound:
        output.say("Please enter an integer between 1 and " + str(upperBound) + ".")
        choice = getInput(prompt)
    return int(choice)

# Get input from a list of options. Special logic for how to display the option can be passed, and if necessary, a function can be passed that returns whether an option is valid.
def inputFromOptions(prompt, options, mapOption = lambda option: str(option), condition = lambda option: True, warning = "", debug=False):
    if len(options) == 0:
        return None
    output.outputList(options, mapOption)
    choice = getInput(prompt)
    while not isInt(choice) or int(choice) > len(options) or int(choice) < 1 or not condition(options[int(choice) - 1]):
        if debug and choice == "debug":
            return "debug"
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
