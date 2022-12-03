"""
Project: Final Project Vaccination
Professor: João Meidanis
Students: Pedro Henrique Di Francia Rosso and Rubens de Castro Pereira
Date: 24/10/2022
Version: 1.0.0
Function:
1) Calculate the sum of doses per city.
2) Calculate the ratio proximity between cities from the summarized data.
"""

# ###########################################
# Importing needed libraries
# ###########################################

# importing python packages and modules
import os
import numpy as np
import pandas as pd


# ###########################################
# Application Methods
# ###########################################


def calculateVaccinationRatio(input_data):
    # Input data now contains all information we want to process, so, let us iterate each of them
    for input_serie in input_data:
        # to work better
        input_files = input_serie['input_files']
        cities = input_serie['cities']
        outliers_cities = input_serie['outliers_cities']
        new_columns = input_serie['new_columns']
        group_order = input_serie['group_order']
        output_path = input_serie['output_path']
        output_files = input_serie['output_files']
        output_file_vaccination_ratio = output_files[0]
        output_file_city_doses = output_files[1]
        name = input_serie['name']

        # message in the console
        print("\n----------------------------------------------")
        print(f"1) Processing input data for {name}")
        print()

        # reading the sheet
        raw_data = pd.read_excel(input_files)

        # removing outliers cities of raw data
        for ibgeID in outliers_cities:
            raw_data_indexes = raw_data.loc[raw_data['ibgeID'] == ibgeID].index
            raw_data = raw_data.drop(index=raw_data_indexes)
        raw_data = raw_data.reset_index()

        # adding new column with year and month together
        raw_data['year_month'] = (raw_data['year'].apply(lambda x: f"{x:04d}") + \
                                  raw_data['month'].apply(lambda x: f"{x:02d}")).astype(int)

        # setting years and months to process
        years = [2021, 2022]
        months = [3, 6, 9, 12]  # Always maintain 0 and other number here

        # removing outliers cities
        for ibgeID in outliers_cities:
            city_index = cities.loc[cities['ibgeID'] == ibgeID].index
            cities = cities.drop(index=city_index)
        cities = cities.reset_index()

        # get the number of cities
        number_of_cities = len(cities)
        rows_columns = number_of_cities + 1

        # adding new columns to the cities dataframe
        cities['dose_0'] = 0
        cities['dose_1'] = 0
        cities['dose_2'] = 0
        cities['dose_3'] = 0
        cities['dose_4'] = 0
        cities['dose_5'] = 0

        # Divide data by month
        for year in years:
            for month in months:
                year_month = int(str(year) + str(month).zfill(2))
                year_month_data = raw_data[raw_data['year_month'] <= year_month].reset_index(drop=True)

                # initializing new array
                vaccination_ratio = np.zeros(rows_columns * rows_columns, dtype="float32").reshape(rows_columns,
                                                                                                   rows_columns)

                print(f"2) Calculating the total sum of vaccination doses: {year}-{month}")
                print()

                # group data summarizing number of vaccines of each city
                month_summarized = year_month_data[new_columns].groupby(group_order, as_index=False).sum()

                # processing each city to calculate the summary of the doses
                for city_index, city_row in cities.iterrows():
                    # # disregarding outliers cities
                    # if city_row['ibgeID'] in outliers_cities:
                    #     continue

                    city = month_summarized.loc[month_summarized['ibgeID'] == city_row['ibgeID']]
                    for index, row in city.iterrows():
                        # adding new columns for doses
                        cities._set_value(city_index, 'dose_' + str(row['dose']), (row['count'] / row['pop2021']))

                # saving cities with doses sum
                output_file_city_doses_csv = output_path + output_file_city_doses + "_" + str(year) + "_" + str(
                    month) + ".csv"
                cities.to_csv(output_file_city_doses_csv, index=False)

                # getting the series doses
                ibgeID = cities['ibgeID']
                doses_0 = cities['dose_0']
                doses_1 = cities['dose_1']
                doses_2 = cities['dose_2']
                doses_3 = cities['dose_3']
                doses_4 = cities['dose_4']
                doses_5 = cities['dose_5']

                # setting ibgeID of the two cities
                for index in range(0, number_of_cities):
                    vaccination_ratio[index + 1][0] = ibgeID[index]
                    vaccination_ratio[0][index + 1] = ibgeID[index]

                print(f"3) Calculating proximity ratio between cities")
                print()

                # calculation of ratio proximity between cities
                for origin_index in range(0, number_of_cities - 1):
                    print(f'{year}_{month} - origin city index {origin_index}')

                    for target_index in range(origin_index + 1, number_of_cities):
                        # print(f'target index {target_index}')

                        # calculating the proximity ratio
                        proximity_ratio = np.abs((doses_0[origin_index] + doses_1[origin_index]) -
                                                 (doses_0[target_index] + doses_1[target_index]))

                        # proximity_ratio = calculateEuclideanDistance( \
                        #     doses_0[origin_index], doses_1[origin_index], doses_2[origin_index], \
                        #     doses_3[origin_index], doses_4[origin_index], doses_5[origin_index], \
                        #     doses_0[target_index], doses_1[target_index], doses_2[target_index], \
                        #     doses_3[target_index], doses_4[target_index], doses_5[target_index] \
                        #     )

                        # setting the proximity ratio of two cities
                        vaccination_ratio[origin_index + 1][target_index + 1] = proximity_ratio
                        vaccination_ratio[target_index + 1][origin_index + 1] = proximity_ratio

                print()
                print(f"4) Saving results")
                print()

                # removing output file if exists
                output_file_vaccination_ratio_csv = output_path + output_file_vaccination_ratio + "_" + \
                                                    str(year) + "_" + str(month) + ".csv"
                if os.path.exists(output_file_vaccination_ratio_csv):
                    os.remove(output_file_vaccination_ratio_csv)

                # saving the array
                print(f"Saving results in CSV format: {output_file_vaccination_ratio_csv}")
                np.savetxt(output_file_vaccination_ratio_csv, vaccination_ratio, delimiter=",", fmt='%1.6f')


