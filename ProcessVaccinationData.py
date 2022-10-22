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

            # calculate the total number of vaccinations by city
            dfStateVaccinationsGroupedByCity = dfStateVaccinations[['state', 'city', 'count']].groupby(
                ['city', 'state']).sum()

            # adding dataframe of all states of Brazil
            dfAllStatesOfBrazil = pd.concat([dfAllStatesOfBrazil, dfStateVaccinationsGroupedByCity])

            # message showing processing the state
            print("Processing state", state)

        except:
            # nothing to do
            pass

        # remove output file if exists
        outputFilename = "allStatesOfBrazil.xlsx"
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

    # processing vaccination data
    processVaccinationSheets(workingPath + inputFilesPath \
                             , workingPath + outputFilesPath \
                             , dfStatesOfBrazil \
                             , vaccinationDatasetUrl \
                             )

    # Wait for the user input to terminate the program
    # input("Press any key to terminate the program")
