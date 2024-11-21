import polars as pl
import time
import gcsfs
from google.cloud import storage
import os
import json 

# Configuración de credenciales y entorno
CREDENTIALS_FILE = r"D:\DOCUMENTOS\DATA_SCIENCE\Documentos proyecto final\Proyecto_Final_Yelp\Notebooks\credencial_karen_propietario.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_FILE

BUCKET_NAME = "bucket-proyecto-final-1"
REMOTE_DATASETS_DIR = "datos-crudos/Yelp/"
client = storage.Client.from_service_account_json(CREDENTIALS_FILE)
bucket = client.bucket(BUCKET_NAME)

start_time = time.time()

# Función 1: Cargar datos desde Google Cloud Storage
def load_dataframes_from_gcs():
    print("Iniciando carga de datos desde Google Cloud Storage...")
    fs = gcsfs.GCSFileSystem(token=CREDENTIALS_FILE)

    path_business = "bucket-proyecto-final-1/datos-crudos/Yelp/business.parquet"
    path_reviews = "bucket-proyecto-final-1/datos-crudos/Yelp/review.parquet"

    with fs.open(path_business, "rb") as f:
        df_business = pl.read_parquet(f)
    with fs.open(path_reviews, "rb") as f:
        df_reviews = pl.read_parquet(f)
    
    print("df_business y df_reviews cargados exitosamente.")
    return df_business, df_reviews

# Función 2: Transformación y procesamiento
def transform_data(df_business, df_reviews):
    """Transforma y procesa los datos."""
    print("Iniciando transformación y procesamiento de datos...")
    
    # Filtrar filas con más del 70% de valores no nulos en df_reviews
    umbral_nulos_reviews = int(0.7 * df_reviews.shape[1])  # 70% de las columnas
    df_reviews = df_reviews.filter(
        pl.sum_horizontal(pl.all().is_not_null().cast(int)) > umbral_nulos_reviews
    )
    df_reviews = df_reviews.fill_null("valor incompleto")
    print("Nulos manejados en df_reviews.")
    
    # Filtrar filas con más del 70% de valores no nulos en df_business
    umbral_nulos_business = int(0.7 * df_business.shape[1])
    df_business = df_business.filter(
        pl.sum_horizontal(pl.all().is_not_null().cast(int)) > umbral_nulos_business
    )
    df_business = df_business.fill_null("valor incompleto")
    print("Nulos manejados en df_business.")
    
    # Eliminar duplicados
    df_business = df_business.unique()
    
    # Procesar columnas JSON
    df_business = df_business.with_columns([
        pl.col("attributes").cast(str).fill_null("null").alias("attributes"),
        pl.col("hours").json_encode().fill_null("null").alias("hours"),  # Usando json_encode()
    ])
    print("Transformaciones iniciales aplicadas.")
    
    # Filtrar usuarios 'top'
    user_counts = df_reviews.group_by("user_id").agg([
        pl.count("review_id").alias("review_count"),
        pl.sum("useful").alias("useful_count")
    ])
    
    review_quantile = user_counts["review_count"].quantile(0.75)
    useful_quantile = user_counts["useful_count"].quantile(0.75)
    
    df_top_users = user_counts.filter(
        (pl.col("review_count") > review_quantile) | (pl.col("useful_count") > useful_quantile)
    )
    df_reviews_filtered = df_reviews.filter(pl.col("user_id").is_in(df_top_users["user_id"]))
    df_business_filtered = df_business.filter(pl.col("business_id").is_in(df_reviews_filtered["business_id"]))
    
    print("Filtrado de datos completado.")
    
    # Procesar categorías
    df_business_filtered = df_business_filtered.with_columns([
        pl.col("categories").fill_null("").str.split(", ").alias("categories")
    ])
    print("Negocios y categorías procesadas.")
    
    return df_reviews_filtered, df_business_filtered

# Función 3: Exportar datos transformados
def export_transformed_data(df_reviews_filtered, df_business_filtered):
    print("Iniciando exportación de datos procesados...")
    
    # Combinar DataFrames
    preprocesado_yelp_df = df_reviews_filtered.join(df_business_filtered, on="business_id", how="inner")
    
    # Exportar localmente
    local_file_path = "preprocesado_yelp_df.parquet"
    preprocesado_yelp_df.write_parquet(local_file_path)
    print(f"Archivo {local_file_path} generado con éxito.")
    
    # Subir a Cloud Storage
    remote_path = "datos-preprocesados/Yelp/preprocesado_yelp_df.parquet"
    blob = bucket.blob(remote_path)
    if not blob.exists():
        blob.upload_from_filename(local_file_path)
        print(f"Archivo subido exitosamente: gs://{BUCKET_NAME}/{remote_path}")
    
    os.remove(local_file_path)
    print(f"Archivo {local_file_path} eliminado del sistema local.")

if __name__ == "__main__":
    df_business, df_reviews = load_dataframes_from_gcs()
    df_reviews_filtered, df_business_filtered = transform_data(df_business, df_reviews)
    export_transformed_data(df_reviews_filtered, df_business_filtered)
    elapsed_time = time.time() - start_time
    print(f"Tiempo total de ejecución: {elapsed_time:.2f} segundos")

#github: https://github.com/matiasoviedo28