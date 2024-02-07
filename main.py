from fastapi import FastAPI
from typing import List, Optional
from fastapi.exceptions import HTTPException
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise        import cosine_similarity
from sklearn.metrics.pairwise        import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer


app=FastAPI(debug=True)

df = pd.read_csv('data_final.csv')

@app.get("/")
def Proyecto_de_Angel_Jaramillo():
    return "Hello World My name is Angel "


    # Ejercicio 1

@app.get("/Developer_Stats/")
def get_developer_stats(developer: str) -> List[dict]:
    # Filtrar solo juegos del desarrollador proporcionado
    df_selected_developer = df[df['developer'].str.lower() == developer.lower()]

    if df_selected_developer.empty:
        raise HTTPException(status_code=404, detail="Desarrollador no encontrado")

    # Filtrar solo juegos 'Free to Play'
    df_free_to_play = df_selected_developer[df_selected_developer['price'].str.lower().str.contains('free', na=False)]

    if df_free_to_play.empty:
        raise HTTPException(status_code=404, detail=f"No hay juegos gratuitos ('Free to Play') para el desarrollador {developer}")

    # Agrupar por año
    grouped = df_free_to_play.groupby('year')

    # Calcular la cantidad de items y el porcentaje de contenido Free
    result = grouped.agg({'items_count': 'sum', 'title': 'count'}).rename(columns={'title': 'free_games_count'})
    result['percentage_free'] = round((result['free_games_count'] / result['items_count']) * 100, 1)

    # Convertir el resultado a formato JSON
    result_json = result.reset_index().to_dict(orient='records')

    # Modificar la respuesta para tener el formato deseado
    response = [{"year": entry["year"], "items_count": entry["items_count"], "free content": f"{entry['percentage_free']}%"} for entry in result_json]

    return response


        # Ejercicio 2 
@app.get('/User_Data/')
def userdata(User_id: str) -> dict:
    # Filtramos el DataFrame para obtener solo las filas asociadas al usuario especificado
    user_df = df[df['user_id'] == User_id]

    if user_df.empty:
        return {"Mensaje": f"No hay datos disponibles para el usuario {User_id}."}

    # Calculamos la cantidad de dinero gastado por el usuario sumando los precios de los items comprados
    dinero_gastado = user_df['price'].sum()

    # Calculamos el porcentaje de recomendación basado en la columna 'recommend'
    porcentaje_recomendacion = (user_df['recommend'].sum() / len(user_df)) * 100

    # Calculamos la cantidad de items del usuario
    cantidad_items = len(user_df)

    # Construimos el resultado como un diccionario
    resultado = {"Usuario": User_id, "Dinero gastado": f"{dinero_gastado:.2f} USD", "% de recomendación": f"{porcentaje_recomendacion:.2f}%", "Cantidad de items": cantidad_items}

    return resultado


        # Ejercicio 3
@app.get('/User_For_Genre/')
def UserForGenre(genero: str) -> dict:
    # Convertimos la primera letra del género a mayúscula para asegurarnos de que coincida con los datos
    genero = genero.capitalize()
    # Filtramos el DataFrame para obtener solo las filas asociadas al género especificado
    genre_df = df[df[genero] == 1]
    if genre_df.empty:
        return {"Mensaje": f"No hay datos disponibles para el género {genero}."}
    # Encontramos el usuario con más horas jugadas para el género dado
    max_playtime_user = genre_df.loc[genre_df['playtime_forever'].idxmax(), 'user_id']
    # Agrupamos por año y sumamos las horas jugadas para cada año
    year_playtime_df = genre_df.groupby('year')['playtime_forever'].sum().reset_index()
    # Construimos la lista de acumulación de horas jugadas por año en el formato requerido
    horas_jugadas_por_año = [{"Año": int(row['year']), "Horas": int(row['playtime_forever'])} for _, row in year_playtime_df.iterrows()]
    # Construimos el resultado como un diccionario
    resultado = {"Usuario con más horas jugadas para Género": max_playtime_user, "Horas jugadas": horas_jugadas_por_año}

    return resultado


    # Ejercicio 4
