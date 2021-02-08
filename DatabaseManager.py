from Utility import GetNumberInput
from getpass import getpass
import mysql.connector


class DatabaseManager:

    db = None
    mycursor = None

    def __init__(self, username: str = None, password: str = None, database: str = None) -> None:
        if username != None and password != None:
            self.ConnectToMySQL(username, password, database)

    def ConnectToMySQL(self, username: str, password: str, database: str = None) -> bool:

        print("Attempting to connect to local MySQL server...")
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user=username,
                passwd=str(password))
            self.mycursor = self.db.cursor()

            print("Connection established successfully!\n")

            if database != None:
                self.mycursor.execute("USE {0}".format(database))

            return True

        except mysql.connector.Error as e:
            self.PrintException(e)
            exit()

    def StorePassword(self) -> str:
        passTitle = input("Enter Password Title (Required): ")
        passUser = input("Enter Username: ")
        passEmail = input("Enter Email Address: ")
        password = getpass("Enter Password (Required): ")
        print()


        try:
            print("Inserting password...")
            self.mycursor.execute("INSERT INTO passwords(title,userName,emailAddr,password) VALUES(%s, %s, %s, %s);", (passTitle, passUser, passEmail, password))  # nopep8
            self.db.commit()
            print("Password inserted sucessfully!")

        except mysql.connector.Error as e:
            self.PrintException(e)

    def GetAllPasswords(self):

        try:
            self.mycursor.execute("SELECT * FROM passwords")
            return self.mycursor.fetchall()

        except mysql.connector.Error as e:
            self.PrintException(e)

    def GetPasswordFromTitle(self):
        passTitle = input("Enter Title: ")
        try:
            self.mycursor.execute("SELECT * FROM passwords WHERE title LIKE '{0}'".format(passTitle))  # nopep8
            return self.mycursor.fetchall()

        except mysql.connector.Error as e:
            self.PrintException(e)

    def GetPasswordFromEmail(self):
        passEmail = input("Enter Email Address: ")

        try:
            self.mycursor.execute("SELECT * FROM passwords WHERE emailAddr LIKE '{0}'".format(passEmail))  # nopep8
            return self.mycursor.fetchall()

        except mysql.connector.Error as e:
            self.PrintException(e)

    def ModifyPasswordProperties(self):
        passID = GetNumberInput("Enter Password ID: ", 1)
        passTitle = input("Enter Password Title (Required): ")
        passUser = input("Enter Username: ")
        passEmail = input("Enter Email Address: ")
        password = getpass("Enter Password (Required): ")
        print("Updating password details...")

        try:
            self.mycursor.execute("UPDATE passwords SET title = %s, userName = %s, emailAddr = %s, password = %s WHERE id = %s", (passTitle, passUser, passEmail, password, passID))  # nopep8
            self.db.commit()
            print("Password details updated successfully!\n")

        except mysql.connector.Error as e:
            self.PrintException(e)

    # Sets up a new database for storing passwords locally
    def SetupDB(self):
        try:
            # Create a new database called passwordDB
            print("Attempting to create a new database called 'passwordDB'...")
            self.mycursor.execute("CREATE DATABASE IF NOT EXISTS passwordDB;")
            self.mycursor.execute("USE passwordDB;")
            # Later only drop table if it is not appropriate
            self.mycursor.execute("DROP TABLE IF EXISTS passwords;")
            self.mycursor.execute("""CREATE TABLE passwords (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(30)  NOT NULL,
                userName VARCHAR(50),
                emailAddr VARCHAR(50),
                password VARCHAR(50) NOT NULl
                );""")
            print("Database created successfully")

            # Create a new user called PassMan or change its password anyways
            userPass = getpass("Enter Masterpassword: ")
            print("Attempting to create a new MySQL user called 'PassMan'...")
            self.mycursor.execute("""DROP USER IF EXISTS 'PassMan'@'localhost';""".format(userPass))  # nopep8
            self.mycursor.execute("""CREATE USER 'PassMan'@'localhost' IDENTIFIED BY "{0}";""".format(userPass))  # nopep8

            # Grant PassMan privileges over passwordDB
            print("Granting all privileges to 'PassMan' on 'passwords' in 'passwordDB';")
            self.mycursor.execute("GRANT ALL PRIVILEGES ON passwordDB.passwords TO 'PassMan'@'localhost';")  # nopep8
            self.mycursor.execute("FLUSH PRIVILEGES;")
            print("Successfully granted privileges!")

        except mysql.connector.Error as e:
            self.PrintException(e)

    # Resets masterpassword although the stored credentials must have administrative power
    def ResetPass(self):
        password = getpass("Enter new Masterpassword: ")
        print("Attempting to change master password...")

        try:
            self.mycursor.execute("""ALTER USER 'PassMan'@'localhost' IDENTIFIED BY "{0}";""".format(password))  # nopep8
            print("Password reset successfully!")

        except mysql.connector.Error as e:
            self.PrintException(e)

    # Prints MySQL Exception
    def PrintException(self, e: mysql.connector.Error):
        print("\n" + "-"*60)
        print("Error Number: " + str(e.errno))
        print("SQLSTATE: " + str(e.sqlstate))
        print("Error Message: " + str(e.msg))
        print("-"*60 + "\n")
