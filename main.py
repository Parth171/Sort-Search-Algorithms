'''
title: Superhero Search and Sort
author: Parth Sakpal
date-created: 10/12/2023
'''


# import libraries
import csv
import pathlib
import sqlite3
from tabulate import tabulate # Used to display the Superhero Information neatly to the User


# Creates the Database File
DATABASE_FILE = "superhero.db"


# Checks if this is the first time running the program
FIRST_RUN = True

# Checks to see if database file already exists
if (pathlib.Path.cwd() / DATABASE_FILE).exists():
    FIRST_RUN = False

CONNECTION = sqlite3.connect(DATABASE_FILE)
CURSOR = CONNECTION.cursor()

# Two Lists used to separate the DC and Marvel Data to individually sort each by the Superhero ID
MARVEL_DATA = []
DC_DATA = []


def menu():
    """
    Explains the program and presents a menu to the user for them to pick an action
    :return: int
    """

    print("""
    ___________________________________________________________________________________________________________________
    
    Welcome to the Recursive SUPER HERO SEARCH AND SORT!
    
    This program will allow you to search for a Superhero by using their SuperHero ID, view the sorted Superhero 
    database, and even add your own superhero to the Database! (Note: Please enter the ID accurately and exactly as it is meant to appear) 
    
    
    1. Search for SuperHero using their Superhero ID
    
    2. View Sorted Superhero Database 
    
    3. Add your own Superhero
    
    4. Exit the program
    ___________________________________________________________________________________________________________________
    """)

    # Error checks the input to see if it is a numeric value
    USER_INPUT = input("Select your choice: ")
    if USER_INPUT.isnumeric() is False:
        print("Enter a number value.")
        return menu()

    USER_INPUT = int(USER_INPUT)

    # Checks to see if the option selected is present in the menu
    if 5 > USER_INPUT > 0:
        return USER_INPUT
    else:
        print("Select an option from the menu")
        return menu()


def createDatabase():
    '''
    Create the superhero datbase
    :return: None
    '''

    global CONNECTION, CURSOR

    CURSOR.execute("""
        CREATE TABLE
            superhero (
                superhero_id,
                name,
                ID,
                align,
                eye,
                hair,
                alive,
                appearance,
                first_appearance,
                year,
                brand

            )
    ;""")


# Extract data from the csv
def getRawData(fileName):
    '''
    Gets the raw data from the Superhero CSV File
    :param fileName: CSV file
    :return: 2D Array
    '''


    DATA = []
    FILE = open(fileName)

    LINES = csv.reader(FILE)

    for line in LINES:
        DATA.append(line)

    TITLE = DATA.pop(0)


    for i in range(len(DATA)):
        if DATA[i][9].isnumeric():
            DATA[i][9] = int(DATA[i][9])

    return DATA, TITLE


def addData(LIST):
    """
    Adds the sorted Superhero list to the database
    :param LIST: List (Sorted by Superhero ID)
    :return: None
    """

    global CONNECTION, CURSOR

    for i in range(len(LIST)):
        CURSOR.execute("""
            INSERT INTO
                superhero
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )

        ;""", LIST[i])

        CONNECTION.commit()

def quickSort(LIST, FIRST_INDEX, LAST_INDEX):
    """
    Quick Sorts the data (recursively)
    :param LIST: List (Raw Data)
    :param FIRST_INDEX: int
    :param LAST_INDEX: int
    :return: List (sorted)
    """

    if FIRST_INDEX < LAST_INDEX:
        PIVOT_VALUE = LIST[FIRST_INDEX]

        LEFT_INDEX = FIRST_INDEX + 1
        RIGHT_INDEX = LAST_INDEX

        DONE = False


        while not DONE:
            while LEFT_INDEX <= RIGHT_INDEX and LIST[LEFT_INDEX] <= PIVOT_VALUE:
                LEFT_INDEX += 1
            while RIGHT_INDEX >= LEFT_INDEX and LIST[RIGHT_INDEX] >= PIVOT_VALUE:
                RIGHT_INDEX -= 1

            if RIGHT_INDEX < LEFT_INDEX:
                DONE = True

            else:
                TEMP = LIST[LEFT_INDEX]

                LIST[LEFT_INDEX] = LIST[RIGHT_INDEX]

                LIST[RIGHT_INDEX] = TEMP

        TEMP = LIST[FIRST_INDEX]
        LIST[FIRST_INDEX] = LIST[RIGHT_INDEX]
        LIST[RIGHT_INDEX] = TEMP

        quickSort(LIST, FIRST_INDEX, RIGHT_INDEX - 1)
        quickSort(LIST, RIGHT_INDEX + 1, LAST_INDEX)

    return LIST


