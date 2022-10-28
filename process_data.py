"""
Project: Final Project - Covid19 Vaccination
Professor: João Meidanis
Students: Pedro Henrique Di Francia Rosso and Rubens de Castro Pereira
Date: 21/10/2022
Version: 1.0.0
Function: Process raw data of vaccination, covid cases and covid death
"""

# ###########################################
# Importing Libraries
# ###########################################
import os
import pandas as pd


# ###########################################
# Application Methods
# ###########################################
def getBrazilianStates(file_path):
    return pd.read_excel(file_path)


def processData(input_data):
    statistics_list = []

    # Input data now contains all information we want to process, so, let us iterate each of them
    for input_serie in input_data:
        # To work better
        input_files = input_serie['input_files']
        new_columns = input_serie['new_columns']
        group_order = input_serie['group_order']
        output_file = input_serie['output_file']
        name = input_serie['name']

        print("\n----------------------------------------------")
        print(f"Processing input data for {name}")

        processed_data = pd.DataFrame()

        for sheet in input_files:
            try:
                # Read file
                raw_data = pd.read_csv(
                    sheet, compression='gzip', header=0, sep=',', quotechar='"')

                # Add statistics for this file
                statistics_item = [name, sheet, len(raw_data)]
                statistics_list.append(statistics_item)

                # if there is a "data" col, transform into year/month
                try:
                    raw_data['year'] = pd.DatetimeIndex(raw_data['date']).year
                    raw_data['month'] = pd.DatetimeIndex(raw_data['date']).month
                except:
                    pass

                # Group the raw data
                grouped_data = raw_data[new_columns].groupby(
                    group_order, as_index=False).sum()

                # Concatenate with the final result
                processed_data = pd.concat([processed_data, grouped_data])

                # message showing processing the state
                print("Processed sheet: ", sheet.split('/')[-1])

            except:
                pass

        # removing output file if exists
        if os.path.exists(output_file):
            os.remove(output_file)

        # saving sheet
        with pd.ExcelWriter(output_file, mode='w', ) as writer:
            processed_data.to_excel(writer, sheet_name=name)

    return pd.DataFrame(
        statistics_list, columns=['subject', 'sheet', 'number of rows'])


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # setting paths and file names
    root_path = os.getcwd().replace("\\", "/") + "/../"
    data_path = root_path + 'data/'

    inputs_path = data_path + 'input/'
    outputs_path = data_path + 'output/'

    # getting states of Brazil
    brazilian_states = getBrazilianStates(inputs_path + 'states_of_brazil.xlsx')

    # Series that describe files to read
    input_data = []

    # List of files that describe vaccination data
    vaccination_files = []
    for state in brazilian_states["initials"]:
        vaccination_files.append(
            inputs_path + 'processed_' + state.strip() + '.csv.gz')

    # List of files that describe Covid Cases and deaths data
    covid_files = []
    covid_files.append(inputs_path + 'cases-brazil-cities-time_2020.csv.gz')
    covid_files.append(inputs_path + 'cases-brazil-cities-time_2021.csv.gz')
    covid_files.append(inputs_path + 'cases-brazil-cities-time.csv.gz')

    # Vaccination data
    input_data.append({
        'input_files': vaccination_files,
        'new_columns': ['state', 'city', 'ibgeID', 'pop2021', 'year', 'month', 'count'],
        'group_order': ['state', 'city', 'ibgeID', 'pop2021', 'year', 'month'],
        'output_file': outputs_path + "vaccination.xlsx",
        'name': "Vaccination",
    })

    # City data
    input_data.append({
        'input_files': vaccination_files,
        'new_columns': ['state', 'city', 'ibgeID', 'pop2021'],
        'group_order': ['state', 'city', 'ibgeID', 'pop2021'],
        'output_file': outputs_path + "city.xlsx",
        'name': "City",
    })

    # Covid Deaths data
    input_data.append({
        'input_files': covid_files,
        'new_columns': ['state', 'city', 'ibgeID', 'year', 'month', 'newDeaths'],
        'group_order': ['state', 'city', 'ibgeID', 'year', 'month'],
        'output_file': outputs_path + "covid_deaths.xlsx",
        'name': "Covid Deaths",
    })

    # Covid Deaths data
    input_data.append({
        'input_files': covid_files,
        'new_columns': ['state', 'city', 'ibgeID', 'year', 'month', 'newCases'],
        'group_order': ['state', 'city', 'ibgeID', 'year', 'month'],
        'output_file': outputs_path + "covid_cases.xlsx",
        'name': "Covid Cases",
    })

    # This processes all the input files described before
    statistics = processData(input_data)

    # saving statistic sheet
    statistic_output = outputs_path + 'processing_statistics.xlsx'
    with pd.ExcelWriter(statistic_output, mode='w', ) as writer:
        statistics.to_excel(writer)
