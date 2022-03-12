<img src="https://bit.ly/2VnXWr2" alt="Ironhack Logo" width="100"/>

# Title of My Project
Matheus Sartortt

- [Cohort](https://my.ironhack.com/cohorts/5f60a919b77d4c478c04cf99/profile) 
- Campus: Ironhack Lisbon
- Date: March 12th 2022

## Content
- [Project Description](#project-description)
- [Hypotheses / Questions](#hypotheses-/-questions)
- [Dataset](#dataset)
- [Workflow](#workflow)
- [Organization](#organization)

<a name="project-description"></a>

## Project Description
The main challenge of this project was to create a webscraping code to collect data from movies through [IMDB](https://www.imdb.com/)  website and, later, work on the data (cleaning and formatting) in addition to evaluating metrics by hypothesis testing. 

<a name="hypotheses-/-questions"></a>

## Hypotheses / Questions
1. Evaluating the country where the movie was shot:
- Does a movie shot in the USA have better ROI?
- Does a movie shot in the USA have better ratings?
- Does a movie shot in the USA have more award nominations?

2. Evaluating the language spoken on the movie:
- Does a movie shot in English have better ROI?
- Does a movie shot in the English have better ratings?
- Does a movie shot in the English have more award nominations?

<a name="dataset"></a>

## Dataset
The dataset was obtained from the IMDB website. The main focus was to evaluate every movie launched in 2021, registered in IMDB.

[IMDB](https://www.imdb.com/search/title/?title_type=feature,tv_movie&release_date=2021-01-01,2021-12-31)

<a name="workflow"></a>

## Workflow
The project is divided into 4 parts, each with its own .py file for better organization. The flow was as follows:

1. [Create list timeframe:](https://github.com/msartortt/Project-Week-6/blob/master/your-project/01_create_list_timeframe.py) here we select the time cut to be evaluated and get all the movies registered on IMDB in this period;
2. [Create movies info dataframe:](https://github.com/msartortt/Project-Week-6/blob/master/your-project/02_create_movies_info_dataframe.py) here a webscraping is run to collect all the information to be evaluated about each movie (each line represents a movie);
3. [Create movies ratings dataframe:](https://github.com/msartortt/Project-Week-6/blob/master/your-project/03_create_movies_ratings_dataframe.py) here a second webscraping is run to collect all ratings for each movie, divided into voter genre and age group;
4. [Run movies statistical analysis:](https://github.com/msartortt/Project-Week-6/blob/master/your-project/04_run_movies_statistical_analysis.py) this code cleans, format and evaluates the main data, including hypothesis tests.

<a name="organization"></a>

## Organization
For this project, Anaconda Spyder was used as code editor. For the data visualization part, [Tableau](https://public.tableau.com/app/profile/matheus8205/viz/project_imbd/Dashboard?publish=yes)  was used.