def userInput(DATA):
    '''
    Gets the user input for Superhero ID and error checks
    :param DATA: 2D array
    :return: Str (Superhero ID)
    '''


    INPUT = input(str("What is the Superhero ID: "))

    ID = []

    # Error checks to see if the inputted Superhero ID is in the database
    for i in range(len(DATA)):
            ID.append(DATA[i][0])


    if INPUT not in ID:
        print("INVALID ENTRY")
        return userInput(DATA)

    else:
        return INPUT



def binarySearch(LIST, VALUE):
    """
    Recursive Binary Searches the Data to find the index of the Value
    :param LIST: list
    :param VALUE: str
    :return: index of the value
    """

    MIDPOINT = len(LIST) // 2

    # Base case
    if LIST[MIDPOINT][0][1:] == VALUE[1:]:
        return MIDPOINT, LIST
    else:
        # recursive process

        if VALUE[1:] < LIST[MIDPOINT][0][1:]:
            return binarySearch(LIST[:MIDPOINT], VALUE)

        else:
            return binarySearch(LIST[MIDPOINT + 1:], VALUE)


def getData():
    """
    Get the data from the database (this is to ensure that if the user has added a new member, the member can be displayed when searching)
    :return: list - from the database
    """

    global CONNECTION, CURSOR

    DATA = CURSOR.execute("""
        SELECT
            *
        FROM 
            superhero
        
    ;""").fetchall()

    return DATA

def addSuperHero():
    """
    An option to add a superhero to the database
    :return: none
    """

    global CONNECTION, CURSOR

    print("""
           Please enter the values for the following fields.
           Filling out the Superhero ID, name, and Brand fields are mandatory. Other fields may be left blank.
           """)

    USER_DATA = []

    USER_DATA.append(input("Superhero ID: "))
    USER_DATA.append(input("name: "))
    USER_DATA.append(input("ID (Public Identity or Secret Identity): "))
    USER_DATA.append(input("ALIGN (Good, Bad, Neural): "))
    USER_DATA.append(input("EYE: "))
    USER_DATA.append(input("HAIR: "))
    USER_DATA.append(input("ALIVE: "))
    USER_DATA.append(input("APPEARANCES: "))
    USER_DATA.append(input("FIRST APPEARANCE (YEAR, MONTH): "))
    USER_DATA.append(input("YEAR: "))
    USER_DATA.append(input("Brand (Marvel or DC): "))

    # Checks to see is all the required data has been inputted
    if USER_DATA[0] == "" or USER_DATA[1] == "" or USER_DATA[10] == "":
        print("You have not entered all the required data")
        return addSuperHero()


    CURSOR.execute("""
        INSERT INTO
            superhero
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        
        )
    ;""", USER_DATA)

    CONNECTION.commit()


if __name__ == "__main__":

    RAW_DATA, TITLES = getRawData("comicBookCharData_mixed.csv")

    if FIRST_RUN:
        createDatabase()

        for i in range(len(RAW_DATA)):
            if RAW_DATA[i][0][0] == "M":
                MARVEL_DATA.append(RAW_DATA[i])
            else:
                DC_DATA.append(RAW_DATA[i])

        # Quicksorts the DC and Marvel Data separately and combines it into one List
        SORTED_DATA = quickSort(DC_DATA, 0, len(DC_DATA)-1) + quickSort(MARVEL_DATA, 0, len(MARVEL_DATA)-1)


        addData(SORTED_DATA)

    while True:

        # Fetches the data from the database
        DATA = getData()

        for i in range(len(DATA)):
            DATA[i] = list(DATA[i])
            for j in range(len(DATA[i])):
                if DATA[i][j] == "":
                    DATA[i][j] = "N/A"


        # INPUTS #
        CHOICE = menu()


        # PROCESSING #
        if CHOICE == 1:


            USER_SEARCH = userInput(DATA)
            VALUE_INDEX, USER_LIST = binarySearch(DATA, USER_SEARCH)

            # OUTPUTS #
            print(f"\n{tabulate(USER_LIST[VALUE_INDEX:VALUE_INDEX+1], headers=TITLES)}")


        # INPUTS #
        if CHOICE == 2:

            # PROCESSING AND OUTPUTS
            print(tabulate(DATA, headers=TITLES)) # prints


        # INPUTS #
        if CHOICE == 3:
            # PROCESSING #
            addSuperHero()
            # OUTPUTS #
            print("Successfully added your superhero!")

        # INPUTS #
        if CHOICE == 4:
            # PROCESSING AND OUTPUTS
            print("Thanks for using the program!")
            break










