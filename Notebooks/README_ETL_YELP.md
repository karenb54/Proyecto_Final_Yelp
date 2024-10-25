# Proceso de Limpieza de Datos (ETL)
Este archivo **ETL.py** contiene el código para el proceso de limpieza de datos utilizado en el proyecto de análisis de reseñas de negocios. La limpieza de datos es esencial para mejorar la calidad y precisión del análisis, asegurando que los datos estén en un formato adecuado para su uso. A continuación, se detallan los pasos realizados y sus justificaciones.

### Pasos del Proceso de Limpieza
1. Carga de Datos
Se cargan los datos desde dos fuentes principales:

review.json: Contiene las reseñas de los usuarios.
business.pkl: Incluye la información de los negocios.
Usamos pd.read_json para cargar el archivo de reseñas en formato JSON y pd.read_pickle para cargar los negocios desde un archivo Pickle. Esto permite manejar grandes volúmenes de datos manteniendo la eficiencia.

2. Manejo de Valores Nulos
Se aplican diferentes estrategias para manejar los valores nulos:

Eliminación de filas y columnas vacías: Si una fila o columna contiene únicamente valores nulos, se elimina para reducir el ruido en los datos.

Umbral del 70%: Si más del 70% de los datos en una columna son nulos, se elimina la columna para evitar incluir datos incompletos.

### Relleno de valores nulos

Para columnas numéricas, se rellenan con la media de la columna.
Para columnas categóricas o de texto, se utiliza el valor 'valor incompleto' para indicar que la información no está disponible.
Estas decisiones ayudan a preservar la mayor cantidad de datos posible mientras se mejora su calidad.

3. Eliminación de Columnas Duplicadas
Se eliminan las columnas duplicadas del DataFrame df_business. Este paso es fundamental para evitar inconsistencias y redundancias que podrían afectar el análisis. La eliminación se realiza seleccionando las columnas que no estén duplicadas.

4. Conversión de Formato en Atributos
La columna attributes, que contiene información en formato de diccionario, se convierte en un formato estándar (string). Esto es necesario para expandir los atributos en columnas separadas en pasos posteriores.

5. Procesamiento por Chunks
Para procesar archivos grandes de manera eficiente, se usa un enfoque de procesamiento por chunks con un tamaño de 100,000 filas por chunk. Este enfoque ayuda a evitar problemas de memoria y permite realizar operaciones de agregación sobre datos muy grandes.

6. Agrupación y Cálculo de Métricas
Se agrupan los datos por user_id para calcular dos métricas:

Cantidad de reseñas (review_id).
Suma de la utilidad (useful).
Se define un estado top o regular para los usuarios en función de los cuartiles de estas métricas. Los usuarios en el cuartil superior (75%) se etiquetan como top.

7. Filtrado de Datos
Se filtran las reseñas y negocios para incluir solo aquellos relacionados con usuarios top. Este paso reduce el tamaño del conjunto de datos y se enfoca en los usuarios más relevantes para el análisis.

8. Manejo de Categorías y Atributos
Se manejan las categorías en df_business para separar múltiples categorías en diferentes filas y se limpian los atributos, expandiéndolos en columnas separadas. Este paso permite realizar un análisis más granular de los servicios y características de los negocios.

9. Exportación del DataFrame Combinado
Finalmente, los datos limpios se exportan a un archivo meta_df.parquet. Este formato se eligió por su capacidad de compresión y rápida lectura/escritura, lo que lo hace ideal para grandes volúmenes de datos.

### Resultados Obtenidos
Reducción del tamaño de los datos: Filtrar los usuarios top permitió reducir el conjunto de datos, facilitando un análisis más eficiente.
Estandarización de los datos: El manejo de valores nulos y la expansión de atributos mejoraron la calidad de los datos.
Preparación para el Análisis: El archivo meta_df.parquet resultante contiene un conjunto de datos limpio y optimizado, listo para el análisis exploratorio.
Conclusión
Este proceso de limpieza asegura que los datos estén en las mejores condiciones para el análisis, reduciendo el ruido y enfocándose en la información más relevante. Esto permite realizar análisis precisos y extraer insights valiosos para el negocio.