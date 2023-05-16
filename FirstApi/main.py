from fastapi import FastAPI
import pandas as pd
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
df_movies= pd.read_csv(path,parse_dates=['release_date'],encoding ='utf-8')
#df= pd.read_csv('C:\Users\Hp\Documents\henry course\Labs\PI_01\datasets\new_movies_dataset.csv',parse_dates=['release_date'])



'''''
1. 'Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes (nombre del mes, en str, ejemplo 'enero') 
historicamente'
'''

@app.get('/peliculas_mes/{mes}')
def peliculas_mes(mes:str):
    df_movies_copy = df_movies.copy()
    df_movies_copy['month'] = df_movies_copy.release_date.dt.month_name()
    # Dicctionary traduction
    translation_dict = {'January': 'enero', 'February': 'febrero', 'March': 'marzo', 'April': 'abril', 'May': 'mayo',
                        'June':'junio','July':'julio','August': 'agosto','September': 'septiembre','October': 'octubre',
                        'November': 'noviembre','December': 'diciembre'}
    # Applying traduction
    df_movies_copy['month'] = df_movies_copy['month'].replace(translation_dict)
    df_movies_copy = df_movies_copy.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    result = df_movies_copy[df_movies_copy.month==mes]['title'].count()
    return {'month':mes,'quantity':int(result)}
    
'''''    
#2. 'Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrenaron ese dia (de la semana, en str, ejemplo 'lunes')
 historicamente' 
'''
@app.get("/peliculas_dia/{dia}")
def peliculas_dia(dia:str):
    df_movies_copy = df_movies.copy()
    df_movies_copy['day'] = df_movies_copy.release_date.dt.day_name()
    # Dicctionary traduction
    translation_dict = {'Monday': 'lunes',
                        'Tuesday': 'martes',
                        'Wednesday': 'miercoles',
                        'Thursday': 'jueves',
                        'Friday': 'viernes',
                        'Saturday': 'sabado',
                        'Sunday': 'domingo'}
    # Applying traduction
    df_movies_copy['day'] = df_movies_copy['day'].replace(translation_dict)
    df_movies_copy = df_movies_copy.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    result = df_movies_copy[df_movies_copy.day==dia]['title'].count()
    return {'day':dia,'quantity':int(result)}

'''
3. Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio
'''
@app.get("/franquicia{franquicia}")
def franquicia(franquicia:str):
    df_movies_copy = df_movies.copy()
    result = df_movies_copy[df_movies_copy.belongs_to_collection == franquicia]['title'].count()
    total_revenue = df_movies_copy[df_movies_copy.belongs_to_collection == franquicia]['revenue'].sum()
    mean_revenue = df_movies_copy[df_movies_copy.belongs_to_collection == franquicia]['revenue'].mean()
    return {'franchise':franquicia, 'quantity':int(result), 'total revenue':float(total_revenue), 'mean revenue':float(mean_revenue)}

'''
4. 'Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo'
'''
@app.get("/peliculas_pais/{pais}")
def peliculas_pais(pais:str):
    df_movies_copy = df_movies.copy()
    country_ = df_movies_copy.production_countries
    country_ = country_.str.split(',')
    country_ = country_.explode()
    result = country_[country_ == pais].count()
    return {'country':pais, 'quantity':int(result)}

'''
5. Ingresas la productora, retornando la ganancia total y la cantidad de peliculas que produjeron''
'''
@app.get("/productoras/{productora}")
def productoras(productora:str):
    df_movies_copy = df_movies.copy()
    result=df_movies_copy[df_movies_copy.production_companies==productora].revenue.count()
    total_revenue=df_movies_copy[df_movies_copy.production_companies==productora].revenue.sum()
    return {'production companies':productora, 'total revenue':float(total_revenue), 'quantity':int(result)}
    
'''
6.Ingresas la pelicula, retornando la inversion, la ganancia, el retorno y el año en el que se lanzo''
'''
@app.get("/retorno/{pelicula}")
def retorno(pelicula:str):
    df_movies_copy = df_movies.copy()
    investment = df_movies_copy[df_movies_copy.title == pelicula].budget[0]
    revenue = df_movies_copy[df_movies_copy.title == pelicula].revenue[0]
    return_ = df_movies_copy[df_movies_copy.title == pelicula]['return'][0]
    year = df_movies_copy[df_movies_copy.title == pelicula].release_year[0]
    return {'movie':pelicula, 'investment':float(investment), 'revenue':float(revenue),'return':float(return_), 'year':int(year)}

##########recommendation function
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    df_movies_copy = df_movies.copy()
    # Loading just two columns from CSV file on pandas.
    overview = df_movies_copy[['title','overview']]
   
    # Getting the description of the movie title given.
    overview = df_movies_copy[df_movies_copy['title'] == titulo]['overview'].str.strip()[0]

    # Computing  TF-IDF features for all oveviews.
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df_movies_copy['overview'])

    # Computing cosine similarities between overview and movie titles and all the other overviews.
    tfidf_similarities = cosine_similarity(tfidf_matrix, tfidf.transform([overview]))

    # getting top 10 indexes of films wich best matech according to TF-IDF.
    tfidf_similar_movie_indices = tfidf_similarities.argsort(axis=0)[-10:][::-1].flatten()

    # Turn indexes into movie titles  
    tfidf_similar_movie_titles = df_movies_copy.loc[tfidf_similar_movie_indices, 'title'].tolist()
    respuesta = tfidf_similar_movie_titles[1:6]
    return {'recommendation': respuesta}
  
    