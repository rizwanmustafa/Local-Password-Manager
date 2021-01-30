from DatabaseManager import DatabaseManager
from random import randint
from tkinter import Tk
from getpass import getpass
from Utility import GetNumberInput, GetBoolInput


def PrintLoginMenu():
    global databaseManager

    while True:
        print("\n" + "-"*60)
        print("1 : Login")
        print("2 : Reset Masterpassword")
        print("3 : Setup / Reset Password Manager")
        print("4 : Exit")
        print("-"*60 + "\n")

        userChoice = GetNumberInput("Please input your choice", 1, 4)

        if userChoice == 1:
            password = getpass("Enter Masterpassword: ")
            databaseManager = DatabaseManager("PassMan", password, "passwordDB")  # nopep8
            break

        elif userChoice != 4:
            username = input("Enter MySQL Admin Username: ")
            password = getpass("Enter MySQL Admin Password: ")

            databaseManager = DatabaseManager(username, password)
            if userChoice == 2:
                databaseManager.ResetPass()
            else:
                databaseManager.SetupDB()

        else:
            exit()


def PrintMenu():
    global databaseManager

    while True:
        print("\n" + "-"*60)
        print("1 : Generate a new strong password")  # Done
        print("2 : Store a new password")  # Done
        print("3 : Print all passwords")  # Done
        print("4 : Retrieve passwords connected to a specific email")
        print("5 : Retrieve passwords with a specific title")
        print("6 : Modify a password's properties")
        print("7 : Exit")  # Proudly Done
        print("-"*60 + "\n")

        userChoice = GetNumberInput("Please input your choice", 1, 7)
        print()
        if userChoice == 1:
            GeneratePassword()
        elif userChoice == 2:
            databaseManager.StorePassword()
        elif userChoice == 3:
            passwords = databaseManager.GetAllPasswords()
            for x in passwords:
                PrintPasswordDetails(x)
        elif userChoice == 4:
            passwords = databaseManager.GetPasswordFromEmail()
            for x in passwords:
                PrintPasswordDetails(x)
        elif userChoice == 5:
            passwords = databaseManager.GetPasswordFromTitle()
            for x in passwords:
                PrintPasswordDetails(x)
        elif userChoice == 6:
            databaseManager.ModifyPasswordProperties()
        elif userChoice == 7:
            exit()


def GeneratePassword() -> str:
    passLen = GetNumberInput("Password Length (Min Length: 8)", 8)
    passLow = GetBoolInput("Lower Case Letters (0/1)")
    passCap = GetBoolInput("Capital Case Letters (0/1)")
    passNum = GetBoolInput("Numbers (0/1)")
    passSym = GetBoolInput("Symbols (0/1)")
    print("\nGenerating your password...\n")

    protocolNum = 0
    if passLow:
        protocolNum += 1
    if passCap:
        protocolNum += 1
    if passNum:
        protocolNum += 1
    if passSym:
        protocolNum += 1

    if protocolNum == 0:
        print("Please choose valid options for generating a password\n")
        return GeneratePassword()

    genPass = ""
    containsLow = containsCap = containsNum = containsSym = False
    symbols = ['!', '@', '#', '$', '%', '&', '*', '(', ')', '-', '_', '=', '+', '[', ']', '/', ';', ':', ',', '.', '"', "'", '?']  # nopep8

    while True:
        while len(genPass) != passLen:
            randomNum = randint(0, 3)

            if passLow and randomNum == 0:
                genPass += chr(randint(97, 122))
            elif passCap and randomNum == 1:
                genPass += chr(randint(65, 90))
            elif passNum and randomNum == 2:
                genPass += str(randint(0, 9))
            elif passSym and randomNum == 3:
                genPass += symbols[randint(0, len(symbols)-1)]

        for x in genPass:
            if x.isalpha():
                if x.isupper():
                    containsCap = True
                elif x.islower():
                    containsLow = True
            elif x.isnumeric():
                containsNum = True
            elif x in symbols:
                containsSym = True

        if containsLow == passLow and containsCap == passCap and containsNum == passNum and containsSym == passSym:
            print("Your generated password is: {0}".format(genPass))
            CopyTextToClipBoard(genPass)
            print("It has been copied to your clipboard!\n")
            return
        else:
            genPass = ""


def CopyTextToClipBoard(copyString: str):
    tk = Tk()
    tk.withdraw()
    tk.clipboard_clear()
    tk.clipboard_append(copyString)
    tk.update()


def PrintPasswordDetails(passDetails):
    print("\n" + "-"*60)
    print("ID: {0}\nTitle: {1}\nUsername: {2}\nEmail Address: {3}\nPassword: {4}".format(passDetails[0], passDetails[1], passDetails[2], passDetails[3], passDetails[4]))  # nopep8
    print("-"*60 + "\n")


#------------------------------------------------------------#
databaseManager = None

print("-"*60)
print("Welcome to Password Manager by Rizwan Mustafa!")
print("-"*60)

PrintLoginMenu()
PrintMenu()

#------------------------------------------------------------#
