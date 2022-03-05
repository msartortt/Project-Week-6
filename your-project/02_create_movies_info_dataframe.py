# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 20:14:22 2022

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
import regex as re
    
'''
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒▒   TAKE FROM IMDB ALL THE IMPORTATN INFO ABOUT EACH MOVIE  ▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
'''

# This loop will webscrap de IMDB page for each filme on our list and and take the data we want to evaluate

flat_list = pd.read_csv('lista_imdb_links_2021.csv')
flat_list = list(flat_list['0'])

data = []
link_error = []

for link in flat_list:
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, features = 'lxml')
        
        # 1. get the data from the movie IMDB page
        imdbID = link.replace('https://www.imdb.com/title/tt','').replace('/','')
        # 2. movie name
        movie_name = soup.title.text
        movie_name = movie_name.replace(' - IMDb','')
        # 3. launching year
        try:
            year = soup.find_all('ul', attrs = {'data-testid':"hero-title-block__metadata"})[0].text
            year = re.findall(r'[0-9]{4}', year)
            year = year[0]
        except:
            year = ''
        # 4. IMDB rating
        try:
            imdb_rating = soup.find_all('span', attrs = {'class':"AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV"})[0].text
        except:
            imdb_rating = ''
        # 5. quantidade de votos
        try:
            user_votes = soup.find_all('div', attrs = {'class':"AggregateRatingButton__TotalRatingAmount-sc-1ll29m0-3 jkCVKJ"})[0].text
        except:
            user_votes = ''
        # 6. director
        try:
            director = soup.find_all('a', attrs = {'class':"ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})[0].text
        except:
            director = ''
        # awards
        try:
            awards = soup.find_all('li', attrs = {'data-testid':"award_information"})[0].text
        except:
            awards = ''
        # 7. oscars
        try:
            oscars = re.findall(r'(\d+)(?=\s*Oscar)', awards)[0]
        except:
            oscars = 0
        # 8. awards won
        try:
            awards_won = re.findall(r'(\d+)(?=\s*win)', awards)[0]
        except:
            awards_won = 0
        # 9. nominations
        try:
            awards_nominated = re.findall(r'(\d+)(?=\s*nomination)', awards)[0]
        except:
            awards_nominated = 0
        # 10. genre
        try:
            genres_html = soup.find_all('div', attrs = {'data-testid':"genres"})[0]
            genre = genres_html.find_all('a', attrs = {'class':'GenresAndPlot__GenreChip-sc-cum89p-3 LKJMs ipc-chip ipc-chip--on-baseAlt'})
            genres = [x.text for x in genre]
        except:
            genres = ''
        # 11. countries
        try:
            country_htlm = soup.find_all('li', attrs = {'data-testid':"title-details-origin"})[0]
            countries = country_htlm.find_all('a', attrs = {'class':'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'})
            country = [x.text for x in countries]
        except:
            country = ''
        # 12. languages
        try:
            languages_htlm = soup.find_all('li', attrs = {'data-testid':"title-details-languages"})[0]
            language = languages_htlm.find_all('a', attrs = {'class':'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'})
            languages = [x.text for x in language]
        except:
            languages = ''
        # 13. boxoffice budget
        try:
            boxoffice_budget = soup.find_all('li', attrs = {'data-testid':"title-boxoffice-budget"})[0].text
            boxoffice_budget = boxoffice_budget.replace('Budget','').replace(' (estimated)','')
            boxoffice_budget = re.findall(r'[0-9]*', boxoffice_budget)
            boxoffice_budget = ''.join(str(x) for x in boxoffice_budget)
        except:
            boxoffice_budget = ''
        # 14. gross worldwide
        try:
            gross_worldwide = soup.find_all('li', attrs = {'data-testid':"title-boxoffice-cumulativeworldwidegross"})[0].text
            gross_worldwide = gross_worldwide.replace('Gross worldwide','').replace(' (estimated)','')
            gross_worldwide = re.findall(r'[0-9]*', gross_worldwide)
            gross_worldwide = ''.join(str(x) for x in gross_worldwide)
        except:
            gross_worldwide = ''
        
        # Create a dictionary
        data.append({'imdbID': imdbID,
                     'movie_name':movie_name,
                     'year':year,
                     'imdb_rating':imdb_rating,
                     'user_votes':user_votes,
                     'director':director,
                     'oscars':oscars,
                     'awards_won':awards_won,
                     'awards_nominated':awards_nominated,
                     'genres':genres,
                     'country':country,
                     'languages':languages,
                     'boxoffice_budget':boxoffice_budget,
                     'gross_worldwide':gross_worldwide})
        print(link)    
    except:
        link_error.append(link)

# Drop duplicates and sotre it in a csv file so we don't need to run it again
movies_data = pd.DataFrame(data)
movies_data.drop_duplicates(subset=['imdbID'], keep='last')
movies_data.to_csv('movies_data_2021.csv', index=False)