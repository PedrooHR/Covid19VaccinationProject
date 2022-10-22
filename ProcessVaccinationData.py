"""
Assignment: Final Project Vaccination
Professor: João Meidanis
Students: Pedro Henrique Di Francia Rosso and Rubens de Castro Pereira
Date: 21/10/2022
Version: 1.0.0
"""

# ###########################################
# Importing needed libraries
# ###########################################


# importing python packages and modules
import os
import pandas as pd


# ###########################################
# Application Methods
# ###########################################


def getStatesOfBrazil(inputFilesPath, filename):
    dfStatesOfBrazil = pd.read_excel(inputFilesPath + filename)
    # display(dfStatesOfBrazil)
    return dfStatesOfBrazil


def processSheets(inputSheets, outputFilesPath, columnsOfNewSheet, columnsOfGroupBy, outputSheetName,
                  internalSheetName):
    # message in the console
    print("----------------------------------------------")
    print("Processing ", internalSheetName)
    print()

    # initializing new dataframe
    dfOneSheet = pd.DataFrame()

    # processing sheets
    for sheet in inputSheets:
        try:
            # reading sheet
            dfSheet = pd.read_csv(sheet, compression='gzip', header=0, sep=',', quotechar='"')

            # creating news columns to help the group by clause
            dfSheet['year'] = pd.DatetimeIndex(dfSheet['date']).year
            dfSheet['month'] = pd.DatetimeIndex(dfSheet['date']).month
            # dfStateVaccinations['year_month'] = dfStateVaccinations['date'].str.slice(start=0, stop=7)

            # calculate the total number of vaccinations by city
            # columnsOfNewSheet = ['state', 'city', 'year', 'month', 'count']
            # columnsOfGroupBy = ['state', 'city', 'year', 'month']
            dfStateVaccinationsGroupedByCity = dfSheet[columnsOfNewSheet].groupby(columnsOfGroupBy,
                                                                                  as_index=False).sum()

            # adding dataframe of all states of Brazil
            dfOneSheet = pd.concat([dfOneSheet, dfStateVaccinationsGroupedByCity])

            # message showing processing the state
            print("Processing state", sheet)

        except:
            # nothing to do
            pass

    # remove output file if exists
    # outputSheetName = "allStatesVaccinations.xlsx"
    if os.path.exists(outputFilesPath + outputSheetName):
        os.remove(outputFilesPath + outputSheetName)

    # save sheet
    # internalSheetName = "vaccinations"
    with pd.ExcelWriter(outputFilesPath + outputSheetName, mode='w', ) as writer:
        dfOneSheet.to_excel(writer, sheet_name=internalSheetName)


