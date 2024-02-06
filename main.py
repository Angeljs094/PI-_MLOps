from fastapi import FastAPI
from typing import List, Optional
from fastapi.exceptions import HTTPException
import pandas as pd
import numpy as np


app=FastAPI(debug=True)

df = pd.read_csv('data_final.csv')

@app.get("/")
def Angel_Jaramillo_Data_Analystic():
    return "Hello World My name is Angel "


    # Ejercicio 1

@app.get("/developer-stats/")
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
@app.get('/userdata/')
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
@app.get('/UserForGenre/')
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
@app.get('/Best_developer/')
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
@app.get('/sentiment_analysis/')
def developer_reviews_analysis(desarrollador: str) -> dict:
    # Filtrar el DataFrame por el desarrollador proporcionado
    df_selected_developer = df[df['developer'].str.lower() == desarrollador.lower()]

    # Contar los registros de reseñas categorizadas como positivas y negativas
    positive_count = df_selected_developer[df_selected_developer['sentiment_analysis'] == 2].shape[0]
    negative_count = df_selected_developer[df_selected_developer['sentiment_analysis'] == 0].shape[0]

    # Crear el diccionario de retorno
    result = {desarrollador: {'Positive': positive_count, 'Negative': negative_count}}

    return result