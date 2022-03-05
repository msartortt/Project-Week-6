# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 10:12:57 2022

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
▒▒▒▒▒▒▒▒▒▒   TAKE FROM IMDB THE LIST OF MOVIES FROM A TIMEFRAME  ▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
'''

# This loop will webscrap de IMDB page with the list of all films from this timeframe, taking the link for each movie

url = 'https://www.imdb.com/search/title/?title_type=feature,tv_movie&release_date=2021-01-01,2021-12-31'
amount_movies = 14482 # inserting manualy the total amount of movies from the desired timeframe
url_list = []

try:
    for i in range (0,(round(amount_movies/50))):
        if i <= (round(amount_movies/50)):
            response = requests.get(url)
            soup = BeautifulSoup(response.content, features = 'lxml')

            list_detail = soup.find_all('div', attrs = {'class':'lister-item-content'})
            url_list_now = ["https://www.imdb.com" + link.a['href'] for link in list_detail]
            url_list.append(url_list_now)
            
            try:
                linkNext1 = soup.find_all('a', attrs = {'class':'lister-page-next next-page'})[0]
                linknext = linkNext1['href']
                url = f'https://www.imdb.com{linknext}'
            except:
                url = url

        else:   
            flat_list = [item for lista in url_list for item in lista]
except:
    print(f'issue with this link: {url}')
    
# Drop duplicates and sotre it in a csv file so we don't need to run it again

flat_list_df = pd.DataFrame(flat_list)
flat_list_df = flat_list.drop_duplicates()
flat_list_df.to_csv('list_imdb_links_2021.csv', index=False)