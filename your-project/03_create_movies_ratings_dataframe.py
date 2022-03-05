# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 20:15:07 2022

@author: msart
"""


'''
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   IMPORTING LIBRARIES  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
'''
import pandas as pd
from bs4 import BeautifulSoup
import requests
    
'''
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒▒▒▒▒▒   TAKE FROM IMDB THE RATINGS FROM ALL MOVIES  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
'''

# This loop will take all the ratings for every movie in our list of movies

flat_list = pd.read_csv('lista_imdb_links_2021.csv')
flat_list = list(flat_list['0'])

link_erro = []
imdb_ratings = []

for link in flat_list:
    
    try:
        rating_link = f'{link}ratings/'
        response = requests.get(rating_link)
        soup = BeautifulSoup(response.content, features = 'lxml')

        # Extracting Movie Id
        imdbID = link.replace('https://www.imdb.com/title/tt','').replace('/','')

        # Extracting table
        tables = soup.find_all('table')[1]

        # Extracting columns' names
        colname = tables.find_all('div', attrs = {'class':'tableHeadings'})
        colnames = [col.text.split("\n") for col in colname]
        flat_colnames = [item for sublist in colnames for item in sublist]

        # Extracting all rows
        row = tables.find_all('div', attrs = {'class':'bigcell'})
        rows = [r.text.split("\n") for r in row]
        flat_rows = [item for sublist in rows for item in sublist]

        splited = []
        len_l = len(flat_rows)
        for i in range(3):
            start = int(i*len_l/3)
            end = int((i+1)*len_l/3)
            splited.append(flat_rows[start:end])

        # Extracting columns gender
        col_gender = tables.find_all('div', attrs = {'class':'leftAligned'})
        col_gender = [i.text for i in col_gender]

        df = pd.DataFrame(splited, columns = flat_colnames)
        df.insert(0, 'imdbID', imdbID)
        df.insert(1, 'Gender', col_gender)

        try:
            imdb_ratings = pd.concat([imdb_ratings,df])
        except:
            imdb_ratings = df

    except:
        link_erro.append(rating_link)

# save to a file as the code was too heavy and I don't want to have to run it every time

movies_ratings_imdb = imdb_ratings.drop_duplicates(subset=['Movie Id'], keep='last')
movies_ratings_imdb.to_csv('movies_ratings_imdb_2021.csv', index=False)

len(movies_ratings_imdb) # Total amount of movies with ratings
len(link_erro) # Total amount of movies without ratings