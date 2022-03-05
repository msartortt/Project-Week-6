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

# Now we need to creat a different table, containg every genre in a different column
genres_melt = movies_data[['imdbID','genres']]
genres_melt["genres"] = genres_melt.genres.str.replace("'", "", regex=True).str.replace("]", "", regex=True).str.replace("[", "", regex=True)
genres_melt = pd.concat([genres_melt[['imdbID']], genres_melt['genres'].str.split(', ', expand=True)], axis=1)

stacked = genres_melt.set_index('imdbID').stack() # keep topic as index, stack other columns 'against' it
movies_genres = stacked.reset_index(name='genres') # set the name of the new series created
movies_genres.drop('level_1', axis=1, inplace=True) # drop the 'source' level (key.*)

movies_genres.dropna(subset = ['genres'], inplace = True) # drop any nulls
movies_genres.to_csv('movies_genres_2021.csv', index=False) # export to csv

#Repeate the same process for Countries:

countries_melt = movies_data[['imdbID','country']]
countries_melt["country"] = countries_melt.country.str.replace("'", "", regex=True).str.replace("]", "", regex=True).str.replace("[", "", regex=True)
countries_melt = pd.concat([countries_melt[['imdbID']], countries_melt['country'].str.split(', ', expand=True)], axis=1)

stacked = countries_melt.set_index('imdbID').stack()
movies_countries = stacked.reset_index(name='country')
movies_countries.drop('level_1', axis=1, inplace=True)

movies_countries.dropna(subset = ['country'], inplace = True)
movies_countries.to_csv('movies_countries_2021.csv', index=False)

#Repeate the same process for Languages:

languages_melt = movies_data[['imdbID','languages']]
languages_melt["languages"] = languages_melt.languages.str.replace("'", "", regex=True).str.replace("]", "", regex=True).str.replace("[", "", regex=True)
languages_melt = pd.concat([languages_melt[['imdbID']], languages_melt['languages'].str.split(', ', expand=True)], axis=1)

stacked = languages_melt.set_index('imdbID').stack() 
movies_languages = stacked.reset_index(name='languages')
movies_languages.drop('level_1', axis=1, inplace=True) 
movies_languages.dropna(subset = ['languages'], inplace = True)
movies_languages.to_csv('movies_languages_2021.csv', index=False)