@app.get('/Best_Developer/')
def best_developer_year(year: int) -> list[dict]:
    # Filtra el DataFrame para el año dado y con análisis de sentimiento positivo
    df_filtrado = df[(df['year'] == year) & (df['sentiment_analysis'] == 2)]

    # Agrupa por desarrollador y cuenta el número de recomendaciones
    df_agrupado = df_filtrado.groupby('developer')['sentiment_analysis'].count().reset_index()

    # Ordena en orden descendente y toma los primeros 3
    df_top_3 = df_agrupado.sort_values(by='sentiment_analysis', ascending=False).head(3)

    # Construye el resultado en el formato requerido con puestos consecutivos de 1 a 3
    resultado = [{"Puesto " + str(i + 1): row['developer']} for i, (_, row) in enumerate(df_top_3.iterrows(), start=0)]

    return resultado


        # Ejercicio 5
@app.get('/Sentiment_Analysis/')
def developer_reviews_analysis(desarrollador: str) -> dict:
    # Filtrar el DataFrame por el desarrollador proporcionado
    df_selected_developer = df[df['developer'].str.lower() == desarrollador.lower()]

    # Contar los registros de reseñas categorizadas como positivas y negativas
    positive_count = df_selected_developer[df_selected_developer['sentiment_analysis'] == 2].shape[0]
    negative_count = df_selected_developer[df_selected_developer['sentiment_analysis'] == 0].shape[0]

    # Crear el diccionario de retorno
    result = {desarrollador: {'Positive': positive_count, 'Negative': negative_count}}

    return result

muestra = df.head(5000)
tfidf = TfidfVectorizer(stop_words='english')
muestra=muestra.fillna("")

tdfid_matrix = tfidf.fit_transform(muestra['review'])
cosine_similarity = linear_kernel( tdfid_matrix, tdfid_matrix)


@app.get('/recomendacion_id/{id_producto}')
def recomendacion(id_producto: int):
    if id_producto not in muestra['steam_id'].values:
        return {'mensaje': 'No existe el id del juego.'}
    
    # Obtener géneros del juego con el id_producto
    generos = muestra.columns[4:19]  # Obtener los nombres de las columnas de género
    
    # Filtrar el dataframe para incluir juegos con géneros coincidentes pero con títulos diferentes
    filtered_df = muestra[(muestra[generos] == 1).any(axis=1) & (muestra['steam_id'] != id_producto)]
    
    # Calcular similitud del coseno
    tdfid_matrix_filtered = tfidf.transform(filtered_df['review'])
    cosine_similarity_filtered = linear_kernel(tdfid_matrix_filtered, tdfid_matrix_filtered)
    
    idx = muestra[muestra['steam_id'] == id_producto].index[0]
    sim_cosine = list(enumerate(cosine_similarity_filtered[idx]))
    sim_scores = sorted(sim_cosine, key=lambda x: x[1], reverse=True)
    sim_ind = [i for i, _ in sim_scores[1:6]]
    sim_juegos = filtered_df['title'].iloc[sim_ind].values.tolist()
    
    return list(set(sim_juegos))


@app.get('/recomendacion_usuario/{id_usuario}')
def recomendacion_usuario(id_usuario: int):
    juegos_recomendados = set()  # Utilizamos un conjunto para evitar juegos duplicados
    
    # Obtener los juegos recomendados para el usuario
    for idx, row in muestra.iterrows():
        if row['id'] == id_usuario:
            sim_cosine = list(enumerate(cosine_similarity[idx]))
            sim_scores = sorted(sim_cosine, key=lambda x: x[1], reverse=True)
            sim_ind = [i for i, _ in sim_scores[1:6]]
            sim_juegos = muestra['title'].iloc[sim_ind].values.tolist()
            juegos_recomendados.update(sim_juegos)  # Agregar los juegos recomendados al conjunto
    
    return list(juegos_recomendados)