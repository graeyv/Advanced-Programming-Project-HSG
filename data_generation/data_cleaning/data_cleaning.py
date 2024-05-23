"""
read all the csv in the windows folder. 
"""
# import packages
import re
import os
import pandas
import random
import numpy as np
import csv
from pyproj import Proj, transform

# path to data
folder_path = r"PATH TO FOLDER WITH FILES 'raw_data_immoscout'"

# get a list of the names of all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# initialization to store all d
data_list = []

# read each file and append it to a list
for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    df = pandas.read_csv(file_path)
    data_list.append(df)

# extract all data (56 files) into one dataframe "data"
data = pandas.concat(data_list, ignore_index=True)

# for better overview, delete all variables other than "data"
del csv_file, csv_files, data_list, df, file_path, folder_path

"""
1. price

Result:
    Ratios Price data / True Price:
    1.284	 1.296	1.314	 1.284 1.296 1.314 1.314 1.314 1.314 1.314 1.314 1.284 1.284
    Conclusion: We take 1.3 as approximation
"""

# filter out all rows that have no prices
data = data[data['price'] != 'auf Anfrage'] # 5918 rows removed

# replace ".-" with " " and make it numerical
data['price'] = data['price'].str.replace('.–', '').astype(int)

# remove rows that have prices < 100'000 as it seems like the price given
# there is just a place-holder or anomalies
data = data[data['price'] >= 100000]
# 78 rows removed

# randomly choose 10 rows and compare prices from data with advertisement (true prices)
random.seed(1)
price_check = data.sample(50, random_state=1)  # randomly choose 50 rows
price_check = price_check[["street", "PLZ", "price"]] # select rows relevant for this test
price_check = price_check.dropna(subset=["street"]) # drop missing values in test dataframe

data['price'] /= 1.3 # divide price by 1.3 as approximation of true price

del price_check # delete variable for better overview

"""
2. number of rooms 

Result:
    Getting a sample of each number of rooms and check with website.
    No pattern recognized - number of rooms will be dropped.
 
[number of rooms data 2 : (4	 4	 4	3	4	3	1) in advertisements ]
[number of rooms data 2.5: (4.5	3.5	4.5	4.5	4.5	4.5	4.5	3.5	4.5	4.5) in adv.]
[number of rooms data 3: (7 6	5	5	5	6	5	5	5	6) in adv.]
[number of rooms data 3.5: (5.5	5.5	5.5	5.5	2.5	2.5	2.5	5.5	5.5	6.5) in adv.]
[number of rooms data 4: (9	 9	8	9	9	9) in adv.]
"""

# remove number of rooms in the data
data = data.drop('number_of_rooms', axis=1)

"""
3. Living area

Result:
    Irregularities in ratio. We did following approximations:
        - Living area data > 120: Ratio = 1.2
        - Living area < 120: Ratio = 0.65
"""

# remove rows with missing value in living area
data = data.dropna(subset=["living_area"]) # 2618 rows removed

# replace ".-" and " m²" with and empty string make it numerical
data['living_area'] = data['living_area'].astype(str).str.replace(' m²', '') # replacements
data['living_area'] = pandas.to_numeric(data['living_area'], errors='coerce') # make it numerical

# take a random sample and compare values
area_check = data.sample(50, random_state=1)  # randomly choose 50 rows
area_check = area_check[["street", "PLZ", "price", "living_area"]] # select rows relevant for this test
area_check = area_check.dropna(subset=["street"]) # drop missing values in test dataframe
area_check = area_check.sort_values(by="living_area", ascending=False)
true_living_areas = [249, 200, 1, 158, 148, 141, 1, 117, 119, 124, 110, 115, 100, 110, 91, 1, 68, 74, 73] # 1 = not available
area_check["true_living_areas"] = true_living_areas
area_check["ratio"] = area_check["living_area"] / area_check["true_living_areas"]

del area_check, true_living_areas

