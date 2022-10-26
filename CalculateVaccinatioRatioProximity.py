"""
Project: Final Project Vaccination
Professor: João Meidanis
Students: Pedro Henrique Di Francia Rosso and Rubens de Castro Pereira
Date: 24/10/2022
Version: 1.0.0
Function: Calculate the ratio proximity between cities from the summarized data.
"""
# ###########################################
# Importing needed libraries
# ###########################################


# importing python packages and modules
import os
import pandas as pd
import math


# from IPython.display import display


# ###########################################
# Application Methods
# ###########################################


def calculationVaccinationRadio(inputSheet, outputFilesPath, outputSheetName, internalSheetName):
    # message in the console
    print()
    print("----------------------------------------------")
    print("Processing ", inputSheet)
    print()

    # initializing new dataframe
    dfResult = pd.DataFrame()
    statisticList = []

    # reading sheet
    # dfSheet = pd.read_excel(inputSheet, header=0, sep=',', quotechar='"')
    dfSheet = pd.read_excel(inputSheet)

    # group data summarizing number of vaccines of each city
    columnsOfNewSheet = ['state', 'city', 'ibgeID', 'pop2021', 'count']
    columnsOfGroupBy = ['state', 'city', 'ibgeID', 'pop2021']
    dfVaccinationsGroupedByCity = dfSheet[columnsOfNewSheet].groupby(columnsOfGroupBy, as_index=False).sum()

    # auxiliary list of results
    listEuclideanDistanceOfCity = []

    # calculation of euclidean distance between all cities of Brazil
    for origin_index in range(0, len(dfVaccinationsGroupedByCity) - 1):
        # if (origin_index > 100):
        #     break

        for target_index in range(origin_index + 1, len(dfVaccinationsGroupedByCity)):
            # processing cities in the same state
            # if (dfVaccinationsGroupedByCity['state'].iloc[origin_index] != \
            #         dfVaccinationsGroupedByCity['state'].iloc[target_index]):
            #     continue

            # calculting the euclidean distance bewtween two cities
            euclideanDistance = calculateEuclideanDistanceTwoCities( \
                dfVaccinationsGroupedByCity['count'].iloc[origin_index] \
                , dfVaccinationsGroupedByCity['pop2021'].iloc[origin_index] \
                , dfVaccinationsGroupedByCity['count'].iloc[target_index] \
                , dfVaccinationsGroupedByCity['pop2021'].iloc[target_index] \
                )

            # if (euclideanDistance < 0.5):
            itemEuclideanDistanceOfCity = [ \
                dfVaccinationsGroupedByCity['state'].iloc[origin_index] \
                , dfVaccinationsGroupedByCity['city'].iloc[origin_index] \
                , dfVaccinationsGroupedByCity['ibgeID'].iloc[origin_index] \
                , dfVaccinationsGroupedByCity['state'].iloc[target_index] \
                , dfVaccinationsGroupedByCity['city'].iloc[target_index] \
                , dfVaccinationsGroupedByCity['ibgeID'].iloc[target_index] \
                , euclideanDistance \
                ]
            listEuclideanDistanceOfCity.append(itemEuclideanDistanceOfCity)

    # removing output file if exists
    if os.path.exists(outputFilesPath + outputSheetName):
        os.remove(outputFilesPath + outputSheetName)

    # saving sheet
    dfEuclideanDistanceOfCity = pd.DataFrame( \
        listEuclideanDistanceOfCity, columns=[ \
            'origin state', 'origin city', 'origin ibge id' \
            , 'target state', 'target city', 'target ibge id' \
            , 'distance'] \
        )
    # with pd.ExcelWriter(outputFilesPath + outputSheetName, mode='w', ) as writer:
    #     dfEuclideanDistanceOfCity.to_excel(writer)
    dfEuclideanDistanceOfCity.to_csv(outputFilesPath + outputSheetName, encoding='utf-8')


def calculateEuclideanDistanceTwoCities(originCityVaccineCount, originCityPopulation, \
                                        targetCityVaccineCount, targetCityPopulation):
    # calculating percentages
    originPercentage = (originCityVaccineCount / 4) / originCityPopulation
    targetPercentage = (targetCityVaccineCount / 4) / targetCityPopulation

    # calculating the distance
    distance = math.sqrt(math.pow((originPercentage - targetPercentage), 2))

    # returning the distance
    return distance


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # setting paths and file names
    rootPath = os.getcwd().replace("\\", "/") + "/../"
    workingPath = rootPath + 'data/'

    inputFilesPath = '02-Output Files/'
    outputFilesPath = '03-Calculations/'

    # statistic of processing
    statisticList = []

    inputSheetName = "Vaccination.xlsx"
    outputSheetName = "VaccinationRatioProximity.csv"
    internalSheetName = "VaccinationRatioProximity"
    calculationVaccinationRadio(workingPath + inputFilesPath + inputSheetName \
                                , workingPath + outputFilesPath \
                                , outputSheetName \
                                , internalSheetName \
                                )

    # Wait for the user input to terminate the program
    # input("Press any key to terminate the program")
