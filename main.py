'''
title: Superhero Search and Sort
author: Parth Sakpal
date-created: 10/12/2023
'''


# import libraries
import csv
import pathlib
import sqlite3



DATABASE_FILE = "supehero.db"

FIRST_RUN = True

# Checks to see if database file already exists
if (pathlib.Path.cwd() / DATABASE_FILE).exists():
    FIRST_RUN = False

CONNECTION = sqlite3.connect(DATABASE_FILE)
CURSOR = CONNECTION.cursor()



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
            if LIST[j][9] < LIST[MIN_INDEX][9]:
                MIN_INDEX = j


        if LIST[MIN_INDEX] < LIST[i]:
            TEMP = LIST[i]
            LIST[i] = LIST[MIN_INDEX]
            LIST[MIN_INDEX] = TEMP











# Extract data from the csv
def getData(fileName):
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

    return DATA


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
        print("worked")







def createDatabase(LIST):
    '''
    Create the superhero datbase
    :param LIST: list
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
                year,
                brand
                
            )
    ;""")



if __name__ == "__main__":

    DATA = getData("comicBookCharData_mixed.csv")
    print(int(DATA[0][9]))
    print(DATA[0][9])

    '''print(DATA)
    selectionSort(DATA)
    print("######################################################################")
    print(DATA)'''







