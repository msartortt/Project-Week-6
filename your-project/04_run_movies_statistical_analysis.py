# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 20:15:37 2022

@author: msart
"""


'''
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   IMPORTING LIBRARIES  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
'''
import pandas as pd
import numpy as np
from scipy import stats
    
'''
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒▒▒▒   FIRST WE NEED TO DO SOME DATA CLEANING AND FORMATIGN  ▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
'''

# Importing al the need tables created from our webscraping

movies_data = pd.read_csv('C:\\Users\msart\Desktop\IronHack\Module_2\Project-Week-6\your-project\movies_data_2021.csv')
movies_ratings_imdb = pd.read_csv('C:\\Users\msart\Desktop\IronHack\Module_2\Project-Week-6\your-project\movies_ratings_imdb_2021.csv')

## TYPE FORMATING

# Defining strings
movies_data['imdbID'] = movies_data['imdbID'].astype('str')
movies_data['movie_name'] = movies_data['movie_name'].astype('str')
movies_data['director'] = movies_data['director'].astype('str')

# Defining numerics
movies_data['year'] = pd.to_numeric(movies_data['year'], downcast="integer")
movies_data['imdb_rating'] = pd.to_numeric(movies_data['imdb_rating'])
movies_data['oscars'] = pd.to_numeric(movies_data['oscars'])
movies_data['awards_won'] = pd.to_numeric(movies_data['awards_won'])
movies_data['awards_nominated'] = pd.to_numeric(movies_data['awards_nominated'])
movies_data['boxoffice_budget'] = pd.to_numeric(movies_data['boxoffice_budget'])
movies_data['gross_worldwide'] = pd.to_numeric(movies_data['gross_worldwide'])

movies_data.dtypes

# Defining strings
movies_ratings_imdb['imdbID'] = movies_ratings_imdb['imdbID'].astype('str')
movies_ratings_imdb['Gender'] = movies_ratings_imdb['Gender'].astype('str')

# Defining numerics
movies_ratings_imdb['All Ages'].replace('-', '', inplace=True)
movies_ratings_imdb['All Ages'] = pd.to_numeric(movies_ratings_imdb['All Ages'])
movies_ratings_imdb['<18'].replace('-', '', inplace=True)
movies_ratings_imdb['<18'] = pd.to_numeric(movies_ratings_imdb['<18'])
movies_ratings_imdb['18-29'].replace('-', '', inplace=True)
movies_ratings_imdb['18-29'] = pd.to_numeric(movies_ratings_imdb['18-29'])
movies_ratings_imdb['30-44'].replace('-', '', inplace=True)
movies_ratings_imdb['30-44'] = pd.to_numeric(movies_ratings_imdb['30-44'])
movies_ratings_imdb['45+'].replace('-', '', inplace=True)
movies_ratings_imdb['45+'] = pd.to_numeric(movies_ratings_imdb['All Ages'])

movies_ratings_imdb.dtypes

# Do some data cleaning
movies_data.isna().sum() # total amount of nulls by column
movies_data.isna().sum()/(len(movies_data))*100 # percentage of nulls by column

# We need to creat two new flag-columns as we will evaluate if a movie being filmed in USA/english impacts in the movies success (we are using the free version of Tableau, so we have a limit of how many dataframes we can import)
movies_data['English'] = np.where(movies_data['languages'].str.contains('English'), True, False)
movies_data['United States'] = np.where(movies_data['country'].str.contains('United States'), True, False)

movies_data['year'].fillna(value=2021, inplace=True) # cleaning years

movies_ratings_imdb.isna().sum() 
movies_ratings_imdb.isna().sum()/(len(movies_ratings_imdb))*100
movies_ratings_imdb.dropna(subset=['All Ages'], inplace=True)

# Now we need to creat a different table, containg every genre in a different column
genres_melt = movies_data[['imdbID','genres']]
genres_melt["genres"] = genres_melt.genres.str.replace("'", "", regex=True).str.replace("]", "", regex=True).str.replace("[", "", regex=True)
genres_melt = pd.concat([genres_melt[['imdbID']], genres_melt['genres'].str.split(', ', expand=True)], axis=1)

stacked = genres_melt.set_index('imdbID').stack() # keep topic as index, stack other columns 'against' it
movies_genres = stacked.reset_index(name='genres') # set the name of the new series created
movies_genres.drop('level_1', axis=1, inplace=True) # drop the 'source' level (key.*)

movies_genres.dropna(subset = ['genres'], inplace = True) # drop any nulls
movies_genres.to_csv('movies_genres_2021.csv', index=False) # export to csv
movies_genres.to_excel('movies_genres_2021.xlsx', sheet_name='genres', index=False) # export to xlsx

#Repeate the same process for Countries:

countries_melt = movies_data[['imdbID','country']]
countries_melt["country"] = countries_melt.country.str.replace("'", "", regex=True).str.replace("]", "", regex=True).str.replace("[", "", regex=True)
countries_melt = pd.concat([countries_melt[['imdbID']], countries_melt['country'].str.split(', ', expand=True)], axis=1)

stacked = countries_melt.set_index('imdbID').stack()
movies_countries = stacked.reset_index(name='country')
movies_countries.drop('level_1', axis=1, inplace=True)

movies_countries.dropna(subset = ['country'], inplace = True)
movies_countries.to_csv('movies_countries_2021.csv', index=False)
movies_countries.to_excel('movies_countries_2021.xlsx', sheet_name='countries', index=False)

#Repeate the same process for Languages:

languages_melt = movies_data[['imdbID','languages']]
languages_melt["languages"] = languages_melt.languages.str.replace("'", "", regex=True).str.replace("]", "", regex=True).str.replace("[", "", regex=True)
languages_melt = pd.concat([languages_melt[['imdbID']], languages_melt['languages'].str.split(', ', expand=True)], axis=1)

stacked = languages_melt.set_index('imdbID').stack() 
movies_languages = stacked.reset_index(name='languages')
movies_languages.drop('level_1', axis=1, inplace=True) 
movies_languages.dropna(subset = ['languages'], inplace = True)

movies_languages.to_csv('movies_languages_2021.csv', index=False)
movies_languages.to_excel('movies_languages_2021.xlsx', sheet_name='languages', index=False)


'''
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   HIPOTESIS TESTING  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
'''

# As we don't have the full universe information even for 2021 entirely, we will work with a sample.
# This sample was selected based on the non-probabilistic convenience sampling method, with 175 occurrences.
# This method provides us with convenience, ease and speed, despite not having a high rate of representativeness.
movies_data_not_null = movies_data[movies_data.isnull().sum(axis=1) == 0]

# In order to compare the profits between movies, we will calculate the ROI (return over investment)
# This metric is a percentage of how much a movie made in comparisson from the total budget
movies_data_not_null['ROI'] = (movies_data_not_null['gross_worldwide'] - movies_data_not_null['boxoffice_budget'])/ movies_data_not_null['boxoffice_budget']

'''
▒▒▒▒▒▒▒▒▒ Does a movie shot in the USA have better ROI? ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

H0: µ USA ROI < µ Other countires ROI
H1: µ USA ROI ≥ µ Other countires ROI
'''
usa_ROI = movies_data_not_null['ROI'][movies_data_not_null['United States'] == True]
other_ROI_0 = movies_data_not_null[movies_data_not_null['ROI'] < 100] # looking at our data we saw that 5 movies have an outlier value and we are not secure about this data source
other_ROI = other_ROI_0['ROI'][other_ROI_0['United States'] == False]

t_test = stats.ttest_ind(usa_ROI, other_ROI, alternative='greater')

alpha = 1-0.95
p_value = t_test[1]

p_value <= alpha # We reject the H0. Movies shot in USA tend to have a better ROI

usa_ROI.mean() # ~(0.49)
other_ROI.mean() # ~(-0.3)

'''
▒▒▒▒▒▒▒▒▒ Does a movie shot in the USA have better ratings? ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

H0: µ USA ratings < µ Other countires ratings
H1: µ USA ratings ≥ µ Other countires ratings
'''
usa_ratings = movies_data_not_null['imdb_rating'][movies_data_not_null['United States'] == True]
other_ratings = movies_data_not_null['imdb_rating'][movies_data_not_null['United States'] == False]

t_test = stats.ttest_ind(usa_ratings, other_ratings, alternative='greater')

alpha = 1-0.95
p_value = t_test[1]

p_value <= alpha # We are not able to reject the H0. Movies shot outside USA tend to have a greater ratings

usa_ratings.mean() # ~(6.01)
other_ratings.mean() # ~(6.49)

'''
▒▒▒▒▒▒▒▒▒ Does a movie shot in the USA have more award nominations? ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

H0: µ USA nominations < µ Other countires nominations
H1: µ USA nominations ≥ µ Other countires nominations
'''
usa_nominations = movies_data_not_null['awards_nominated'][movies_data_not_null['United States'] == True]
other_nominations = movies_data_not_null['awards_nominated'][movies_data_not_null['United States'] == False]

t_test = stats.ttest_ind(usa_nominations, other_nominations, alternative='greater')

alpha = 1-0.95
p_value = t_test[1]

p_value <= alpha # We reject the H0. Movies shot in USA tend to have more award nominations

usa_nominations.mean() # ~(22.74)
other_nominations.mean() # ~(4.30)

'''
▒▒▒▒▒▒▒▒▒ Does a movie shot in English have better ROI? ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

H0: µ English ROI < µ non-English ROI
H1: µ English ROI ≥ µ non-English ROI
'''
english_ROI = movies_data_not_null['ROI'][movies_data_not_null['English'] == True]
non_english_ROI_0 = movies_data_not_null[movies_data_not_null['ROI'] < 100] # looking at our data we saw that 5 movies have an outlier value and we are not secure about this data source
non_english_ROI = non_english_ROI_0['ROI'][non_english_ROI_0['English'] == False]

t_test = stats.ttest_ind(english_ROI, non_english_ROI, alternative='greater')

alpha = 1-0.95
p_value = t_test[1]

p_value <= alpha # We reject the H0. Movies shot in English language tend to have a better ROI

english_ROI.mean() # ~(0.31)
non_english_ROI.mean() # ~(-0.32)

'''
▒▒▒▒▒▒▒▒▒ Does a movie shot in the English have better ratings? ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

H0: µ English ratings < µ non-English ratings
H1: µ English ratings ≥ µ non-English ratings
'''
english_ratings = movies_data_not_null['imdb_rating'][movies_data_not_null['English'] == True]
non_english_ratings = movies_data_not_null['imdb_rating'][movies_data_not_null['English'] == False]

t_test = stats.ttest_ind(english_ratings, non_english_ratings, alternative='greater')

alpha = 1-0.95
p_value = t_test[1]

p_value <= alpha # We are not able to reject the H0. Movies shot in other languages tend to have a greater ratings

english_ratings.mean() # ~(5.99)
non_english_ratings.mean() # ~(6.59)

'''
▒▒▒▒▒▒▒▒▒ Does a movie shot in the English have more award nominations? ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

H0: µ English nominations < µ non-English nominations
H1: µ English nominations ≥ µ non-English nominations
'''
english_nominations = movies_data_not_null['awards_nominated'][movies_data_not_null['English'] == True]
non_english_nominations = movies_data_not_null['awards_nominated'][movies_data_not_null['English'] == False]

t_test = stats.ttest_ind(english_nominations, non_english_nominations, alternative='greater')

alpha = 1-0.95
p_value = t_test[1]

p_value <= alpha # We reject the H0. Movies shot in English tend to have more award nominations

english_nominations.mean() # ~(19.35)
non_english_nominations.mean() # ~(4.01)
