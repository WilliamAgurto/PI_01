<div align="center">

![](https://camo.githubusercontent.com/35b81f213ddb0e019b3567f6982d740bb2d01ae5dd712a1537e09e826e940228/68747470733a2f2f643331757a386c77666d796e38672e636c6f756466726f6e742e6e65742f4173736574732f6c6f676f2d68656e72792d77686974652d6c672e706e67)

</div>
<center><h1><b> 
	PROYECTO INDIVIDUAL Nº1 <br>
<h1>Machine Learning Operations (MLOps)</h1> </b></h1></center><br>
	



<div align="center"> Henry's Labs <br>
	 by  William Andres Agurto Prado (DTS-09) </div>

<div align="center">

![](https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png)

</div>

### **Project Estructure**

------------
This is my first individual project focus on doing ETL(Extract, Transform and load), EDA (Exploratory data Analysis).<br><br>

### **Project Development**

------------
**1. ETL Process Stage ➡️**
Main file: [etl_principal.ipynb](https://github.com/WilliamAgurto/PI_01/blob/main/ETL.ipynb)
- The ETL (Extraction, Transformation, and Load) process was carried out.
- The necessary dataframes for the process were prepared, resulting from the treatment of the four provided datasets (amazon_prime_titles.csv, disney_plus_titles.csv, hulu_titles.csv, netflix_titles.csv) of movies and series (titles).
- A single dataframe was prepared for the treatment of the eight provided datasets with information on the ratings.
- The required MVP (Minimum Viable Product) tasks were performed by:<br>

		i. Some fields, such as belongs_to_collection, production_companies, and others (see data dictionary), are nested, meaning they either have a dictionary or a list as values in each row. You will need to unnest them in order to join them back to the dataset or find a way to access that data without unnesting.<br>

		ii.Null values in the revenue and budget fields should be filled with the number 0.<br>
	
		iii.Null values in the release date field should be removed.<br>
	
		iv. If there are dates, they should have the format YYYY-mm-dd, and a release_year column should be created to extract the year from the release date.<br>
	
		v. Create a column for return on investment, called "return," by dividing revenue by budget. When data is not available to calculate this, it should be set to 0.<br>
        
        vi.Remove columns that will not be used: video, imdb_id, adult, original_title, vote_count, poster_path, and homepage.<br>

**2. API Development Stage ➡️**
Main file: [main.py](https://github.com/WilliamAgurto/PI_01/blob/main/FirstApi/main.py)
- The process of making the information available through the FastAPI framework was carried out.
- The Render cloud was used to deploy the project.
[Access to the documentation on render.com](http://127.0.0.1:8000/docs#/default/return__return__movie__get) where you can access all the developed queries.

- The required MVP queries (functions) were performed:<br>

		i. defpeliculas_mes(mes):
            You enter the month and the function returns the number of movies that were historically released that month (month name, as str, example 'January')
            return {'mes':mes, 'cantidad':respuesta}.

        ii. def peliculas_dia(dia):
            You enter the day and the function returns the number of movies that were historically released that day (of the week, as str, example 'Monday')
            return {'dia':dia, 'cantidad':respuesta}.

        iii.def franquicia(franquicia):
            You enter the franchise, returning the number of movies, total profit and average profit
            return {'franquicia':franquicia, 'cantidad':respuesta, 'ganancia_total':respuesta, 'ganancia_promedio':respuesta}.

        iv. def peliculas_pais(pais):
            You enter the country, returning the number of movies produced in it
            return {'pais':pais, 'cantidad':respuesta}.

        v. def productoras(productora):
            '''You enter the production company, returning the total profit and number of movies produced'''
            return {'productora':productora, 'ganancia_total':respuesta, 'cantidad':respuesta}

        vi. def retorno(pelicula):
            You enter the movie, returning the investment, profit, return and year in which it was released
            return {'pelicula':pelicula, 'inversion':respuesta, 'ganacia':respuesta,'retorno':respuesta, 'anio':respuesta}<br><br>


**3. Exploratory Data Analysis Stage ➡️** Main file: [eda_principal.ipynb](https://github.com/WilliamAgurto/PI_01_ML_OPS/blob/master/EDA.ipynb)

- The required MVP tasks were performed:
- The dataframe (movie_dataset) were analyzed in terms of their structure, shape, information, null values, duplicate values, etc.
- Histograms were created on Matplotlib and Seaborn to obtain a general overview of the data distribution of the movie and series dataframe.<br><br>

**4. Recommendation System Stage ➡️**
Main file: [RecommendationSystem.ipynb](https://github.com/WilliamAgurto/PI_01/blob/main/RecomendationSystem.ipynb)
-  TfidfVectorizer library was used in order to achieve project requests and this was used on FastApi.<br><br>

**Data Source  ➡️** [Data](https://github.com/WilliamAgurto/PI_01/tree/main/datasets)
------------

Datasets: The folder contains two files..<br><br>

**Supporting Material ⚪** 
------------

In this same repository, you can find some helpful links. they were useful to achive the project requests.<br>
Click on [here](https://github.com/WilliamAgurto/PI_01_ML_OPS/blob/master/SupportMaterial.md) if you want to check some of them.
