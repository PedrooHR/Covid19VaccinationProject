"""
Assignment: 06 - Scale-free network.
Professor: João Meidanis
Student: Rubens de Castro Pereira
Date: 22/09/2022
Version: 1.0.0
"""

# ###########################################
# Importing needed libraries
# ###########################################

# importing python packages and modules
import csv
import math

import matplotlib.pyplot as plt

# import application  classes
from City import City

# ###########################################
# Constants
# ###########################################
LINE_FEED = '\n'
TAB = '\t'
COMMA = ','


# ###########################################
# Application Methods
# ###########################################

# ###########################################
# Methods of Level 1
# ###########################################


# reading the links list
def processInputFile(fileName):
    # initializing objects and variables
    cities = []
    linesCounter = 0

    # reading files of links
    with open(fileName, newline='', encoding='utf-8-sig') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=COMMA)

        header = False
        for row in csvReader:

            if not header:
                header = True
                continue

            # getting fields
            date = row[0]
            state = row[1]
            cityName = row[2]
            ibgeID = int(row[3])
            dose = int(row[4])
            vaccine = row[5]
            sex = row[6]
            age = row[7]
            count = int(row[8])
            pop2021 = int(row[9])

            # getting city by IBGE
            city = getCityByIdIBGE(ibgeID, cities)

            # check if city exists in the list
            if city is None:
                # creating new city object
                city = City(ibgeID, cityName, state, pop2021)

                # adding city to list
                cities.append(city)

            # adding number of vaccines in city
            city.addDose(dose, count)

            linesCounter += 1
            if linesCounter > 100000:
                print(row)
                linesCounter = 0

    # calculating dose percentage
    for city in cities:
        city.calculateDosePercentage()

    # returning lists
    return cities


# ###########################################
# Methods of Level 2
# ###########################################

# get city by IBGE id
def getCityByIdIBGE(idIBGE, cities):
    for city in cities:
        if idIBGE == city.idIBGE:
            return city

    # not found city in list
    return None


def printStatistic(fileName, cities):
    print('-------------------------------------------')
    print()
    print(fileName)
    print()
    print('Total of cities: ', len(cities))

    print()
    print('Number of links of nodes')
    for city in cities:
        print(city)

    # print()
    # print('Network Degrees')
    # degrees, totalNumberOfLinks, degreesProbability, minDegree, maxDegree = Node.getValuesToPlot(nodes)
    # totalDegreeProbability = 0
    # for i in range(len(degrees)):
    #     print('Degree: ', degrees[i], ' ', totalNumberOfLinks[i], ' ', degreesProbability[i])
    #     totalDegreeProbability = totalDegreeProbability + degreesProbability[i]
    #
    # print('Total of degrees probability: ', totalDegreeProbability)


# save cities  list into CSV file
def saveNodesListIntoCSVFile(cities, fileName):
    # preparing nodes list to save
    list = []
    row = ['city' \
        , 'state' \
        , 'id_ibge' \
        , 'population' \
        , 'number_of_dose_0' \
        , 'number_of_dose_1' \
        , 'number_of_dose_2' \
        , 'number_of_dose_3' \
        , 'number_of_dose_4' \
        , 'percentage_of_dose_0' \
        , 'percentage_of_dose_1' \
        , 'percentage_of_dose_2' \
        , 'percentage_of_dose_3' \
        , 'percentage_of_dose_4' \
           ]
    list.append(row)

    for city in cities:
        row = [city.name \
            , city.state \
            , city.idIBGE \
            , str(city.population) \
            , str(city.numberOfDose_0) \
            , str(city.numberOfDose_1) \
            , str(city.numberOfDose_2) \
            , str(city.numberOfDose_3) \
            , str(city.numberOfDose_4) \
            , str(city.percentOfDose_0) \
            , str(city.percentOfDose_1) \
            , str(city.percentOfDose_2) \
            , str(city.percentOfDose_3) \
            , str(city.percentOfDose_4) \
               ]
        list.append(row)

    with open(fileName, 'w', newline='') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(list)


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # setting paths and file names
    applicationPath = 'Z:/Meu Drive/03. Doutorado/30. Doutorado IC-Unicamp/2022-2/MO412 - Graphs Algoritms/07. Final Project/Dataset COVID-19 Brazil/Brasil/'

    # fileName = applicationPath + 'processed_GO.csv/processed_GO.csv'
    fileName = applicationPath + 'processed_SC.csv/processed_SC.csv'

    # initializing objects
    cities = []

    # reading nodes list
    cities = processInputFile(fileName)

    # printing details of cities
    printStatistic(fileName, cities)

    # saving nodes list into CSV file
    # citiesFileName = applicationPath + 'processed_GO.csv/processed_GO_cities.csv'
    citiesFileName = applicationPath + 'processed_SC.csv/processed_SC_cities.csv'
    saveNodesListIntoCSVFile(cities, citiesFileName)

    # Wait for the user input to terminate the program
    # input("Press any key to terminate the program")
