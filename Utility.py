# Prints a prompt and validates the user input
# If the input is valid, it is returned else the user is asked for valid input two more times and then the program exits
def GetNumberInput(printString: str, minLimit: int = None, maxLimit: int = None) -> int:
    userTries = 0
    while True:
        userInput = input(printString + ": ").strip()
        if userInput.isdigit():
            userInput = int(userInput)
            if (minLimit == None or userInput >= minLimit) and (maxLimit == None or userInput <= maxLimit):
                return int(userInput)
            else:
                print("Please input a valid option!\n")
        else:
            print("Please input a valid option!\n")
        userTries += 1
        if userTries >= 3:
            print()
            exit()

# A special case of GetNumberInput where only bool input in the form of binary is accepted
def GetBoolInput(printString: str) -> bool:
    return GetNumberInput(printString, 0, 1).__bool__()