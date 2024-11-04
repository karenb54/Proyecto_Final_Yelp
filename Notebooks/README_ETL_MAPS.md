# Proceso de Carga, Limpieza y Análisis de Datos de Locales en EE.UU.

Este script tiene como objetivo cargar, limpiar y analizar datos de locales en EE.UU., utilizando archivos en formato JSON y Parquet. La información final es almacenada en formato Parquet y está optimizada para su análisis posterior. Este proyecto está diseñado para una cadena de restaurantes europea que desea expandirse en el mercado estadounidense, centrándose en estados específicos y categorías de locales relevantes.

## Estructura del Código

El script se divide en los siguientes pasos:

### 1. Configuración de Autenticación y Conexión con Google Cloud
La autenticación para Google Cloud se configura al inicio del script, permitiendo el acceso a los archivos almacenados en Google Cloud Storage (GCS) a través de la librería `gcsfs`. Esto es necesario para cargar archivos desde GCS y evitar errores de permisos.

- **Librerías utilizadas**: `gcsfs`, `polars`
- **Archivo de autenticación**: `credentials.json`

### 2. Carga de Archivos Parquet en Polars
Los archivos en formato Parquet se cargan en `Polars`, una librería rápida para el análisis de datos. Se concatenan múltiples archivos, ya que los datos pueden estar divididos en varios archivos Parquet.

- **Función**: `read_parquet_files`
- **Propósito**: Permitir la carga eficiente de archivos Parquet y concatenarlos en un solo DataFrame.
- **Salida**: `pl_df`, un DataFrame de Polars con todos los datos de locales.

### 3. Carga y Limpieza de Archivos JSON en Spark
Para manejar grandes volúmenes de datos JSON, el script utiliza Spark para cargar, procesar y limpiar los datos. Los archivos JSON son cargados en un DataFrame de Spark y luego se seleccionan las columnas necesarias para el análisis.

- **Columnas seleccionadas**: `avg_rating`, `category`, `gmap_id`, `name`, `num_of_reviews`, `address`
- **Propósito**: Reducir el volumen de datos a las columnas de interés y optimizar el procesamiento.

### 4. Limpieza de Datos
En esta sección se realiza una limpieza exhaustiva de los datos, eliminando duplicados y registros incompletos:

- **Extracción de Estados**: Los estados se extraen de la dirección del local y se limpian para asegurar uniformidad.
- **Eliminación de Duplicados**: Se eliminan registros duplicados basados en el campo `gmap_id`, conservando solo valores únicos.
- **Filtrado de Valores Nulos**: Se filtran registros con valores nulos en `estado` y `category`, manteniendo solo aquellos con información completa.
- **Filtrado por Estados de EE.UU.**: Para mantener la relevancia, solo se conservan los estados de EE.UU. (representados por códigos de dos letras).

### 5. Análisis y Agrupación de Datos
Se realiza una agrupación de los datos en Polars para contar la cantidad total de reseñas y el recuento de identificadores únicos (`gmap_id`) por categoría. Esto permite analizar la cantidad de reseñas y locales por categoría de local, facilitando el análisis de popularidad en distintas categorías.

- **Propósito**: Obtener un panorama de las categorías de locales más populares en términos de reseñas.

### 6. Guardado de Resultados en Formato Parquet
Finalmente, el DataFrame limpio y procesado se guarda en formato Parquet, optimizado para almacenamiento y consultas rápidas.

- **Ruta de almacenamiento**: `../data/GoogleMaps/sitiosfiltrado.parquet`

### Mensajes de Éxito y Control de Errores
El código incluye mensajes de confirmación para cada tarea realizada y manejo de errores. Esto permite seguir el flujo de ejecución y detectar cualquier problema en el proceso de carga o procesamiento.

## Dependencias

- **Polars**: `pip install polars`
- **Pygwalker**: `pip install pygwalker`
- **Google Cloud Storage (gcsfs)**: `pip install gcsfs`
- **Pyspark**: `pip install pyspark`

## Resultados Obtenidos
El archivo resultante en formato Parquet contiene locales únicos con información limpia y completa, listos para el análisis de categorías y estados. Este proceso facilita la detección de patrones y preferencias de los clientes en el mercado estadounidense, apoyando la toma de decisiones estratégicas para la expansión de la cadena de restaurantes.

Este proceso de ETL está optimizado para manejar grandes volúmenes de datos, garantizando que la información final esté lista para su análisis en estudios de mercado detallados.