def processVaccinationSheets(inputFilesPath, outputFilesPath, dfStatesOfBrazil, vaccinantionDatasetUrl):
    # initializing new dataframe
    dfAllStatesOfBrazil = pd.DataFrame()

    # processing vaccinations per states
    for state in dfStatesOfBrazil["initials"]:
        # # downloading file from Wesley Cota (wcota) github
        # urlAndFileName = vaccinantionDatasetUrl + 'processed_' + state.strip() + '.csv.gz'
        # r = requests.get(urlAndFileName, allow_redirects=True)
        # fullFileName = inputFilesPath + 'processed_' + state.strip() + '.csv.gz'
        # open(fullFileName, 'wb').write(r.content)

        # getting the vaccinations of state
        fullFileName = inputFilesPath + 'processed_' + state.strip() + '.csv.gz'
        try:
            # reading sheet of state vaccinations
            dfStateVaccinations = pd.read_csv(fullFileName, compression='gzip', header=0, sep=',', quotechar='"')

            # creating news columns to help the group by clause
            dfStateVaccinations['year'] = pd.DatetimeIndex(dfStateVaccinations['date']).year
            dfStateVaccinations['month'] = pd.DatetimeIndex(dfStateVaccinations['date']).month
            # dfStateVaccinations['year_month'] = dfStateVaccinations['date'].str.slice(start=0, stop=7)

            # calculate the total number of vaccinations by city
            dfStateVaccinationsGroupedByCity = dfStateVaccinations[['state', 'city', 'year', 'month', 'count']].groupby(
                ['state', 'city', 'year', 'month'], as_index=False).sum()

            # adding dataframe of all states of Brazil
            dfAllStatesOfBrazil = pd.concat([dfAllStatesOfBrazil, dfStateVaccinationsGroupedByCity])

            # message showing processing the state
            print("Processing state", state)

        except:
            # nothing to do
            pass

    # remove output file if exists
    outputFilename = "allStatesVaccinations.xlsx"
    if os.path.exists(outputFilesPath + outputFilename):
        os.remove(outputFilesPath + outputFilename)

    # save sheet
    with pd.ExcelWriter(outputFilesPath + outputFilename, mode='w', ) as writer:
        dfAllStatesOfBrazil.to_excel(writer, sheet_name="vaccinations")


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # setting paths and file names
    rootPath = os.getcwd().replace("\\", "/") + "/../"
    workingPath = rootPath + 'data/'

    inputFilesPath = '01-Input Files/'
    outputFilesPath = '02-Output Files/'
    vaccinationDatasetUrl = 'https://github.com/wcota/covid19br-vac/'

    # getting states of Brazil
    dfStatesOfBrazil = getStatesOfBrazil(workingPath + inputFilesPath, 'states_of_brazil.xlsx')

    # build list of states to process the vaccinations data
    inputSheets = []
    for state in dfStatesOfBrazil["initials"]:
        # setting the full path and sheet name for the vaccinations data
        inputSheets.append(workingPath + inputFilesPath + 'processed_' + state.strip() + '.csv.gz')

    # processing vaccination data
    columnsOfNewSheet = ['state', 'city', 'year', 'month', 'count']
    columnsOfGroupBy = ['state', 'city', 'year', 'month']
    outputSheetName = "allVaccinationsOfStates.xlsx"
    internalSheetName = "vaccinations"
    processSheets(inputSheets \
                  , workingPath + outputFilesPath \
                  , columnsOfNewSheet \
                  , columnsOfGroupBy \
                  , outputSheetName \
                  , internalSheetName \
                  )
    # processVaccinationSheets(workingPath + inputFilesPath \
    #                          , workingPath + outputFilesPath \
    #                          , dfStatesOfBrazil \
    #                          , vaccinationDatasetUrl \
    #                          )

    # build list of sheets to process the deaths 
    inputSheets.clear()
    inputSheets.append(workingPath + inputFilesPath + 'cases-brazil-cities-time_2020.csv.gz')
    inputSheets.append(workingPath + inputFilesPath + 'cases-brazil-cities-time_2021.csv.gz')
    inputSheets.append(workingPath + inputFilesPath + 'cases-brazil-cities-time.csv.gz')

    # processing deaths data
    columnsOfNewSheet = ['state', 'city', 'year', 'month', 'newDeaths']
    columnsOfGroupBy = ['state', 'city', 'year', 'month']
    outputSheetName = "allDeaths.xlsx"
    internalSheetName = "deaths"
    processSheets(inputSheets \
                  , workingPath + outputFilesPath \
                  , columnsOfNewSheet \
                  , columnsOfGroupBy \
                  , outputSheetName \
                  , internalSheetName \
                  )

    # build list of sheets to process new cases
    inputSheets.clear()
    inputSheets.append(workingPath + inputFilesPath + 'cases-brazil-cities-time_2020.csv.gz')
    inputSheets.append(workingPath + inputFilesPath + 'cases-brazil-cities-time_2021.csv.gz')
    inputSheets.append(workingPath + inputFilesPath + 'cases-brazil-cities-time.csv.gz')

    # processing deaths data
    columnsOfNewSheet = ['state', 'city', 'year', 'month', 'newCases']
    columnsOfGroupBy = ['state', 'city', 'year', 'month']
    outputSheetName = "allCases.xlsx"
    internalSheetName = "cases"
    processSheets(inputSheets \
                  , workingPath + outputFilesPath \
                  , columnsOfNewSheet \
                  , columnsOfGroupBy \
                  , outputSheetName \
                  , internalSheetName \
                  )

    # Wait for the user input to terminate the program
    # input("Press any key to terminate the program")
