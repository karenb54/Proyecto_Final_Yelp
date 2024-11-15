from pyspark.sql import SparkSession
from google.cloud import storage
import glob
import os

# Creando sesión spark
spk = SparkSession.builder \
    .config("spark.driver.port", "4040") \
    .master("local[*]") \
    .appName("EDALocales") \
    .getOrCreate()

# Ruta absoluta (ajusta según tu sistema)
CREDENTIALS_FILE = r"/home/hugo/HENRY/Proyecto Final/credencial_karen_propietario.json"
LOCAL_DATASETS_DIR = r"/run/media/hugo/06368a0d-700b-4ac5-9159-173c295dcaed/Google/metadata-sitios"

# Configuración de Google Cloud Storage (GCS)
BUCKET_NAME = "bucket-proyecto-final-1"
REMOTE_DATASETS_DIR = "datos-crudos/Google/Sitios/"  # Review

def convert_and_upload_to_gcs():
    """Convierte archivos locales a Parquet y los sube a Google Cloud Storage."""
    print("Iniciando conversión y subida de archivos a Google Cloud Storage...")

    # Inicializar cliente de Google Cloud Storage
    storage_client = storage.Client.from_service_account_json(CREDENTIALS_FILE)
    bucket = storage_client.bucket(BUCKET_NAME)

    # Listar archivos locales con glob
    file_pattern = os.path.join(LOCAL_DATASETS_DIR, '*.json')
    files = glob.glob(file_pattern)

    if not files:
        print("No se encontraron archivos JSON en el directorio especificado.")
        return

    # Leer archivos con Spark
    df = spk.read.json(files)

    # Ruta para guardar archivos Parquet
    parquet_file_path = os.path.join(LOCAL_DATASETS_DIR, 'Sitios')

    # Comprobar si existe la carpeta
    if not os.path.exists(parquet_file_path):
        df.write.parquet(parquet_file_path)
    else:
        overwrite = input('La carpeta ya existe, ¿desea sobrescribir? (si o no): ')
        if overwrite.lower() == 'si':
            df.write.parquet(parquet_file_path, mode='overwrite')
        else:
            print('Mueva la carpeta a otro destino o renombrela')
            return  # Salir si no se desea sobrescribir

    # Subir archivos Parquet a Google Cloud Storage
    for file in os.listdir(parquet_file_path):
        local_file_path = os.path.join(parquet_file_path, file)
        print(file)
        # Verificar si el archivo ya existe en Google Cloud Storage
        blob = bucket.blob(os.path.join(REMOTE_DATASETS_DIR, file))
        if blob.exists():
            print(f"El archivo {file} ya existe en Google Cloud Storage. Saltando...")
        else:
            # Subir a Google Cloud Storage
            print(f"Subiendo {file} a Google Cloud Storage...")
            blob.upload_from_filename(local_file_path)
            print(f"Archivo subido exitosamente: gs://{BUCKET_NAME}/{REMOTE_DATASETS_DIR}/{file}")

    print("Todos los archivos Parquet han sido subidos a Google Cloud Storage.")

if __name__ == "__main__":
    convert_and_upload_to_gcs()
    spk.stop()  # Detener la sesión de Spark correctamente