"""
Project: Final Project - Covid19 Vaccination
Professor: João Meidanis
Students: Pedro Henrique Di Francia Rosso and Rubens de Castro Pereira
Date: 21/10/2022
Version: 1.0.0
Function: Generate graphs
"""

# ###########################################
# Importing Libraries
# ###########################################
import os
import pandas as pd
import numpy as np


# ###########################################
# Library Methods
# ###########################################


def getClasses(data_series, number_of_classes, cities):
    '''
    Returns classes between 0 and 1
    '''
    for input_serie in data_series:
        # To work better
        input_files = input_serie['input_files']
        new_columns = input_serie['new_columns']
        group_order = input_serie['group_order']
        output_file = input_serie['output_file']
        selections = input_serie['selections']
        target =input_serie['target']
        name = input_serie['name']

        print("\n----------------------------------------------")
        print(f"Processing data for {name}")

        years = [2020, 2021, 2022]
        months = [0, 3, 6, 9, 12] # Always maintain 0 and other number here
        data_by_time = cities
        for sheet in input_files:
            # Read file
            print(f"Reading data from {sheet}")
            raw_data = pd.read_excel(sheet)

            # Remove non-cities
            raw_data = raw_data[raw_data['ibgeID'] > 100].reset_index(drop=True)

            # Special selection
            for selection in selections:
                selection_data = pd.DataFrame()
                for value in selection['values']:
                    value_data = raw_data[raw_data[selection['target']] == value].reset_index(drop=True)
                    selection_data = pd.concat([selection_data, value_data], axis=0)
                raw_data = selection_data

            # Divide data by month
            for year in years:
                for month in range(len(months) - 1):
                    year_data = raw_data[raw_data['year']
                                         == year].reset_index(drop=True)
                    month_data = year_data[year_data['month']
                                           > months[month]].reset_index(drop=True)
                    month_data = month_data[month_data['month']
                                            <= months[month + 1]].reset_index(drop=True)

                    # remove negative values
                    month_data[target] = np.where(month_data[target] < 0, 0, month_data[target])

                    # group data by city and add pop
                    grouped_month_data = month_data[new_columns].groupby(
                        group_order, as_index=False).sum()
                    grouped_month_data = pd.DataFrame(list(grouped_month_data[target]), columns=[target], index=grouped_month_data['ibgeID'])

                    grouped_month_data = pd.concat(
                        [cities, grouped_month_data], axis=1)

                    grouped_month_data[target] = np.where(pd.isnull(grouped_month_data[target]), 0, grouped_month_data[target])

                    # calculate classes
                    class_division = (1 / (number_of_classes - 1)) * 10 
                    grouped_month_data['class_value'] = (grouped_month_data[target] / grouped_month_data['pop'])
                    max_value = grouped_month_data['class_value'].max()
                    if max_value > 0:
                        grouped_month_data['class'] = (grouped_month_data['class_value'] / max_value) * 10
                        grouped_month_data['class'] = np.floor(grouped_month_data['class'] / class_division)
                    else:
                        grouped_month_data['class'] = grouped_month_data['class_value'] * 0

                    final_mont_data = pd.DataFrame(list(grouped_month_data['class']), columns=[
                                                "(" + str(months[month] + 1) + "-" + str(months[month + 1]) + ")/" + str(year)], index=grouped_month_data.index)

                    # append in final result
                    data_by_time = pd.concat([data_by_time, final_mont_data], axis=1)

        # removing output file if exists
        if os.path.exists(output_file):
            os.remove(output_file)

        # saving sheet
        with pd.ExcelWriter(output_file, mode='w', ) as writer:
            data_by_time.to_excel(writer, sheet_name=name)


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # setting paths and file names
    root_path = os.getcwd().replace("\\", "/") + "/../"
    data_path = root_path + 'data/'

    inputs_path = data_path + 'input/'
    outputs_path = data_path + 'output/'
    calculations_path = data_path + 'calculations/'


    # get information about cities
    cities = pd.read_excel(outputs_path + "city.xlsx")
    cities = pd.DataFrame(list(cities['pop2021']), columns=['pop'], index=cities['ibgeID'])

    # Series that describe files to read
    data_series = []

    # Cases data
    data_series.append({
        'input_files': [outputs_path + "covid_cases.xlsx"],
        'new_columns': ['ibgeID', 'newCases'],
        'group_order': ['ibgeID'],
        'selections': [],
        'target': 'newCases',
        'output_file': calculations_path + "classes_cases.xlsx",
        'name': "Cases Classes",
    })

    # Deaths data
    data_series.append({
        'input_files': [outputs_path + "covid_deaths.xlsx"],
        'new_columns': ['ibgeID', 'newDeaths'],
        'group_order': ['ibgeID'],
        'selections': [],
        'target': 'newDeaths',
        'output_file': calculations_path + "classes_deaths.xlsx",
        'name': "Deaths Classes",
    })

    # Vaccination data
    data_series.append({
        'input_files': [outputs_path + "vaccination.xlsx"],
        'new_columns': ['ibgeID', 'count'],
        'group_order': ['ibgeID'],
        'selections': [{'target': 'dose', 'values': [0, 1] }],
        'target': 'count',
        'output_file': calculations_path + "classes_vaccination.xlsx",
        'name': "Vaccination Classes",
    })


    # This processes all the input files described before
    getClasses(data_series, 5, cities)

