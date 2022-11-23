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
        new_columns = input_serie['new_columns']
        group_order = input_serie['group_order']
        output_file = input_serie['output_file']
        name = input_serie['name']

        # message in the console
        print("\n----------------------------------------------")
        print(f"1) Processing input data for {name}")
        print()

        # reading the sheet
        raw_data = pd.read_excel(input_files)

        xxxxxxxxx = 0

        # adding new column with year and month together
        # raw_data['year_month'] = raw_data['month'].astype(str).zfill(2)
        # raw_data['year_month'] = raw_data['month'].astype(str).zfill(2)
        # raw_data['year_month'] = raw_data['year']
        # raw_data['year_month'] = raw_data['year'].to_string() + raw_data['year'].to_string()
        raw_data['year_month'] = (raw_data['year'].apply(lambda x: f"{x:04d}") + \
                                  raw_data['month'].apply(lambda x: f"{x:02d}")).astype(int)

        # setting years and months to process
        years = [2021, 2022]
        months = [0, 3, 6, 9, 12]  # Always maintain 0 and other number here

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

        # initializing new array
        vaccination_ratio = np.zeros(rows_columns * rows_columns).reshape(rows_columns, rows_columns)
        statistics = []

        # Divide data by month
        for year in years:
            for month in range(len(months) - 1):
                year_month = int(str(year) + str(month + 1).zfill(2))
                year_month_data = raw_data[raw_data['year_month'] <= year_month].reset_index(drop=True)

                # year_data = raw_data[raw_data['year'] <= year].reset_index(drop=True)
                # month_data = year_data[year_data['month'] > months[month]].reset_index(drop=True)
                # month_data = month_data[month_data['month'] <= months[month + 1]].reset_index(drop=True)

                # initializing new array
                vaccination_ratio = np.zeros(rows_columns * rows_columns).reshape(rows_columns, rows_columns)

                print(f"2) Calculating the total sum of vaccination doses")
                print()

                # group data summarizing number of vaccines of each city
                month_summarized = year_month_data[new_columns].groupby(group_order, as_index=False).sum()

                # processing each city to calculate the summary of the doses
                for city_index, city_row in cities.iterrows():
                    city = month_summarized.loc[month_summarized['ibgeID'] == city_row['ibgeID']]
                    for index, row in city.iterrows():
                        # adding new columns for doses
                        cities._set_value(city_index, 'dose_' + str(row['dose']), (row['count'] / row['pop2021']))

                # saving cities with doses sum
                output_file_cities_xlsx = output_file + "_cities_" + str(year) + "_" + str(month) + ".xlsx"
                cities.to_excel(output_file_cities_xlsx, index=False)

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

                print(f"3) Calculating the proximity ratio between cities")
                print()

                # calculation of ratio proximity between cities
                for origin_index in range(0, number_of_cities - 1):
                    print(f'origin index {origin_index}')

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

                print(f"4) Saving results")
                print()

                # removing output file if exists
                output_file_csv = output_file + "_" + str(year) + "_" + str(month) + ".csv"
                if os.path.exists(output_file_csv):
                    os.remove(output_file_csv)

                # defining excel file
                # output_file_xlsx = output_file + '.xlsx'
                # if os.path.exists(output_file_xlsx):
                #     os.remove(output_file_xlsx)

                # saving the array
                print(f"Saving results in CSV format: {output_file_csv}")
                np.savetxt(output_file_csv, vaccination_ratio, delimiter=",")

                # convert array into a dataframe to save in Excel format
                # print(f"Saving results in Excel format: {output_file_xlsx}")
                # df = pd.DataFrame(vaccination_ratio)
                # df.to_excel(output_file_xlsx, index=False)


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

    # initializing names
    input_filename = "vaccination.xlsx"
    output_filename = "vaccination_ratio"

    # vaccination data
    input_data.append({
        'input_files': inputs_path + input_filename,
        'cities': cities,
        'new_columns': ['state', 'city', 'ibgeID', 'pop2021', 'dose', 'count'],
        'group_order': ['state', 'city', 'ibgeID', 'pop2021', 'dose'],
        'output_file': outputs_path + output_filename,
        'name': "vaccination_ratio",
    })

    # calculating the vaccination ratio
    calculateVaccinationRatio(input_data)

    # Wait for the user input to terminate the program
    # input("Press any key to terminate the program")
    # xxxxxxxxxxx