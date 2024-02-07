# Machine Learning Operations (MLOps)
## Sistema de Recomendación de Videojuegos usando Machine Learning
[![imagen](imagen "imagen")](https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png "imagen")

### Introducción
Este proyecto consiste en un sistema de recomendación de videojuegos utilizando técnicas de aprendizaje automático. El sistema está desarrollado en Python con el framework FastAPI y utiliza un conjunto de datos de la plataforma Steam. Los usuarios pueden obtener recomendaciones personalizadas basadas en diferentes criterios.

### **Librerías Utilizadas**
Pandas
Matplotlib
Numpy
Seaborn
Wordcloud
NLTK
Uvicorn
Render
FastAPI
Python
Scikit-Learn

### **Características del Proyecto**  

**Extracción, Transformación y Carga (ETL)**: Se llevó a cabo un proceso de ETL para limpiar y preprocesar los datos de Steam, asegurando que estén listos para el análisis y la construcción del modelo de recomendación.

**Análisis Exploratorio de Datos (EDA):** Se realizó un análisis exhaustivo de los datos para entender su estructura y características. Esto incluyó la visualización de distribuciones, análisis de correlaciones y tendencias temporales, entre otros.

**Modelado de Recomendación: **Se implementó un modelo de recomendación basado en similitud de contenido utilizando la técnica de similitud del coseno. Esto permite recomendar videojuegos similares a un juego específico o a los juegos que un usuario ha jugado previamente.


###  **Endpoints API**
El sistema cuenta con los siguientes endpoints API:

**/Developer_Stats/:** Proporciona estadísticas sobre los juegos desarrollados por un desarrollador específico, incluyendo la cantidad de juegos gratuitos ('Free to Play') y el porcentaje de contenido gratuito.

**/User_Data/:** Devuelve información sobre un usuario específico, como el dinero gastado en juegos, el porcentaje de recomendación y la cantidad de juegos adquiridos.

**/User_For_Genre/:** Ofrece detalles sobre el usuario que ha jugado más horas en un género de videojuegos determinado, junto con las horas jugadas por año para ese género.

**/Best_Developer/:** Muestra los tres mejores desarrolladores en términos de recomendaciones positivas para un año específico.

**/Sentiment_Analysis/:** Realiza un análisis de sentimiento de las reseñas de un desarrollador específico, contando la cantidad de reseñas positivas y negativas.

**/recomendacion_id/{id_producto}:** Recomienda juegos similares a un juego específico identificado por su ID de producto.

**/recomendacion_usuario/{id_usuario}:** Recomienda juegos para un usuario específico basado en su historial de juego.

### Estructura del Proyecto

El proyecto está estructurado de la siguiente manera:

**main.py:** Contiene el código principal de la aplicación FastAPI, incluyendo la definición de los endpoints API y la lógica de negocio.

**data_final.csv:** Archivo CSV que contiene los datos de Steam utilizados en el proyecto.

**README.md:** Este archivo, que proporciona una visión general del proyecto, sus características y su estructura.

### **Demostración en Render y YouTube**

El proyecto está desplegado en [**ML-OPS**](https://ml-ops-angel-jaramillo.onrender.com/docs "Render")
Puedes ver una demostración en [**VIDEO**](https://www.youtube.com/watch?v=Rw887TSEQz0 "Video")  en  YouTube