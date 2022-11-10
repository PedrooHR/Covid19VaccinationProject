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


def calculateVaccinationRadio(input_data, output_files_path, output_sheet_name, internal_sheet_name):
    # message in the console
    print()
    print("----------------------------------------------")
    print("Processing ", input_data)
    print()

    # initializing new dataframe
    result = pd.DataFrame()
    statistics = []

    # reading sheet
    # dfSheet = pd.read_excel(inputSheet, header=0, sep=',', quotechar='"')
    sheet = pd.read_excel(input_data)

    # group data summarizing number of vaccines of each city
    columns_of_new_sheet = ['state', 'city', 'ibgeID', 'pop2021', 'count']
    columns_of_group_by = ['state', 'city', 'ibgeID', 'pop2021']
    vaccinations = sheet[columns_of_new_sheet].groupby(columns_of_group_by, as_index=False).sum()

    # auxiliary list of results
    euclidean_distances = []

    # calculation of euclidean distance between all cities of Brazil
    for origin_index in range(0, len(vaccinations) - 1):
        # if (origin_index > 100):
        #     break

        for target_index in range(origin_index + 1, len(vaccinations)):
            # processing cities in the same state
            # if (dfVaccinationsGroupedByCity['state'].iloc[origin_index] != \
            #         dfVaccinationsGroupedByCity['state'].iloc[target_index]):
            #     continue

            # calculating the euclidean distance bewtween two cities
            euclidean_distance = calculateEuclideanDistance( \
                vaccinations['count'].iloc[origin_index] \
                , vaccinations['pop2021'].iloc[origin_index] \
                , vaccinations['count'].iloc[target_index] \
                , vaccinations['pop2021'].iloc[target_index] \
                )

            # if (euclideanDistance < 0.5):
            item_euclidean_distance = [ \
                vaccinations['state'].iloc[origin_index] \
                , vaccinations['city'].iloc[origin_index] \
                , vaccinations['ibgeID'].iloc[origin_index] \
                , vaccinations['state'].iloc[target_index] \
                , vaccinations['city'].iloc[target_index] \
                , vaccinations['ibgeID'].iloc[target_index] \
                , euclidean_distance \
                ]
            euclidean_distances.append(item_euclidean_distance)

    # removing output file if exists
    if os.path.exists(output_files_path + output_sheet_name):
        os.remove(output_files_path + output_sheet_name)

    # saving sheet
    result_euclidean_distance = pd.DataFrame( \
        euclidean_distances, columns=[ \
            'origin state', 'origin city', 'origin ibge id' \
            , 'target state', 'target city', 'target ibge id' \
            , 'distance'] \
        )
    # with pd.ExcelWriter(outputFilesPath + outputSheetName, mode='w', ) as writer:
    #     dfEuclideanDistanceOfCity.to_excel(writer)
    result_euclidean_distance.to_csv(output_files_path + output_sheet_name, encoding='utf-8')


def calculateEuclideanDistance(origin_city_vaccine_count, origin_city_population, \
                               target_city_vaccine_count, target_city_population):
    # calculating percentages
    origin_percentage = (origin_city_vaccine_count / 4) / origin_city_population
    target_percentage = (target_city_vaccine_count / 4) / target_city_population

    # calculating the distance
    distance = math.sqrt(math.pow((origin_percentage - target_percentage), 2))

    # returning the distance
    return distance


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # setting paths and file names
    root_path = os.getcwd().replace("\\", "/") + "/../"
    working_path = root_path + 'data/'

    input_files_path = '02-Output Files/'
    output_files_path = '03-Calculations/'

    # statistic of processing
    statistics = []

    input_sheet_name = "Vaccination.xlsx"
    output_sheet_name = "VaccinationRatioProximity.csv"
    internal_sheet_name = "VaccinationRatioProximity"
    calculateVaccinationRadio(working_path + input_files_path + input_sheet_name \
                              , working_path + output_files_path \
                              , output_sheet_name \
                              , internal_sheet_name \
                              )

    # Wait for the user input to terminate the program
    # input("Press any key to terminate the program")
    # xxxxxxxxxxx