"""
We see that ratio between true living area / living area data is stable in intervalls
living area 130-310: ratio is around 1.25
living area 52-70: ratio around 0.75
living area 41-43: ratio around 0.57

As above further checks where made for other ranges:
    - Top 10 values in area: Values : 1.314	1.296	1.296	1.313541667	1.295206056	1.29529182	1.293375394
    - Values between 70 and 130 - unique values = (120, 76, 75, 74, 73, 72, 71, 70)
    - Living area = 120 --> resulted ratios between 1.14 and 1.2 ()
      [ Results for "data[data['living_area'] == 120].sample(n=10, random_state=1 )":
       (1.188118812	1.142857143	1.188118812	1.153846154 ]
    - Living area between 70 and 76 --> resulted ratios between 0.72 and 0.77
      [ results for 'data[(data['living_area'] >= 70) & (data['living_area'] <= 76)].sample(n=20, random_state=1)':
       0.724489796	0.767676768	0.736842105	0.768421053	0.765957447	0.760416667	0.768421053	0.76344086	0.765306122 ]
    - Living area between 40 and 70 --> resulted in values between 0.72 and some exceptions at 0.56
      [ Results for 'data[(data['living_area'] >= 40) & (data['living_area'] < 70)].sample(
          n=50, random_state=1).sort_values(by='living_area'):
        0.73	0.77	0.77	0.56	0.56	0.77	0.76	0.76	0.77	0.76	0.76	0.76	0.77	0.72	0.76	0.73	0.76	0.77	0.77	0.77 ]
    - Living area between 20 and 39 --> restulted in values between 0.56 and 0.8
      Results for 'data[(data['living_area'] >= 20) & (data['living_area'] < 39)].sample(
          n=50, random_state=1).sort_values(by='living_area')':
       0.8	 0.8	0.77	0.78	0.78	0.57	0.77	0.78	0.57	0.56	0.77	0.57	0.77	0.57	0.77	0.56]
"""

"""
Transform data living area.
Following approximations are done:
    Living area data > 120: Ratio = 1.2
    Living area < 120: Ratio = 0.65
"""

data['living_area'] = data['living_area'].apply( # divide by 1.2 if > 120 and else by 0.65
lambda area: area / 1.2 if area >= 120 else area / 0.65) 

"""
4. Construction Year

Result:
    Construction Year is correct
"""
# check for strange values
construction_observations = data['construction_year'].value_counts() # values 2223 and 2107 detected
wrong_values = [2223, 2107]
corrected_values = [2023, 2017]
# replace wrong values by corrected values
for wrong_value, corrected_value in zip(wrong_values, corrected_values):
    data.loc[data['construction_year'] == wrong_value,
             'construction_year'] = corrected_value

# check number of missing values
missing_values_construction_year = data['construction_year'].isna().sum() # 7173 missing

# check median and mode for decision on how to handle missing values
median_construction = data['construction_year'].median()  # 2009
mode_construction_year = data['construction_year'].mode()  # 2024

# as both median and mode are rather new, we assume missing values to be "new constructions"

"""
We introduce a new categorical variable with following criteria:
    New Construction: >2010
    Modern Buildings: 1980-2010
    Old Buildings: 1900-1979
    Historic Houses: <1900
"""

# List with all categories needed for a mapping in a second step
categories = {
    'New Construction': lambda year: 'New Construction' if year > 2010 else None,
    'Modern Buildings': lambda year: 'Modern Buildings' if 1980 <= year <= 2010 else None,
    'Old Buildings': lambda year: 'Old Buildings' if 1900 <= year <= 1979 else None,
    'Historic Houses': lambda year: 'Historic Houses' if year < 1900 else None
}

# apply the categorization function
data['construction_category'] = data['construction_year'].apply(lambda year: next(
    (label for label, func in categories.items() if func(year)), None))

# remove old col with construction year
data.drop(columns=['construction_year'], inplace=True)

# for data with missing construction_category, assume the building to be a new construction
data['construction_category'] = data['construction_category'].fillna('New Construction') # replace None with "New Construction"

# delete variables not needed anymore
del construction_observations, corrected_value, corrected_values, median_construction
del missing_values_construction_year, mode_construction_year, wrong_value, wrong_values

"""
Canton
"""
# read an excel which contains all PLZ with Canton
file_path = "PLZ.xlsx"
PLZ = pandas.read_excel(file_path)

# new colomn with PLZ and Location only
data['PLZ_only'] = data['PLZ'].str.extract(r'(\d+)') # extracts all digits
data['Location'] = data['PLZ'].str.extract(r'(\D+)') # extracts the rest
data['Location'] = data['Location'].str.strip() # remove leading adn trailing spaces

# dictionary mapping PLZ to canton
plz_to_canton = dict(zip(PLZ['PLZ'].astype(str), PLZ['Kanton ']))

# map PLZ values in data to canton according to dictionary above
data['canton'] = data['PLZ_only'].map(plz_to_canton)