def calculateEuclideanDistance( \
        origin_dose_0, origin_dose_1, origin_dose_2, origin_dose_3, origin_dose_4, origin_dose_5, \
        target_dose_0, target_dose_1, target_dose_2, target_dose_3, target_dose_4, target_dose_5 \
        ):
    # calculating the distance
    distance = np.sqrt( \
        np.power((origin_dose_0 - target_dose_0), 2) \
        + np.power((origin_dose_1 - target_dose_1), 2) \
        + np.power((origin_dose_2 - target_dose_2), 2) \
        + np.power((origin_dose_3 - target_dose_3), 2) \
        + np.power((origin_dose_4 - target_dose_4), 2) \
        + np.power((origin_dose_5 - target_dose_5), 2) \
        )

    # returning the distance
    return distance


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # setting paths and file names
    root_path = os.getcwd().replace("\\", "/") + "/../"
    data_path = root_path + 'data/'

    inputs_path = data_path + 'output/'
    outputs_path = data_path + 'calculations/'

    # serie that describe files to read
    input_data = []

    # statistic of processing
    statistics = []

    # reading all cities
    input_cities = inputs_path + "city.xlsx"
    cities = pd.read_excel(input_cities)

    # reading all cities
    input_outliers_cities = inputs_path + "outliers.xlsx"
    outliers_cities = pd.read_excel(input_outliers_cities)
    outliers_cities_list = outliers_cities['ibgeID'].values.tolist()

    # initializing names
    input_filename = "vaccination.xlsx"
    output_filename = "vaccination_ratio"

    # vaccination data
    input_data.append({
        'input_files': inputs_path + input_filename,
        'cities': cities,
        'outliers_cities': outliers_cities_list,
        'new_columns': ['state', 'city', 'ibgeID', 'pop2021', 'dose', 'count'],
        'group_order': ['state', 'city', 'ibgeID', 'pop2021', 'dose'],
        'output_path': outputs_path,
        'output_files': ["vaccination_ratio", "city_doses"],
        'name': "vaccination_ratio",
    })

    # calculating the vaccination ratio
    calculateVaccinationRatio(input_data)
