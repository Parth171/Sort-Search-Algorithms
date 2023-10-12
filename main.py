'''
title: Superhero Search and Sort
author: Parth Sakpal
date-created: 10/12/2023
'''


# import libraries
import csv


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






if __name__ == "__main__":
    DATA = getData("comicBookCharData_mixed.csv")

    userInput(DATA)