# check wheter everything worked
canton_observations = data['canton'].value_counts()  # worked

# delete old col place_search
data.drop(columns=['place_search'], inplace=True)

# delete variables not needed anymore
del PLZ, plz_to_canton, canton_observations

"""
Other Variables - check missing values
"""
variables = ['land_area', 'volume', 'last_rennovation', 'number_of_appartments',
             'height_rooms', 'availability', 'object_type', 'number_of_floors']
# a lot of missing values except construction year
missing_values = {col: data[col].isna().sum() for col in variables}
remove = ['land_area', 'volume', 'last_rennovation', 'number_of_appartments',
          'height_rooms', 'availability', 'number_of_floors']
data = data.drop(columns=remove)

# delete variables not needed anymore
del missing_values, remove, variables

"""
Typologie:
    Urban Areas according to admin.ch
    We are assigning to each PLZ a category that is indicating wheter
    it is in an urban area or not. 
"""
# loading the data-  PLZ_ID is needed to assign a BFS-Nr. to every PLZ. 
# this is needed for the data from admin.ch
file_path = "ID_PLZ.csv"
PLZ_ID = pandas.read_csv(file_path, sep=";")
PLZ_ID['PLZ'] = PLZ_ID['PLZ'].astype(str) # convert to string

#create dictionaries for Gemeindename (Municipality name) and Ortschaftsname (Village name) and PLZ to BFS-Nr.
gemeindename_to_bfs = dict(zip(PLZ_ID['Gemeindename'], PLZ_ID['BFS-Nr']))
ortschaftsname_to_bfs = dict(zip(PLZ_ID['Ortschaftsname'], PLZ_ID['BFS-Nr']))
plz_to_bfs = dict(zip(PLZ_ID['PLZ'], PLZ_ID['BFS-Nr']))

# Update BFS-Nr. in data based on the mapping dictionaries
location = data['Location']
plz_only = data['PLZ_only']

bfs_nr_list = [] # empty list to store results

for loc, plz in zip(location, plz_only):
    bfs_nr = gemeindename_to_bfs.get(loc) # check wheter result found in dict. gemeindename_to_bfs
    if pandas.isnull(bfs_nr): # if not, check ortschaftsanme
        bfs_nr = ortschaftsname_to_bfs.get(loc)
        if pandas.isnull(bfs_nr): # if still not, check PLU
            bfs_nr = plz_to_bfs.get(plz)
    bfs_nr_list.append(bfs_nr)

data['BFS-Nr.'] = bfs_nr_list

missing_bfs_nr_rows = data[data['BFS-Nr.'].isna()]  # 6 rows missing
data = data.dropna(subset=['BFS-Nr.'])  # remove the rows with missing values

del bfs_nr, bfs_nr_list, loc, location, plz, plz_only, PLZ_ID, missing_bfs_nr_rows

# read data which assigns a category to each BFS-Nr.
file_path = "typologie.xlsx"
typologie = pandas.read_excel(file_path)
typologie = typologie.drop(index=list(range(0, 372)) + list(range(2503, 2514))) # drop rows not needed (first rows + rows for border areas (abroad))
typologie.columns = ['Region-ID', 'Name of region', 'type'] # rename colomns

data['BFS-Nr.'] = data['BFS-Nr.'].astype(float).astype(int).astype(str) # change in format of BFS-Nr.
typologie['Region-ID'] = typologie['Region-ID'].astype(str) 

# create a dictionary that maps from BFS-Nr. to region type
bfs_to_region_type = dict(zip(typologie['Region-ID'], typologie['type']))

# map the 'BFS-Nr.' in data to the 'type' in typologie
data['Region type'] = data['BFS-Nr.'].map(bfs_to_region_type)

# rename the values in "Region type" - add the order
region_type_mapping = {
    "Agglomerationskerngemeinde (Kernstadt)": "1: Agglomerationskerngemeinde (Kernstadt)",
    "Agglomerationskerngemeinde (Hauptkern)": "2: Agglomerationskerngemeinde (Hauptkern)",
    "Agglomerationskerngemeinde (Nebenkern)": "3: Agglomerationskerngemeinde (Nebenkern)",
    "Agglomerationsgürtelgemeinde": "4: Agglomerationsgürtelgemeinde",
    "Mehrfach orientierte Gemeinde": "5: Mehrfach orientierte Gemeinde",
    "Kerngemeinde ausserhalb Agglomerationen": "6 Kerngemeinde ausserhalb Agglomerationen",
    "Ländliche Gemeinde ohne städtischen Charakter": "7: Ländliche Gemeinde ohne städtischen Charakter"
}

