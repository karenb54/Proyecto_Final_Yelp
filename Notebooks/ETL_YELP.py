"""
ETL para estructurar los datos para ser utilizados en analis futuros.
Analizaremos todos los archivos brindados en el dataset de YELP y exportaremos 
solo un meta_df.parquet donde ya estarán vinculados los ID para filtrar y tomar
solo los datos importantes.
github: https://github.com/matiasoviedo28
"""

import pandas as pd
import time
import json

#iniciar el temporizador
start_time = time.time()

#cargar los datos
df_reviews = pd.read_json('review.json', lines=True)
print("df review cargados")
df_business = pd.read_pickle('business.pkl')
print("df business cargados")

#manejo de nulos en df_reviews
df_reviews.dropna(how='all', inplace=True)
umbral_nulos_reviews = 0.7 * len(df_reviews)
df_reviews.dropna(thresh=umbral_nulos_reviews, axis=1, inplace=True)
for columna in df_reviews.columns:
    if df_reviews[columna].dtype in ['float64', 'int64']:
        df_reviews[columna].fillna(df_reviews[columna].mean(), inplace=True)
    else:
        df_reviews[columna].fillna('valor incompleto', inplace=True)
print("nulos manejados en reviews")

#manejo de nulos en df_business
df_business.dropna(how='all', inplace=True)
umbral_nulos_business = 0.7 * len(df_business)
df_business.dropna(thresh=umbral_nulos_business, axis=1, inplace=True)
for columna in df_business.columns:
    if df_business[columna].dtype in ['float64', 'int64']:
        df_business[columna].fillna(df_business[columna].mean(), inplace=True)
    else:
        df_business[columna].fillna('valor incompleto', inplace=True)
print("nulos manejados en business")

#eliminar columnas duplicadas en df_business
df_business = df_business.loc[:, ~df_business.columns.duplicated()]

#convertir las columnas problematicas a un formato consistente
df_business['attributes'] = df_business['attributes'].apply(lambda x: json.dumps(x) if isinstance(x, dict) else str(x))
df_business['hours'] = df_business['hours'].apply(lambda x: json.dumps(x) if isinstance(x, dict) else str(x))

print("Datos cargados y valores nulos manejados.")
df_reviews.to_json('review.json', orient='records', lines=True)
print("review sobreescrito con nulos resueltos")
df_business.to_pickle('business.pkl')
print("business sobreescrito con nulos resueltos")

#########################################################

#tamano del chunk (numero de filas por chunk)
chunk_size = 100000

#diccionarios para acumular resultados de los usuarios
user_review_counts = {}
user_useful_sums = {}

#leer el archivo en chunks y procesar cada chunk
for chunk in pd.read_json('review.json', lines=True, chunksize=chunk_size):
    #verificar si 'user_id', 'review_id' y 'useful' estan en el chunk
    if all(col in chunk.columns for col in ['user_id', 'review_id', 'useful']):
        #seleccionar solo las columnas necesarias
        chunk_filtered = chunk[['user_id', 'review_id', 'useful']]

        #agrupar por 'user_id' en cada chunk
        chunk_grouped = chunk_filtered.groupby('user_id').agg({'review_id': 'count', 'useful': 'sum'})

        #acumular resultados en los diccionarios
        for user_id, row in chunk_grouped.iterrows():
            if user_id in user_review_counts:
                user_review_counts[user_id] += row['review_id']
                user_useful_sums[user_id] += row['useful']
            else:
                user_review_counts[user_id] = row['review_id']
                user_useful_sums[user_id] = row['useful']

print("Procesamiento de chunks finalizado")

#convertir los diccionarios a un dataframe
df_users = pd.DataFrame({
    'user_id': list(user_review_counts.keys()),
    'review_id': list(user_review_counts.values()),
    'useful': list(user_useful_sums.values())
})
print("diccionarios en df listos")

#definir el status 'top' o 'regular' basado en cuartiles
review_quantile = df_users['review_id'].quantile(0.75)
useful_quantile = df_users['useful'].quantile(0.75)

#definir el status 'top' o 'regular' utilizando operaciones vectorizadas
df_users['status'] = 'regular'  #inicialmente, todos son 'regular'
df_users.loc[
    (df_users['review_id'] > review_quantile) | (df_users['useful'] > useful_quantile), 
    'status'
] = 'top'

print("status definidos")

#filtrar solo los usuarios 'top'
df_top_users = df_users[df_users['status'] == 'top']
usuarios_seleccionados = df_top_users['user_id'].nunique()
total_usuarios = df_users['user_id'].nunique()
porcentaje_seleccionados = (usuarios_seleccionados / total_usuarios) * 100

print("usuarios top filtrados")
print(f"Usuarios seleccionados: {usuarios_seleccionados} ({porcentaje_seleccionados:.2f}% del total)")

#######################################################

#filtrar resenas solo de los usuarios 'top'
df_reviews_filtered = df_reviews[df_reviews['user_id'].isin(df_top_users['user_id'])]
print("usuarios top filtrados")

#confirmar la cantidad de resenas restantes
total_reseñas_original = len(df_reviews)
total_reseñas_filtradas = len(df_reviews_filtered)
print(f"Reseñas originales: {total_reseñas_original}, Reseñas después del filtrado: {total_reseñas_filtradas}")
print("cantidad de reseñas restantes verificadas")

##############################################################

#filtrar negocios en los que hay resenas de usuarios 'top'
df_business_filtered = df_business[df_business['business_id'].isin(df_reviews_filtered['business_id'])]
print("negocios con reseñas top filtrado")

#limpiar y separar categorias en df_business_filtered
df_business_filtered['categories'] = df_business_filtered['categories'].fillna('').astype(str).apply(lambda x: x.split(', '))
print("categorias separadas")

#eliminar columnas duplicadas y manejar nulos en df_business_filtered
df_business_filtered = df_business_filtered.loc[:, ~df_business_filtered.columns.duplicated()]
for columna in df_business_filtered.columns:
    if df_business_filtered[columna].dtype in ['float64', 'int64']:
        df_business_filtered[columna].fillna(df_business_filtered[columna].mean(), inplace=True)
    else:
        df_business_filtered[columna].fillna('valor incompleto', inplace=True)

print("Negocios filtrados y categorías procesadas.")

############################################################

#crear un dataframe combinado para exportar
meta_df = pd.merge(df_reviews_filtered, df_business_filtered, on='business_id')
print("df combinado meta_df combinado")

#exportar el dataframe combinado en formato parquet
meta_df.to_parquet('meta_df.parquet', index=False)
print("Archivo meta_df.parquet generado con éxito.")

#calcular el tiempo transcurrido
print("pulsa enter para cerrar")
elapsed_time = time.time() - start_time
print(f"Tiempo de ejecución: {elapsed_time:.2f} segundos")
input()

#########################################################