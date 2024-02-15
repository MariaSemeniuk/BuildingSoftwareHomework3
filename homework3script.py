import pandas as pd #import neccesary packages
import numpy as np
import matplotlib.pyplot as plt

import argparse
import yaml

import logging

from load_file import load_file

parser = argparse.ArgumentParser(description='Dataset analysis script')
parser.add_argument('output', type=str, help='Output filename')
parser.add_argument('config', type=str, help='Path to the configuration file')
parser.add_argument('--verbose', '-v', action='store_true', help='Print verbose logs')
args = parser.parse_args()

if args.verbose:
    logging_level = logging.INFO
else:
    logging_level = logging.WARNING

# Initialize logging module
logging.basicConfig(
    level=logging_level, 
    handlers=[logging.StreamHandler(), logging.FileHandler('my_python_analysis.log')],
)

# read arguments
print(args.config)

config_paths = ['user_config.yml']
config_paths.append(args.config)

print(config_paths)

config = {}
for path in config_paths:
    logging.info(f'Loading {path}')
    with open(path, 'r') as f:
        this_config = yaml.safe_load(f)
        config.update(this_config)

print(config)

green_vehicle = load_file(config['input']) 

#2 Profile the DataFrame
green_vehicle.head()
print(list(green_vehicle)) #column names
green_vehicle.dtypes #dtypes when loaded. All make sense.
green_vehicle.info() #0 NaNs in each colomn
green_vehicle.shape #shape of DataFrame

#3 Generate some summary statistics for the data
green_vehicle.describe(include='all') #see DataFrame for max, min, mean, mean for numeric columns and the most common and unique values for text columns.
#all statistics seem expected. 

#4 Rename one or more columns in the DataFrame
green_vehicle = green_vehicle.rename(columns=str.lower) #rename all columns to be lower case
green_vehicle = green_vehicle.rename(columns={'unit no':'unit_no', 'category description':'category_description', #renaming individual columns
                                               'in service date':'in_service_date','green vehicle type':'green_vehicle_type', 
                                               'division / agency': 'division_agency'})
green_vehicle.head()

#5 Select a single column and find its unique values
green_vehicle['green_vehicle_type'].unique()

#6 Select a single text/categorical column and find the counts of its values. 
if 'make' not in green_vehicle.columns:
    raise KeyError(f"column 'make' not found in Dataframe")
green_vehicle['make'].value_counts()

#7 Convert the data type of at least one of the columns. If all columns are typed correctly, convert one to str and back
green_vehicle['year'] = green_vehicle['year'].astype('str') # convert year column to str 
green_vehicle['year'].head() # double check it is a string, line not needed
green_vehicle['year'] = green_vehicle['year'].astype('int') #convert year column to int
green_vehicle['year'].head() # double check it is an int, line not needed

#8 Write the DataFrame to a different file  format than the original.
green_vehicle.to_csv('../green_vehicle.csv')

# More Data Wrangling, filtering
#1 create a column dervied form an existing one.
#extract date or time part
green_vehicle['in_service_year'] = green_vehicle['in_service_date'].dt.strftime('%Y') #make a column from in_service_date being separated to in_service_year 
green_vehicle['in_service_month'] = green_vehicle['in_service_date'].dt.strftime('%m') #and in_servie_month
green_vehicle.head() #check if correct

#2 Remove one or more columns from the dataset.
green_vehicle = green_vehicle.drop(columns='unit_no') #remove unit_no from dataset
green_vehicle.head() #check if correct

#3 Extract a subset of columns and rows to a new DataFrame
#with the .query(0method and column selecting [[colnames]])
green_vehicle.query('green_vehicle_type == "NATURAL GAS"') #query method to extract NATURAL GAS green vehicles types to a DataFrame
year_make_model = green_vehicle[["year", "make", "model"]] #extract the year, make and model
year_make_model #print the year, make and model DataFrame
#with .loc[]
filter_list = ['NATURAL GAS', 'PROPANE GAS'] #create a list
green_vehicle.loc[green_vehicle['green_vehicle_type'].isin(filter_list), 'green_vehicle_type'] #extract the filter_list from green_vehicle_type to DataFrame

#4. Investigate null values
#Create and describe a DataFrame contaiing records with NaNs in any column

df1 = pd.DataFrame() #new DataFrame
df1['Col1'] = [np.nan,np.nan,np.nan,np.nan,np.nan] #use np.nan to create NaN values in a column
df1['Col2'] = [np.nan,np.nan,np.nan,np.nan,np.nan]
df1['Col3'] = [np.nan,np.nan,np.nan,np.nan,np.nan]
df1['Col4'] = [np.nan,np.nan,np.nan,np.nan,np.nan] #DataFrame has 4 coloumn 

df1

df1.describe(include='all') #describe the df1 DataFrame

#Create and describe a DataFrame containing records with NaNs in a subset of columns
df2 = pd.DataFrame() #new DataFrame
df2['Col1'] = ['0',np.nan,'1',np.nan,'4'] #use np.nan to create NaN values in a column
df2['Col2'] = [np.nan,'1',np.nan,'5','1']
df2['Col3'] = [np.nan,'6',np.nan,np.nan,'1']
df2['Col4'] = [np.nan,np.nan,np.nan,np.nan,np.nan] #DataFrame has 4 coloumn 
df2

df2.describe(include='all') #describe the df2 DataFrame

#If it makes sense to drop records with NaNs in certain columns from the original DataFrame, do so.
df2 = df2.drop(columns='Col4') #drop a column from df2
df2

#Grouping and aggregating
#1. Use `groupby()` to split your data into groups based on one of the columns.
make_groups = green_vehicle.groupby('make')
make_groups['year'].mean() #check if correct

#2. Use `agg()` to apply multiple functions on different columns and create a summary table. 
#Calculating group sums or standardizing data are two examples of possible functions that you can use.
green_vehicle_summary = make_groups.agg(year_mean=('year','mean'), #aggregrate data based on make_groups
                                year_min=('year', 'min'),
                                year_max=('year', 'max'), 
                                )

green_vehicle_summary.head()

### Plot
#1. Plot two or more columns in your data using `matplotlib`, `seaborn`, or `plotly`. 
#Make sure that your plot has labels, a title, a grid, and a legend.

counts = make_groups.agg(make_count=('make', 'count')) #create a dataframe with count of each make of vehicle
ax = counts.plot.bar()  #create a bar plot from counts DataFrame

plt.title('Number of Green Vehicles Owned by the City of Toronto')  #plot title
plt.xlabel('Make') #plot x-axis label
plt.ylabel('Count') #plot y-axis label
ax.grid(alpha=config['alpha']) #insert grid lines
plt.show()
plt.savefig(args.output)
