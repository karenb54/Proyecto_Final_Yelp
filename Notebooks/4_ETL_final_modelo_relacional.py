"""Antes de ejecutar este código, debemos tener los datos
 preprocesados meta_df.parquet en Google."""
#ULTIMO PASO DEL ETL

import polars as pl
import pandas as pd
from google.cloud import storage
import gcsfs
import warnings
import time

start_time = time.time()

#ignorar todos los warnings
warnings.filterwarnings("ignore")

#configuración de la autenticación y detalles del bucket
CREDENTIALS_FILE = "credencial_karen_propietario.json"  #ruta al archivo de credenciales
BUCKET_NAME = "bucket-proyecto-final-1"  #nombre del bucket
PARQUET_PATH = "datos-limpios/yelp/meta_df.parquet"  #ruta relativa del archivo Parquet
LOCAL_TEMP_PATH = "temp_filtered.parquet"  #archivo temporal para subida

#configuración del cliente de GCS
storage_client = storage.Client.from_service_account_json(CREDENTIALS_FILE)
bucket = storage_client.bucket(BUCKET_NAME)

#leer archivos Parquet desde GCS con Polars
def read_parquet(bucket_name, remote_path):
    """Lee un archivo Parquet desde Google Cloud Storage usando Polars."""
    gcsfs_client = gcsfs.GCSFileSystem(token=CREDENTIALS_FILE)
    full_path = f"gs://{bucket_name}/{remote_path}"
    return pl.read_parquet(gcsfs_client.open(full_path))

#guardar DataFrame en GCS
def save_parquet_to_gcs(df, bucket_name, remote_path):
    """Guarda un DataFrame como archivo Parquet en Google Cloud Storage."""
    local_temp_path = LOCAL_TEMP_PATH
    
    #guardar localmente en formato Parquet
    df.write_parquet(local_temp_path)
    
    #subir a GCS
    blob = bucket.blob(remote_path)
    blob.upload_from_filename(local_temp_path)
    print(f"Archivo guardado exitosamente en: gs://{bucket_name}/{remote_path}")

#leer los datos desde GCS
try:
    df = read_parquet(BUCKET_NAME, PARQUET_PATH)
    print("Archivo Parquet leído correctamente desde Google Cloud Storage.")
except FileNotFoundError as e:
    print(f"Error: No se encontró el archivo en GCS. Verifica la ruta: {PARQUET_PATH}")
    raise e

#filtrar los estados que vamos a analizar
estados_elegidos = ['PA', 'TN', 'FL']
df_filtrado = df.filter(df['state'].is_in(estados_elegidos))

#calcular el porcentaje del DataFrame filtrado
total_filas_df = df.height
total_filas_df_filtrado = df_filtrado.height
porcentaje = (total_filas_df_filtrado / total_filas_df) * 100
print(f"Hemos filtrado el {porcentaje:.2f}% del DataFrame preprocesado.")

#crear tablas según el modelo relacional
#tabla Dimensión LOCALES
df_locales = df_filtrado.select([
    pl.col("business_id").alias("id_local"),
    pl.col("name").alias("name"),
    pl.col("state").alias("id_state"),
    pl.col("categories").alias("category")
]).unique()

#tabla Dimensión ESTADOS
estado_poblacion = {
    "PA": {"name_state": "Pennsylvania", "population": 13002700, "income": 63000},
    "TN": {"name_state": "Tennessee", "population": 6897576, "income": 52000},
    "FL": {"name_state": "Florida", "population": 21646155, "income": 59000},
}
df_estados = pl.DataFrame([
    {"id_state": key, **value} for key, value in estado_poblacion.items()
])

#tabla de Hecho REVIEW 
df_reviews = df_filtrado.select([
    pl.col("user_id").alias("id_user"),
    pl.col("business_id").alias("id_local"),
    pl.col("date").alias("time"),
    pl.col("text").alias("review_text"),
    pl.col("stars_x").alias("stars_review")  
])

#convertir df_locales a Pandas para filtrar categorías específicas
categorias_elegidas = ["restaurant", "fast food", "seafood"]
df_locales_pandas = df_locales.to_pandas()

#filtrar cztegorías en Pandas
df_locales_pandas['category'] = df_locales_pandas['category'].apply(lambda x: [cat.lower() for cat in x])
df_locales_filtrado_pandas = df_locales_pandas[
    df_locales_pandas['category'].apply(lambda x: any(cat in categorias_elegidas for cat in x))
]

#convertir de nuevo a Polars
df_locales_filtrado = pl.from_pandas(df_locales_filtrado_pandas)

#tabla Modelo para ML
df_modelo = df_reviews.join(
    df_locales_filtrado.select(["id_local", "id_state"]),
    on="id_local",
    how="inner"  #join interno por id_local
).select([
    pl.col("id_local"),
    pl.col("time"),
    pl.col("review_text"),
    pl.col("stars_review"),
    pl.col("id_state")
])

#guardar las tablas en GCS
save_parquet_to_gcs(df_locales, BUCKET_NAME, "datos-limpios/yelp/tabla_dim_locals.parquet")
save_parquet_to_gcs(df_estados, BUCKET_NAME, "datos-limpios/yelp/tabla_dim_estados.parquet")
save_parquet_to_gcs(df_reviews, BUCKET_NAME, "datos-limpios/yelp/tabla_hecho_reviews.parquet")
save_parquet_to_gcs(df_modelo, BUCKET_NAME, "datos-limpios/yelp/tabla_modelo.parquet")  # cuarta tabla para ML

elapsed_time = time.time() - start_time
print(f"Tiempo total de ejecución: {elapsed_time:.2f} segundos")

#github: https://github.com/matiasoviedo28
