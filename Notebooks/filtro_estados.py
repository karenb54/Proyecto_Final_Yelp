"""Antes de ejecutar este codigo, debemos 
tener los datos preprocesados meta_df.parquet en google"""

import polars as pl
from google.cloud import storage
import gcsfs
import warnings

#ignorar todos los warnings
warnings.filterwarnings("ignore")

#configuración de la autenticación y creación de FileSystem
CREDENTIALS_FILE = "credencial_karen_propietario.json"  #ruta al archivo de credenciales
#CREDENTIALS_FILE = r"D:\DOCUMENTOS\DATA_SCIENCE\Documentos proyecto final\Proyecto_Final_Yelp\Notebooks\credencial_karen_propietario.json"
BUCKET_NAME = "bucket-proyecto-final-1"  #nombre del bucket
REMOTE_PATH = "datos-limpios/yelp/df_estados_filtrados.parquet"  #ruta en GCS donde guardar el archivo

#ruta al archivo Parquet que incluye wildcard para múltiples archivos
PARQUET_PATH = 'gs://bucket-proyecto-final-1/datos-limpios/yelp/meta_df.parquet'

#autenticación con GCS
fs = gcsfs.GCSFileSystem(token=CREDENTIALS_FILE)

#leer los archivos Parquet directamente en un DataFrame de Polars
def read_parquet_files(path):
    files = fs.glob(path)
    frames = [pl.read_parquet(fs.open(file)) for file in files]
    return pl.concat(frames)

#inicializar cliente de Google Cloud Storage
storage_client = storage.Client.from_service_account_json(CREDENTIALS_FILE)
bucket = storage_client.bucket(BUCKET_NAME)

#leer datos desde Google Cloud Storage
df = read_parquet_files(PARQUET_PATH)

#filtrar los estados que vamos a analizar
estados_elegidos = ['CA', 'IL', 'NY', 'FL']
df_filtrado = df.filter(df['state'].is_in(estados_elegidos))

#obtener el total de filas
total_filas_df = df.height
total_filas_df_filtrado = df_filtrado.height

#calcular el porcentaje
porcentaje = (total_filas_df_filtrado / total_filas_df) * 100
print(f"Hemos filtrado el {porcentaje:.2f}% del DataFrame preprocesado.")

#guardar el DataFrame filtrado como archivo Parquet en GCS
def save_parquet_to_gcs(df, bucket_name, remote_path):
    """Guarda un DataFrame de Polars como archivo Parquet en Google Cloud Storage."""
    local_temp_path = "temp_filtered.parquet"
    
    #guardar localmente en formato Parquet
    df.write_parquet(local_temp_path)
    
    #subir a Google Cloud Storage
    blob = bucket.blob(remote_path)
    blob.upload_from_filename(local_temp_path)
    print(f"Archivo guardado exitosamente en: gs://{bucket_name}/{remote_path}")

#llamar a la función para guardar
save_parquet_to_gcs(df_filtrado, BUCKET_NAME, REMOTE_PATH)
