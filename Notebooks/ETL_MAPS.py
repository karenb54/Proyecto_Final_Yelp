import polars as pl
import pygwalker as pyg
from google.oauth2.service_account import Credentials
from google.cloud import storage
import gcsfs
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, substring_index, trim
import pyspark.sql.functions as F
import glob
import time

#configuración de la autenticación para Google Cloud
try:
    fs = gcsfs.GCSFileSystem(token="../Auth/credentials.json")
    print("Autenticación configurada con éxito.")
except Exception as e:
    print(f"Error en la configuración de la autenticación: {e}")

#ruta al archivo Parquet
path = 'gs://bucket-proyecto-final-1/datos-limpios/dataset_google_sitios/*.parquet'

#función para cargar múltiples archivos Parquet en un DataFrame de Polars
def read_parquet_files(path):
    try:
        files = fs.glob(path)
        frames = [pl.read_parquet(fs.open(file)) for file in files]
        print("Archivos Parquet cargados correctamente.")
        return pl.concat(frames)
    except Exception as e:
        print(f"Error al leer archivos Parquet: {e}")
        return None

#cargar datos en DataFrame de Polars
pl_df = read_parquet_files(path)

if pl_df is not None:
    #explode para categorías y agrupar por 'category'
    pl_df = pl_df.explode('category')
    df_grouped = pl_df.group_by("category").agg([
        pl.col("num_of_reviews").sum().alias("total_reviews"),
        pl.col("gmap_id").n_unique().alias("unique_gmap_id_count")
    ]).sort('total_reviews', descending=True)
    print("Agrupación y análisis en Polars completado.")

    #visualización en Pygwalker
    vis_spec = r"""{"config":[{"config":{"defaultAggregated":true,"geoms":["auto"],"coordSystem":"generic","limit":10,"timezoneDisplayOffset":0,"folds":["total_reviews"]},"encodings":{"dimensions":[{"fid":"category","name":"category","basename":"category","semanticType":"nominal","analyticType":"dimension","offset":0},{"fid":"gw_mea_key_fid","name":"Measure names","analyticType":"dimension","semanticType":"nominal"}],"measures":[{"fid":"total_reviews","name":"total_reviews","basename":"total_reviews","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"unique_gmap_id_count","name":"gmap_id_count","basename":"unique_gmap_id_count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}},{"fid":"gw_mea_val_fid","name":"Measure values","analyticType":"measure","semanticType":"quantitative","aggName":"sum"}],"rows":[{"fid":"category","name":"category","basename":"category","semanticType":"nominal","analyticType":"dimension","offset":0,"sort":"descending"}],"columns":[{"fid":"total_reviews","name":"total_reviews","basename":"total_reviews","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0}],"color":[{"fid":"unique_gmap_id_count","name":"gmap_id_count","basename":"unique_gmap_id_count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","offset":0}],"opacity":[],"size":[],"shape":[],"radius":[],"theta":[],"longitude":[],"latitude":[],"geoId":[],"details":[],"filters":[],"text":[]},"layout":{"showActions":false,"showTableSummary":false,"stack":"stack","interactiveScale":false,"zeroScale":true,"size":{"mode":"fixed","width":800,"height":600},"format":{},"geoKey":"name","resolve":{"x":false,"y":false,"color":false,"opacity":false,"shape":false,"size":false}},"visId":"gw_OjTs","name":"Chart 1"}],"chart_map":{},"workflow_list":[{"workflow":[{"type":"view","query":[{"op":"aggregate","groupBy":["category"],"measures":[{"field":"total_reviews","agg":"sum","asFieldKey":"total_reviews_sum"},{"field":"unique_gmap_id_count","agg":"sum","asFieldKey":"unique_gmap_id_count_sum"}]}]},{"type":"sort","by":["total_reviews_sum","unique_gmap_id_count_sum"],"sort":"descending"}],"limit":10}],"version":"0.4.9.10"}"""
    pyg.walk(df_grouped, spec=vis_spec)
else:
    print("No se cargaron archivos Parquet para análisis en Polars.")

#configurar la sesión de Spark
try:
    spk = SparkSession.builder.appName('EDA Locales').getOrCreate()
    print("Sesión de Spark iniciada correctamente.")
except Exception as e:
    print(f"Error al iniciar la sesión de Spark: {e}")

#leer archivos JSON en DataFrame de Spark
try:
    file_paths = glob.glob('../data/GoogleMaps/metadata-sitios/**/*.json', recursive=True)
    start_time = time.time()
    df = spk.read.json(file_paths)
    end_time = time.time()
    print(f"Archivos JSON cargados en Spark. Tiempo de carga: {end_time - start_time:.2f} segundos.")
except Exception as e:
    print(f"Error al cargar archivos JSON: {e}")

#selección y limpieza de columnas
columns = ['avg_rating', 'category', 'gmap_id', 'name', 'num_of_reviews', 'address']
df_eda = df.select(*columns)
df_eda = df_eda.withColumn('estados', substring_index(col('address'), ',', -1))
df_eda = df_eda.withColumn('estado', trim(substring_index(col('estados'), ' ', 2))).drop('estados')

#detectar y eliminar duplicados
total_count = df_eda.count()
distinct_count = df_eda.dropDuplicates(["gmap_id"]).count()
duplicates_count = total_count - distinct_count
df_sin_duplicados = df_eda.dropDuplicates(["gmap_id"])

print(f"Registros iniciales en gmap_id: {total_count}")
print(f"Número de duplicados en gmap_id: {duplicates_count}")
print(f"Número de registros únicos en gmap_id: {df_sin_duplicados.count()}")

#filtrar registros con estado no nulo y categoría no nula
df_sin_duplicados = df_sin_duplicados.filter(df_sin_duplicados["estado"].isNotNull() & df_sin_duplicados["category"].isNotNull())

#filtrar registros donde el estado tiene solo 2 caracteres
df_filtrado = df_sin_duplicados.filter(F.length(df_sin_duplicados["estado"]) == 2)

#filtrar por estados de EE.UU.
estados_eeuu = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", 
                "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", 
                "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

df_filtrado = df_filtrado.filter(df_filtrado['estado'].isin(estados_eeuu))
print(f"Número de registros después del filtrado de estados: {df_filtrado.count()}")

#guardar el DataFrame filtrado en formato Parquet
output_path = "../data/GoogleMaps/sitiosfiltrado.parquet"
try:
    df_filtrado.write.parquet(output_path)
    print("Archivo Parquet guardado exitosamente en la ruta especificada.")
except Exception as e:
    print(f"Error al guardar el archivo Parquet: {e}")

#finalizar sesión de Spark
spk.stop()
print("Sesión de Spark finalizada.")
