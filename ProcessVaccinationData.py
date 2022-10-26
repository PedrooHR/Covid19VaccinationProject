"""
Project: Final Project Vaccination
Professor: João Meidanis
Students: Pedro Henrique Di Francia Rosso and Rubens de Castro Pereira
Date: 21/10/2022
Version: 1.0.0
Function: Process original data of vaccination, covid cases and covid death
"""

# ###########################################
# Importing needed libraries
# ###########################################


# importing python packages and modules
import os
import pandas as pd


# from IPython.display import display


# ###########################################
# Application Methods
# ###########################################


def getStatesOfBrazil(inputFilesPath, filename):
    dfStatesOfBrazil = pd.read_excel(inputFilesPath + filename)
    return dfStatesOfBrazil


def processSheets(inputSheets, outputFilesPath, columnsOfNewSheet, columnsOfGroupBy, outputSheetName,
                  internalSheetName):
    # message in the console
    print()
    print("----------------------------------------------")
    print("Processing ", internalSheetName)
    print()

    # initializing new dataframe
    dfOneSheet = pd.DataFrame()
    statisticList = []

    # processing sheets
    for sheet in inputSheets:
        try:
            # reading sheet
            dfSheet = pd.read_csv(sheet, compression='gzip', header=0, sep=',', quotechar='"')

            # setting statistic
            statisticItem = [internalSheetName, sheet, len(dfSheet)]
            statisticList.append(statisticItem)

            # creating news columns to help the group by clause
            dfSheet['year'] = pd.DatetimeIndex(dfSheet['date']).year
            dfSheet['month'] = pd.DatetimeIndex(dfSheet['date']).month
            # dfStateVaccinations['year_month'] = dfStateVaccinations['date'].str.slice(start=0, stop=7)

            # calculating total number of vaccinations by city
            dfStateVaccinationsGroupedByCity = dfSheet[columnsOfNewSheet].groupby(columnsOfGroupBy,
                                                                                  as_index=False).sum()

            # adding dataframe of all states of Brazil
            dfOneSheet = pd.concat([dfOneSheet, dfStateVaccinationsGroupedByCity])

            # message showing processing the state
            print("Processing state", sheet)

        except:
            # nothing to do
            pass

    # removing output file if exists
    if os.path.exists(outputFilesPath + outputSheetName):
        os.remove(outputFilesPath + outputSheetName)

    # saving sheet
    with pd.ExcelWriter(outputFilesPath + outputSheetName, mode='w', ) as writer:
        dfOneSheet.to_excel(writer, sheet_name=internalSheetName)

    return statisticList


# def processCityPopulation(inputSheets, outputFilesPath, columnsOfNewSheet, columnsOfGroupBy, outputSheetName,
#                           internalSheetName):
#     # message in the console
#     print()
#     print("----------------------------------------------")
#     print("Processing ", internalSheetName)
#     print()
#
#     # initializing new dataframe
#     dfOneSheet = pd.DataFrame()
#     statisticList = []
#
#     # processing sheets
#     for sheet in inputSheets:
#         try:
#             # reading sheet
#             dfSheet = pd.read_csv(sheet, compression='gzip', header=0, sep=',', quotechar='"')
#
#             # getting the city population
#             columnsOfNewSheet = ['state', 'city', 'ibgeID', 'year', 'month', 'count']
#             columnsOfGroupBy = ['state', 'city', 'ibgeID', 'year', 'month']
#             dfCityPopulation = dfSheet[columnsOfNewSheet].groupby(columnsOfGroupBy,
#                                                                   as_index=False).sum()
#
#             # adding dataframe of all states of Brazil
#             dfOneSheet = pd.concat([dfOneSheet, dfStateVaccinationsGroupedByCity])
#
#             # message showing processing the state
#             print("Processing state", sheet)
#
#         except:
#             # nothing to do
#             pass
#
#     # removing output file if exists
#     if os.path.exists(outputFilesPath + outputSheetName):
#         os.remove(outputFilesPath + outputSheetName)
#
#     # saving sheet
#     with pd.ExcelWriter(outputFilesPath + outputSheetName, mode='w', ) as writer:
#         dfOneSheet.to_excel(writer, sheet_name=internalSheetName)
#
#     return statisticList
#

# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # setting paths and file names
    rootPath = os.getcwd().replace("\\", "/") + "/../"
    workingPath = rootPath + 'data/'

    inputFilesPath = '01-Input Files/'
    outputFilesPath = '02-Output Files/'
    # vaccinationDatasetUrl = 'https://github.com/wcota/covid19br-vac/'

    # getting states of Brazil
    dfStatesOfBrazil = getStatesOfBrazil(workingPath + inputFilesPath, 'states_of_brazil.xlsx')

    # statistic of processing
    statisticList = []

    # building list of states to process the vaccinations data
    inputSheets = []
    for state in dfStatesOfBrazil["initials"]:
        # setting the full path and sheet name for the vaccinations data
        inputSheets.append(workingPath + inputFilesPath + 'processed_' + state.strip() + '.csv.gz')

    # processing vaccination data
    columnsOfNewSheet = ['state', 'city', 'ibgeID', 'pop2021', 'year', 'month', 'count']
    columnsOfGroupBy = ['state', 'city', 'ibgeID', 'pop2021', 'year', 'month']
    outputSheetName = "Vaccination.xlsx"
    internalSheetName = "Vaccination"
    statisticList = statisticList + processSheets(inputSheets \
                                                  , workingPath + outputFilesPath \
                                                  , columnsOfNewSheet \
                                                  , columnsOfGroupBy \
                                                  , outputSheetName \
                                                  , internalSheetName \
                                                  )

    # processing vaccination data
    columnsOfNewSheet = ['state', 'city', 'ibgeID', 'pop2021']
    columnsOfGroupBy = ['state', 'city', 'ibgeID', 'pop2021']
    outputSheetName = "City.xlsx"
    internalSheetName = "City"
    processSheets(inputSheets \
                  , workingPath + outputFilesPath \
                  , columnsOfNewSheet \
                  , columnsOfGroupBy \
                  , outputSheetName \
                  , internalSheetName \
                  )

    # building list of sheets to process the deaths
    inputSheets.clear()
    inputSheets.append(workingPath + inputFilesPath + 'cases-brazil-cities-time_2020.csv.gz')
    inputSheets.append(workingPath + inputFilesPath + 'cases-brazil-cities-time_2021.csv.gz')
    inputSheets.append(workingPath + inputFilesPath + 'cases-brazil-cities-time.csv.gz')

    # processing deaths data
    columnsOfNewSheet = ['state', 'city', 'ibgeID', 'year', 'month', 'newDeaths']
    columnsOfGroupBy = ['state', 'city', 'ibgeID', 'year', 'month']
    outputSheetName = "CovidDeath.xlsx"
    internalSheetName = "CovidDeath"
    statisticList = statisticList + processSheets(inputSheets \
                                                  , workingPath + outputFilesPath \
                                                  , columnsOfNewSheet \
                                                  , columnsOfGroupBy \
                                                  , outputSheetName \
                                                  , internalSheetName \
                                                  )

    # building list of sheets to process new cases
    inputSheets.clear()
    inputSheets.append(workingPath + inputFilesPath + 'cases-brazil-cities-time_2020.csv.gz')
    inputSheets.append(workingPath + inputFilesPath + 'cases-brazil-cities-time_2021.csv.gz')
    inputSheets.append(workingPath + inputFilesPath + 'cases-brazil-cities-time.csv.gz')

    # processing deaths data
    columnsOfNewSheet = ['state', 'city', 'ibgeID', 'year', 'month', 'newCases']
    columnsOfGroupBy = ['state', 'city', 'ibgeID', 'year', 'month']
    outputSheetName = "CovidCase.xlsx"
    internalSheetName = "CovidCase"
    statisticList = statisticList + processSheets(inputSheets \
                                                  , workingPath + outputFilesPath \
                                                  , columnsOfNewSheet \
                                                  , columnsOfGroupBy \
                                                  , outputSheetName \
                                                  , internalSheetName \
                                                  )

    # saving statistic sheet
    statisticSheetName = workingPath + outputFilesPath + 'ProcessingStatistics.xlsx'
    dfStatistic = pd.DataFrame(statisticList, columns=['subject', 'sheet', 'number of rows'])
    with pd.ExcelWriter(statisticSheetName, mode='w', ) as writer:
        dfStatistic.to_excel(writer)

    # Wait for the user input to terminate the program
    # input("Press any key to terminate the program")
