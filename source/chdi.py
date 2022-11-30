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
from urllib import request
from unidecode import unidecode

# ###########################################
# Application Methods
# ###########################################
def getCHDIClass(chdi):
    if chdi < 0.5:
        return 0
    elif chdi < 0.6:
        return 1
    elif chdi < 0.7:
        return 2
    elif chdi < 0.8:
        return 3
    else:
        return 4


def processData(input_data, cities):
    # Input data now contains all information we want to process, so, let us iterate each of them
    for input_serie in input_data:
        # To work better
        input_files = input_serie['input_files']
        output_file = input_serie['output_file']
        classes_file = input_serie['classes_file']
        name = input_serie['name']

        print("\n----------------------------------------------")
        print(f"Processing input data for {name}")

        processed_data = pd.DataFrame()

        years = [2020, 2021, 2022]
        months = [0, 3, 6, 9, 12] # Always maintain 0 and other number here
        for sheet in input_files:
            try:
                # Read file
                raw_data = pd.read_excel(sheet)
                
                # convert city names to lowercase and put state in format (XX)
                cities['city'] = list(x.split("/")[-2].lower() + " (" + x.split("/")[-1].lower() + ")" for x in cities['city'].values)

                # put all city names to same codification
                cities['city'] = list(unidecode(x) for x in cities['city'])
                raw_data['Territorialidade'] = list(unidecode(x) for x in raw_data['Territorialidade'])

                # add ibgeID to the CHDI dataframe
                raw_data['ibgeID'] = list(cities[cities['city'] == x.lower()]['ibgeID'].values for x in raw_data['Territorialidade'].values) 

                # remove unmatched rows
                raw_data['ibgeID'] = list(x[0] if len(x) > 0 else 0 for x in raw_data['ibgeID'])
                processed_data = raw_data[raw_data['ibgeID'] != 0]

                # calculate classes
                classes = list(getCHDIClass(x) for x in raw_data['IDHM'])

                # Create a period (equal in all periods) dataframe with classes
                classes_chdi = pd.DataFrame()
                for year in years:
                    for month in range(len(months) - 1):
                         classes_chdi["(" + str(months[month] + 1) + "-" + str(months[month + 1]) + ")/" + str(year)] = classes

                classes_chdi.index = raw_data['ibgeID']

                # message showing processing the state
                print("Processed sheet: ", sheet.split('/')[-1])

            except:
                pass

        # removing output file if exists
        if os.path.exists(output_file):
            os.remove(output_file)
        if os.path.exists(classes_file):
            os.remove(classes_file)

        # saving sheet
        with pd.ExcelWriter(output_file, mode='w', ) as writer:
            processed_data.to_excel(writer, sheet_name=name)
        # saving sheet
        with pd.ExcelWriter(classes_file, mode='w', ) as writer:
            classes_chdi.to_excel(writer, sheet_name=name)


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

    # Series that describe files to read
    input_data = []

    # List of files that describe Covid Cases and deaths data
    chdi_files = []
    chdi_files.append(inputs_path + 'chdi.xlsx')
    
    # get information about cities
    cities = pd.read_excel(outputs_path + "city.xlsx")

    # Vaccination data
    input_data.append({
        'input_files': chdi_files,
        'output_file': outputs_path + "chdi.xlsx",
        'classes_file': calculations_path + "classes_chdi.xlsx",
        'name': "CHDI",
    })

    # This processes all the input files described before
    processData(input_data, cities)