data['Region type'] = data['Region type'].map(region_type_mapping)
missing_type_rows = data[data['Region type'].isna()]  # 4 rows missing
data.dropna(subset=['Region type'], inplace=True)  # drop missing values
type_counts = data['Region type'].value_counts()  # it worked

del type_counts, missing_type_rows

"""
Street names
"""
# remove the comma at the end of the street-name
data['street'] = data['street'].str.replace(',', '')

# drop missing values
data.dropna(subset=['street'], inplace=True)  # 17033 rows dropped
# drop rows that does not have any letters (placeholder-values for streetname)
data = data[data['street'].str.contains(r'[a-zA-Z]')]  # 2907 rows dropped

# drop rows that containt location name, 1496 rows dropped
data = data[~data.apply(lambda row: row['Location'].lower() in row['street'].lower(), axis=1)]  
# only selects row where location is not contained in street

# add number 1 if there is no number
def add_number_to_street(street):
    if not any(char.isdigit() for char in street):
        return street + '1'
    else:
        return street

# apply the function add_number_to_street to add housenumber
data['street'] = data['street'].apply(add_number_to_street)

# load data pure_str that contains all streets in switzerland
file_path = "pure_str.csv"
addresses = pandas.read_csv(file_path, delimiter=';')

# filter important cols and add an additional col with adresses without space and small letters (for comparison)
addresses = addresses[['STN_LABEL', 'ZIP_LABEL', 'COM_FOSNR']]
addresses.columns = ["Address", "PLZ", "BFS-Nr."]
addresses['formatted_address'] = addresses['Address'].str.replace(" ", "").str.lower()

# Keep that, otherwise error!
import pandas
import re 

addresses_data = data['street'].str.replace(" ", "").str.lower() # streetnames from our data 
addresses_data = addresses_data.apply(lambda x: re.sub(r'\d', '', x))  # remove all numbers in addresses_data (we only compare names in this step)
addresses_data = pandas.DataFrame({'street': addresses_data})  # convert back to DataFrame
addresses_data['new_column'] = None # initial value
addresses_data['BFS-Nr.'] = data['BFS-Nr.']

for index, row in addresses_data.iterrows(): # waring: for-loop takes about 30min to compute!
    # Get the street and BFS-Nr. from the current row
    street = str(row['street']).lower()
    bfs_nr = str(row['BFS-Nr.']).lower().replace(" ", "")

    # Filter addresses based on the BFS-Nr.
    corresponding_addresses = addresses[addresses['BFS-Nr.'].astype(str).replace(" ", "") == bfs_nr] # all adresses with this BFS-Nr.

    # initialize new_column value to record whether match is found
    new_column_value = 'No' # default value

    # check if the street is contained within any of the addresses in corresponding_addresses
    if corresponding_addresses['formatted_address'].str.contains(street, case=False).any(): # i matching address found
        # find the index where the street is contained in the formatted_address column
        match_index = corresponding_addresses[corresponding_addresses['formatted_address'].str.contains(street, case=False)].index[0]
        # assign the Address value from the matching index
        new_column_value = corresponding_addresses.loc[match_index, 'Address']
    else:
        # if no match found, check if there's any address from corresponding_addresses that is contained in street (the other way around)
        for addr in corresponding_addresses['formatted_address']:
            if addr.lower() in street:
                new_column_value = corresponding_addresses[corresponding_addresses['formatted_address'].str.lower() == addr.lower()]['Address'].values[0]
                break  # exit loop if a match is found

    # update new_column with the address if match found
    addresses_data.at[index, 'new_column'] = new_column_value
    
addresses_data.rename(columns={'new_column': 'Address'}, inplace=True) # rename the cols
addresses_data['Address'] = addresses_data['Address'].replace('No', 'no match') # renaming for rows with no match

# add results to data
data['Address official'] = addresses_data['Address']
data = data[data['Address official'] != 'No match'] # exclude rows without match

