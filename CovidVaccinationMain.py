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
import networkx as nx

# import application  classes
from City import City
from EuclideanDistanceTwoCities import EuclideanDistanceTwoCities

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


# calculating the euclidean distance between two cities
def calculateEuclideanDistanceOfCities(cities):
    # defining new objects
    euclideanDistancesOfCities = []

    # getting the len of cities list
    maxCities = len(cities)
    i = 0
    while i < maxCities:

        # setting origin city
        originCity = cities[i]

        j = i + 1
        while j < maxCities:
            targetCity = cities[j]
            # print(originCity.name, ' ', targetCity.name)

            # calculating the euclidean distance
            euclideanDistance = EuclideanDistanceTwoCities.calculateEuclideanDistanceTwoCities(originCity, targetCity)

            # adding the euclidean distance calculated in the list
            euclideanDistancesOfCities.append(EuclideanDistanceTwoCities(originCity, targetCity, euclideanDistance))

            # increment index
            j = j + 1

        # increment index
        i = i + 1

    # # calculating the distances
    # for originCity in cities:
    #     for targetCity in cities:
    #         # origin and target cities are the same city
    #         if originCity.idIBGE == targetCity.idIBGE:
    #             continue
    #
    #         # verifying if the link of two cities exists
    #         # if EuclideanDistanceTwoCities.hasLinkOfTwoCities(originCity, targetCity, euclideanDistancesOfCities):
    #         #     continue
    #
    #         # calculating the euclidean distance
    #         euclideanDistance = EuclideanDistanceTwoCities.calculateEuclideanDistanceTwoCities(originCity, targetCity)
    #
    #         # adding the euclidean distance calculated in the list
    #         euclideanDistancesOfCities.append(EuclideanDistanceTwoCities(originCity, targetCity, euclideanDistance))
    #
    # returning the cities list with the distances between all of them
    return euclideanDistancesOfCities


# getting the percentile of the euclidean distances list
def getPercentileOfEuclideanDistancesWithShortestDistance(percentile, euclideanDistancesOfCities):
    # defining new objects
    list = []

    # sort lists by euclidean distance in ascending order
    euclideanDistancesOfCities.sort(key=lambda x: x.euclideanDistance, reverse=False)

    # calculating the percentile of the euclidean distances of cities list
    percentileSize = int(len(euclideanDistancesOfCities) / 100)

    # selecting links according by percentile desired
    count = 0
    maxCount = percentile * percentileSize
    # maxCount = 20
    while (count < maxCount):
        # selecting item
        list.append(euclideanDistancesOfCities[count])

        # incrementing counter
        count = count + 1

    # returning pruned list
    return list


# building the cities graph
def buildGraph(cities, euclideanDistancesOfCities, graphName):
    # defining new objects
    citiesGraph = nx.Graph()

    # setting graph name
    citiesGraph.name = graphName

    # creating the nodes from cities
    for city in cities:
        citiesGraph.add_node(city.idIBGE)

    # creating the links between nodes (cities)
    for euclideanDistanceOfTwoCities in euclideanDistancesOfCities:
        citiesGraph.add_edge( \
            euclideanDistanceOfTwoCities.originCity.idIBGE \
            , euclideanDistanceOfTwoCities.targetCity.idIBGE \
            )
        # citiesGraph.add_edge( \
        #     euclideanDistanceOfTwoCities.originCity.idIBGE \
        #     , euclideanDistanceOfTwoCities.targetCity.idIBGE \
        #     , weight=euclideanDistanceOfTwoCities.euclideanDistance \
        #     )

    return citiesGraph


# building the cities graph
def printGraphReport(citiesGraph):
    # printing graph statistics
    print('Graph Statistics')
    print('Name: ', citiesGraph.name)
    print('Number of nodes: ', nx.number_of_nodes(citiesGraph))
    print('Number of links: ', nx.number_of_edges(citiesGraph))
    print('Average Degree: ', '???')
    print('Density : ', nx.density(citiesGraph))
    print('number_of_selfloops: ', nx.number_of_selfloops(citiesGraph))


