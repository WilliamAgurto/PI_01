from fastapi import FastAPI
import pandas as pd
from typing import Optional
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
app = FastAPI(title='API FILMS',description='Here, I will recomend you the bes movies', version='1.1')

#http://127.0.0.1:8000
'''''
Deben crear 6 funciones para los endpoints que se consumirán en la API, recuerden que deben tener un decorador por cada una (@app.get(‘/’)).
'''
@app.get("/")
async def welcome():
    return "WELCOME!!! HERE YOU WILL FIND THE BEST MOVIES EVER !!!"

@app.get("/index")
async def index():
    return "Function for searching: 1. peliculas_mes 2. peliculas_dia, 3. franquicia, 4. peliculas_pais, 5.productoras  y 6.retorno"

#loading Data
path = 'C:\\Users\\Hp\\Documents\\henry course\\Labs\\PI_01\\datasets\\new_movies_dataset.csv'
df_movies= pd.read_csv(path,parse_dates=['release_date'])
#df= pd.read_csv('C:\Users\Hp\Documents\henry course\Labs\PI_01\datasets\new_movies_dataset.csv',parse_dates=['release_date'])



'''''
1. def peliculas_mes(mes): 'Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes (nombre del mes, en str, ejemplo 'enero') 
historicamente' return {'mes':mes, 'cantidad':respuesta}
'''

@app.get('/movie_month/{month}')
def peliculas_mes(month:Optional[str]='January'):
    df_movies_copy = df_movies.copy()
    df_movies_copy['month'] = df_movies_copy.release_date.dt.month_name()
    df_movies_copy = df_movies_copy.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    result = df_movies_copy[df_movies_copy.month==month]['title'].count()
    return {'month':month,'quantity':int(result)}
    
'''''    
#2.def peliculas_dia(dia): 'Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrenaron ese dia (de la semana, en str, ejemplo 'lunes')
 historicamente' return {'dia':dia, 'cantidad':respuesta}
'''
@app.get("/movie_day/{day}")
def movie_day(day:Optional[str]=None):
    df_movies_copy = df_movies.copy()
    df_movies_copy['day'] = df_movies_copy.release_date.dt.day_name()
    df_movies_copy = df_movies_copy.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    result = df_movies_copy[df_movies_copy.day==day]['title'].count()
    return {'day':day,'quantity':int(result)}

'''
3. Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio
'''
@app.get("/franchise{franchise}")
def franchise(franchise: Optional[str] = None):
    df_movies_copy = df_movies.copy()
    result = df_movies_copy[df_movies_copy.belongs_to_collection == franchise]['title'].count()
    total_revenue = df_movies_copy[df_movies_copy.belongs_to_collection == franchise]['revenue'].sum()
    mean_revenue = df_movies_copy[df_movies_copy.belongs_to_collection == franchise]['revenue'].mean()
    return {'franchise':franchise, 'quantity':int(result), 'total revenue':float(total_revenue), 'mean revenue':float(mean_revenue)}

'''
4. @app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais:str):
    'Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo'
    return {'pais':pais, 'cantidad':respuesta}
'''
@app.get("/movies_country/{country}")
def movies_country(country:Optional[str]=None):
    df_movies_copy = df_movies.copy()
    country_ = df_movies_copy.production_countries
    country_ = country_.str.split(',')
    country_ = country_.explode()
    result = country_[country_ == country].count()
    return {'country':country, 'quantity':int(result)}

'''
5. @app.get('/productoras/{productora}')
def productoras(productora:str):
    'Ingresas la productora, retornando la ganancia total y la cantidad de peliculas que produjeron''
    return {'productora':productora, 'ganancia_total':respuesta, 'cantidad':respuesta
'''
@app.get("/production_companies/{production_companies}")
def production_companies(production_companies:Optional[str]=None):
    df_movies_copy = df_movies.copy()
    result=df_movies_copy[df_movies_copy.production_companies==production_companies].revenue.count()
    total_revenue=df_movies_copy[df_movies_copy.production_companies==production_companies].revenue.sum()
    return {'production companies':production_companies, 'total revenue':float(total_revenue), 'quantity':int(result)}
    
'''
6. @app.get('/retorno/{pelicula}')
def retorno(pelicula:str):
    ''Ingresas la pelicula, retornando la inversion, la ganancia, el retorno y el año en el que se lanzo''
    return {'pelicula':pelicula, 'inversion':respuesta, 'ganacia':respuesta,'retorno':respuesta, 'anio':respuesta}
'''
@app.get("/return/{movie}")
def return_(movie:Optional[str]=None):
    df_movies_copy = df_movies.copy()
    investment = df_movies_copy[df_movies_copy.title == movie].budget[0]
    revenue = df_movies_copy[df_movies_copy.title == movie].revenue[0]
    return_ = df_movies_copy[df_movies_copy.title == movie]['return'][0]
    year = df_movies_copy[df_movies_copy.title == movie].release_year[0]
    return {'movie':movie, 'investment':float(investment), 'revenue':float(revenue),'return':float(return_), 'year':int(year)}

##########recommendation function
@app.get('/get_recomendation/{title}')
def get_recomendation(title:Optional[str]=None):
    df_movies_copy = df_movies.copy()
    # Loading just two columns from CSV file on pandas.
    overview = df_movies_copy[['title','overview']]
   
    # Getting the description of the movie title given.
    overview = df_movies_copy[df_movies_copy['title'] == title]['overview'].str.strip()[0]

    # Computing  TF-IDF features for all oveviews.
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df_movies_copy['overview'])

    # Computing cosine similarities between overview and movie titles and all the other overviews.
    tfidf_similarities = cosine_similarity(tfidf_matrix, tfidf.transform([overview]))

    # getting top 10 indexes of films wich best matech according to TF-IDF.
    tfidf_similar_movie_indices = tfidf_similarities.argsort(axis=0)[-10:][::-1].flatten()

    # Turn indexes into movie titles  
    tfidf_similar_movie_titles = df_movies_copy.loc[tfidf_similar_movie_indices, 'title'].tolist()
    result = tfidf_similar_movie_titles[1:6]
    return {'recommendation': result}
  
    