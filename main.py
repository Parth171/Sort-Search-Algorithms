'''
title: Superhero Search and Sort
author: Parth Sakpal
date-created: 10/12/2023
'''


# import libraries
import csv
import pathlib
import sqlite3
from tabulate import tabulate



DATABASE_FILE = "superhero.db"

FIRST_RUN = True

# Checks to see if database file already exists
if (pathlib.Path.cwd() / DATABASE_FILE).exists():
    FIRST_RUN = False

CONNECTION = sqlite3.connect(DATABASE_FILE)
CURSOR = CONNECTION.cursor()

MARVEL_DATA = []
DC_DATA = []


def menu():
    """
    presents a menu to the user for them to choose an action
    :return: int
    """

    print("""
    ___________________________________________________________________________________________________________________
    
    Welcome to the SUPER HERO SEARCH AND SORT!
    
    This program will allow you to search for a superhero by using their SuperHero ID, View the sorted SuperHero 
    database, and even add your own superhero to the Database! (Note: Please enter the ID accurately and exactly) 
    
    1. Search for SuperHero using their Superhero ID
    2. View Sorted Superhero Database (Sorted by their SuperHero ID in ascending order with DC Superheros appearing first,followed by Marvel SuperHeros.) 
    3. Add your own Superhero
    4. Exit the program
    ___________________________________________________________________________________________________________________
    """)

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

# Sort the Data using Selection Sort
def selectionSort(LIST):
    '''
    Selection sorts the data by the year column
    :param LIST: list
    :return: List (sorted)
    '''

    for i in range(len(LIST)-1):
        MIN_INDEX = i

        for j in range(i+1, len(LIST)):
            if LIST[j][0][1:] < LIST[MIN_INDEX][0][1:]:
                MIN_INDEX = j


        if LIST[MIN_INDEX][0][1:] < LIST[i][0][1:]:
            TEMP = LIST[i]
            LIST[i] = LIST[MIN_INDEX]
            LIST[MIN_INDEX] = TEMP


    return LIST


# Extract data from the csv
def getRawData(fileName):
    '''
    gets the raw data from the Superhero File
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


def userInput(DATA):
    '''
    gets the user input for Superhero ID and error checks
    :param DATA: 2D array
    :return: String
    '''


    INPUT = input(str("What is the superhero ID: "))

    ID = []


    for i in range(len(DATA)):
            ID.append(DATA[i][0])


    if INPUT not in ID:
        print("NOT VALID INPUT!")
        return userInput(DATA)

    else:
        return INPUT


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


def addData(LIST):
    """
    Adds the sorted list to the database
    :param LIST: sorted list of data
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


def linearSearch(LIST, VALUE):
    """
    linear searches the data to find the value
    :param LIST: list
    :param VALUE: str
    :return: index of the value
    """

    for i in range(len(LIST)):
        if LIST[i][0] == VALUE:
            return i


def getData():
    """
    gets the data from the database (this is to ensure that if the user has added a new member, the member can be displayed)
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

    SORTED_DATA = selectionSort(DC_DATA) + selectionSort(MARVEL_DATA)


    addData(SORTED_DATA)

    while True:

        DATA = getData()

        for i in range(len(DATA)):
            DATA[i] = list(DATA[i])
            for j in range(len(DATA[i])):
                if DATA[i][j] == "":
                    DATA[i][j] = "N/A"

        CHOICE = menu()

        if CHOICE == 1:


            USER_SEARCH = userInput(DATA)
            VALUE_INDEX = linearSearch(DATA, USER_SEARCH)


            #DATA[VALUE_INDEX] = tuple(DATA[VALUE_INDEX])

            print(f"\n{tabulate(DATA[VALUE_INDEX:VALUE_INDEX+1], headers=TITLES)}")



        if CHOICE == 2:

            print(tabulate(DATA, headers=TITLES))


        if CHOICE == 3:
            addSuperHero()
            print("Successfully added your superhero!")



        if CHOICE == 4:
            print("Thanks for using the program!")
            break