# show cities graph
def showGraph(citiesGraph):
    citiesGraph.name = 'Cities - SC'
    options = {
        'node_color': 'green',
        'node_size': 10,
        'width': 1,
    }
    # nx.draw(citiesGraph, with_labels=True, font_weight='bold')
    nx.draw(citiesGraph, **options)
    plt.show()
    # nx.draw_random(citiesGraph, **options)
    # plt.show()
    # nx.draw_circular(citiesGraph, **options)
    # plt.show()
    # nx.draw_spectral(citiesGraph, **options)
    # plt.show()
    # nx.draw_shell(citiesGraph, **options)
    # plt.show()
    # nx.draw_spring(citiesGraph, **options)
    # plt.show()
    # nx.draw_networkx(citiesGraph, **options)
    # plt.show()
    #
    # print()
    # print(citiesGraph.name)
    # print()
    # print(citiesGraph.degree)


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


# save cities list into CSV file
def saveCitiesListIntoCSVFile(cities, fileName):
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


# save euclidean distances list into CSV file
def saveEuclideanDistancesListIntoCSVFile(euclideanDistancesOfCities, fileName):
    # preparing nodes list to save
    list = []
    row = ['origin_city' \
        , 'IBGE_origin_city' \
        , 'target_city' \
        , 'IBGE_target_city' \
        , 'euclidean_distance'
           ]
    list.append(row)

    for euclideanDistanceOfTwoCities in euclideanDistancesOfCities:
        row = [euclideanDistanceOfTwoCities.originCity.name \
            , euclideanDistanceOfTwoCities.originCity.idIBGE \
            , euclideanDistanceOfTwoCities.targetCity.name \
            , euclideanDistanceOfTwoCities.targetCity.idIBGE \
            , str(euclideanDistanceOfTwoCities.euclideanDistance)
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

    statePath = 'processed_SC.csv/'
    stateFilename = 'processed_SC.csv'

    fileName = applicationPath + statePath + stateFilename

    # initializing objects
    cities = []
    euclideanDistancesOfCities = []

    # reading nodes list
    cities = processInputFile(fileName)

    # calculating the euclidean distances between all cities
    euclideanDistancesOfCities = calculateEuclideanDistanceOfCities(cities)

    # removing items duplicated
    # euclideanDistancesOfCitiesWithoutDuplicates = EuclideanDistanceTwoCities.removeDuplicateCities(
    #     euclideanDistancesOfCities)

    # pruning  the euclidean distances between all cities
    prunedEuclideanDistancesOfCities = getPercentileOfEuclideanDistancesWithShortestDistance( \
        1, euclideanDistancesOfCities)

    # building graph of the cities
    citiesGraph = buildGraph(cities, prunedEuclideanDistancesOfCities, stateFilename)

    # print the graph report
    printGraphReport(citiesGraph)

    # showing graph of the cities
    showGraph(citiesGraph)

    # printing details of cities
    printStatistic(fileName, cities)

    # saving cities list into CSV file
    citiesFileName = applicationPath + statePath + 'processed_SC_cities.csv'
    saveCitiesListIntoCSVFile(cities, citiesFileName)

    # saving euclidean distances list into CSV file
    euclideanDistancesFileName = applicationPath + statePath + 'processed_SC_cities_euclidean_distances.csv'
    saveEuclideanDistancesListIntoCSVFile(euclideanDistancesOfCities, euclideanDistancesFileName)

    # saving euclidean distances list into CSV file
    euclideanDistancesFileName = applicationPath + statePath + 'processed_SC_cities_euclidean_distances_pruned.csv'
    saveEuclideanDistancesListIntoCSVFile(prunedEuclideanDistancesOfCities, euclideanDistancesFileName)

    # Wait for the user input to terminate the program
    input("Press any key to terminate the program")

    x = 0
