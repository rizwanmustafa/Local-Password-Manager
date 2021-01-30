import hashlib


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


def GetBoolInput(printString: str) -> bool:
    return GetNumberInput(printString, 0, 1).__bool__()
