import os
import dask.dataframe as dd
import pyarrow as pa
import pyarrow.parquet as pq
from google.cloud import storage
import pandas as pd
import json
import time
start_time = time.time()

# Ruta absoluta (ajusta según tu sistema)
CREDENTIALS_FILE = r"D:\DOCUMENTOS\DATA_SCIENCE\Documentos proyecto final\Proyecto_Final_Yelp\Notebooks\credencial_karen_propietario.json"
LOCAL_DATASETS_DIR = r"D:\DOCUMENTOS\DATA_SCIENCE\Documentos proyecto final\Proyecto_Final_Yelp\Datasets"

FILES_TO_CONVERT = {
    "business.pkl": "business.parquet",
    "review.json": "review.parquet",
    "checkin.json": "checkin.parquet",
    "tip.json": "tip.parquet",
    "user.parquet": "user.parquet",  # Ya está en formato Parquet
}

# Configuración de Google Cloud Storage (GCS)
BUCKET_NAME = "bucket-proyecto-final-1"
REMOTE_DATASETS_DIR = "datos-crudos/Yelp/"

def convert_and_upload_to_gcs():
    """Convierte archivos locales a Parquet y los sube a Google Cloud Storage."""
    print("Iniciando conversión y subida de archivos a Google Cloud Storage...")

    # Inicializar cliente de Google Cloud Storage
    storage_client = storage.Client.from_service_account_json(CREDENTIALS_FILE)
    bucket = storage_client.bucket(BUCKET_NAME)

    # Procesar cada archivo
    for local_file, parquet_file in FILES_TO_CONVERT.items():
        local_path = os.path.join(LOCAL_DATASETS_DIR, local_file)
        parquet_path = os.path.join(LOCAL_DATASETS_DIR, parquet_file)
        remote_path = os.path.join(REMOTE_DATASETS_DIR, parquet_file)

        # Verificar si el archivo local existe
        if not os.path.exists(local_path):
            print(f"Archivo no encontrado: {local_path}. Saltando...")
            continue

        # Convertir archivo al formato Parquet si es necesario
        if not local_file.endswith(".parquet"):
            print(f"Convirtiendo {local_file} a {parquet_file}...")

            if local_file.endswith(".pkl"):
                df = pd.read_pickle(local_path)
                # Verificar y eliminar columnas duplicadas
                df = df.loc[:, ~df.columns.duplicated()]

            elif local_file.endswith(".json") or local_file.endswith(".json.crdownload"):
                if local_file == "review.json":
                    # Convertir 'review.json' en fragmentos
                    parquet_writer = None
                    chunk = []
                    with open(local_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            # Leer línea por línea el archivo JSON
                            chunk.append(json.loads(line))

                            # Si el tamaño del chunk alcanza un límite, convertirlo a Parquet
                            if len(chunk) >= 100000:  # Ajusta este número según el tamaño de tu memoria disponible
                                df_chunk = pd.DataFrame(chunk)
                                table = pa.Table.from_pandas(df_chunk)

                                # Inicializar el escritor de Parquet si es la primera vez
                                if parquet_writer is None:
                                    parquet_writer = pq.ParquetWriter(parquet_path, table.schema)

                                # Escribir el fragmento en el archivo Parquet
                                parquet_writer.write_table(table)

                                # Limpiar el chunk
                                chunk = []

                    # Escribir cualquier fragmento restante que no se haya escrito
                    if chunk:
                        df_chunk = pd.DataFrame(chunk)
                        table = pa.Table.from_pandas(df_chunk)
                        parquet_writer.write_table(table)

                    # Cerrar el escritor de Parquet
                    if parquet_writer:
                        parquet_writer.close()
                    print(f"Archivo review.json convertido a Parquet en fragmentos: {parquet_path}")

                else:
                    # Leer el archivo JSON usando dask para otros archivos pequeños
                    df = dd.read_json(local_path, lines=True)
                    # Convertir a pandas para guardar como Parquet
                    df = df.compute()
                    # Guardar como Parquet
                    table = pa.Table.from_pandas(df)
                    pq.write_table(table, parquet_path)
                    print(f"Archivo {local_file} convertido a Parquet: {parquet_path}")
            else:
                print(f"Formato no soportado para {local_file}.")
                continue
        else:
            parquet_path = local_path  # Ya es Parquet

        # Verificar si el archivo ya existe en Google Cloud Storage
        blob = bucket.blob(remote_path)
        if blob.exists():
            print(f"El archivo {parquet_file} ya existe en Google Cloud Storage. Saltando...")
        else:
            # Subir a Google Cloud Storage
            print(f"Subiendo {parquet_file} a Google Cloud Storage...")
            blob.upload_from_filename(parquet_path)
            print(f"Archivo subido exitosamente: gs://{BUCKET_NAME}/{remote_path}")

    print("Proceso de conversión y subida completado.")

if __name__ == "__main__":
    convert_and_upload_to_gcs()
    elapsed_time = time.time() - start_time
    print(f"Tiempo total de ejecución: {elapsed_time:.2f} segundos")