"""Antes de ejecutar este codigo, debemos 
tener los datos preprocesados meta_df.parquet en google"""

import polars as pl
from google.cloud import storage
import gcsfs
import warnings

import time
start_time = time.time()

# Ignorar todos los warnings
warnings.filterwarnings("ignore")

# Configuración de la autenticación y detalles del bucket
CREDENTIALS_FILE = "credencial_karen_propietario.json"  # Ruta al archivo de credenciales
BUCKET_NAME = "bucket-proyecto-final-1"  # Nombre del bucket
PARQUET_PATH = "datos-limpios/yelp/meta_df.parquet"  # Ruta relativa del archivo Parquet
LOCAL_TEMP_PATH = "temp_filtered.parquet"  # Archivo temporal para subida

# Configuración del cliente de Google Cloud Storage
storage_client = storage.Client.from_service_account_json(CREDENTIALS_FILE)
bucket = storage_client.bucket(BUCKET_NAME)

# Leer archivos Parquet desde Google Cloud Storage con Polars
def read_parquet(bucket_name, remote_path):
    """Lee un archivo Parquet desde Google Cloud Storage usando Polars."""
    gcsfs_client = gcsfs.GCSFileSystem(token=CREDENTIALS_FILE)
    full_path = f"gs://{bucket_name}/{remote_path}"
    return pl.read_parquet(gcsfs_client.open(full_path))

# Guardar DataFrame en Google Cloud Storage
def save_parquet_to_gcs(df, bucket_name, remote_path):
    """Guarda un DataFrame como archivo Parquet en Google Cloud Storage."""
    local_temp_path = LOCAL_TEMP_PATH
    
    # Guardar localmente en formato Parquet
    df.write_parquet(local_temp_path)
    
    # Subir a Google Cloud Storage
    blob = bucket.blob(remote_path)
    blob.upload_from_filename(local_temp_path)
    print(f"Archivo guardado exitosamente en: gs://{bucket_name}/{remote_path}")

# Leer los datos desde Google Cloud Storage
try:
    df = read_parquet(BUCKET_NAME, PARQUET_PATH)
    print("Archivo Parquet leído correctamente desde Google Cloud Storage.")
except FileNotFoundError as e:
    print(f"Error: No se encontró el archivo en GCS. Verifica la ruta: {PARQUET_PATH}")
    raise e

# Filtrar los estados que vamos a analizar
estados_elegidos = ['PA', 'TN', 'FL']
df_filtrado = df.filter(df['state'].is_in(estados_elegidos))

# Calcular el porcentaje del DataFrame filtrado
total_filas_df = df.height
total_filas_df_filtrado = df_filtrado.height
porcentaje = (total_filas_df_filtrado / total_filas_df) * 100
print(f"Hemos filtrado el {porcentaje:.2f}% del DataFrame preprocesado.")

# Crear tablas según el modelo relacional
# Tabla Dimensión LOCALES
df_locales = df_filtrado.select([
    pl.col("business_id").alias("id_local"),
    pl.col("name").alias("name"),
    pl.col("state").alias("id_state"),
    pl.col("categories").alias("category")
]).unique()  # Reemplazamos drop_duplicates() con unique()

# Tabla Dimensión ESTADOS
estado_poblacion = {
    "PA": {"name_state": "Pennsylvania", "population": 13002700, "income": 63000},
    "TN": {"name_state": "Tennessee", "population": 6897576, "income": 52000},
    "FL": {"name_state": "Florida", "population": 21646155, "income": 59000},
}
df_estados = pl.DataFrame([
    {"id_state": key, **value} for key, value in estado_poblacion.items()
])

# Tabla de Hecho REVIEW
df_reviews = df_filtrado.select([
    pl.col("user_id").alias("id_user"),
    pl.col("business_id").alias("id_local"),
    pl.col("date").alias("time"),
    pl.col("text")
])

# Guardar las tablas en Google Cloud Storage
save_parquet_to_gcs(df_locales, BUCKET_NAME, "datos-limpios/yelp/tabla_dim_locals.parquet")
save_parquet_to_gcs(df_estados, BUCKET_NAME, "datos-limpios/yelp/tabla_dim_estados.parquet")
save_parquet_to_gcs(df_reviews, BUCKET_NAME, "datos-limpios/yelp/tabla_hecho_reviews.parquet")

elapsed_time = time.time() - start_time
print(f"Tiempo total de ejecución: {elapsed_time:.2f} segundos")