# import list with all buildings (streetname + number) in switzerland
file_path = 'pure_adr.csv'
all_addresses_CH = pandas.read_csv(file_path, delimiter=';')
all_addresses_CH = all_addresses_CH['STN_LABEL'] + ' ' + all_addresses_CH['ADR_NUMBER'] # extract only street + number
all_addresses_CH = pandas.DataFrame(all_addresses_CH) # convert to a dataframe
all_addresses_CH.columns = ['address']
all_addresses_CH = all_addresses_CH.dropna() # drop missing values in list wiht all addresses

data['street'] = data['street'].str.strip() # remove empty spaces
data['Street_in_all_addresses_CH'] = data['street'].isin(all_addresses_CH['address']) # bool checks wheter adress from our dataset is in list with all addresses

# if it is FALSE now, remove everything after first digit and add number "1"
data['street2'] = data.apply(lambda row: re.sub(r'\d.*', '1', row['street']) if row['Street_in_all_addresses_CH'] == False else row['street'], axis=1)
data['Street_in_all_addresses_CH'] = data['street2'].isin(all_addresses_CH['address'])
data = data[data['Street_in_all_addresses_CH'] == True] # drop rows where street is not in list of all addresses

data['street'] = data['street2']
data = data.drop(columns=['Address official', 'Street_in_all_addresses_CH', 'street2'])

# delete variables not needed anymore
del addr, addresses, addresses_data, bfs_nr, corresponding_addresses, index, row, match_index, new_column_value, street

"""
Object Type
"""
value_counts = data['object_type'].value_counts()

# Reassign types with less than 11 occurances
types_to_reassign = {
    'Rustico': 'Wohnung',
    'Mansarde': 'Wohnung',
    'Einliegerwohnung': 'Wohnung',
    'Stöckli': 'Wohnung',
    'Einzelzimmer': 'Wohnung',
    'Haus': 'Einfamilienhaus'  # Reassign 'Haus' to 'Einfamilienhaus'
}

data['object_type'] = data['object_type'].replace(types_to_reassign)

# check if still any values are missing
missing_values_per_column = data.isna().sum() # no missing values

# export data
data.to_csv('cleaned_data.csv', index=False)

del missing_values_per_column, value_counts

"""
Add Latittude / Longitutde to data
"""

import pandas as pd
import numpy as np

# read all addresses
file_path = 'adr_data_clean.csv'
addresses = pandas.read_csv(file_path, delimiter=';')

# split up feature variable (either separated by "," or "/")
split_features = data['features'].str.split('[,\/]', expand=True)

# trim white spaces
split_features = split_features.applymap(lambda x: str(x).strip())

# convert to strings
split_features = split_features.applymap(str)

# unique features
unique_features = pd.unique(split_features.values.ravel())

# remove "none"
unique_features = unique_features[unique_features != 'None']

# remove "nan"
unique_features = unique_features[unique_features != 'nan']

# empty df with dummy variables
dummy_df = pd.DataFrame(0, index=split_features.index, columns=unique_features)

# populate df
for feature in unique_features:
    # Apply str.contains safely across all elements now that they are strings
    mask = split_features.apply(lambda x: x.str.contains(feature, regex=False, na=False))
    dummy_df[feature] = mask.any(axis=1).astype(int)

# merge with original df
merged_df = pd.concat([data, dummy_df], axis=1)
merged_df.drop('features', axis=1, inplace=True) # drop features col

# full address in addresses df
addresses['full_address'] = addresses['STN_LABEL'].astype(str) + ' ' + \
                            addresses['ADR_NUMBER'].astype(str) + ' ' + \
                            addresses['zip'].astype(str)

# full address in data
merged_df["full_address"] =  merged_df['street'].astype(str) + ' ' + merged_df['PLZ_only'].astype(str)

# drop rows where address["full_address"] has a duplicate - otherwise merged_df will change it's size
# identify duplicates in the 'full_address' column
duplicates = addresses.duplicated(subset='full_address', keep=False)
# filter out all rows that have duplicates in the 'full_address' column
addresses_unique = addresses[~duplicates]

# merge merged_df with addresses on 'full_address', keeping all rows from merged_df
merged_df = pd.merge(merged_df, addresses_unique[['full_address', 'lat', 'long']], on='full_address', how='left')

# drop unnecessary columns
merged_df.drop(columns=["PLZ"], inplace=True)

# drop rows with NaN
merged_df.dropna(subset=['long'], inplace=True)

# last check for missing values:
missing_values_per_column = merged_df.isna().sum() # no missing values

# export data
merged_df.to_csv('dat_clean.csv', index=False)


