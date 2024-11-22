<div align="right">
  <span><strong>InsightPro Consulting</strong></span>
  <img src="https://github.com/user-attachments/assets/5e2ff93f-31c3-489e-a78a-e233d306bf2f" alt="Logo InsightPro Consulting" width="50">
</div>  

<h1 align="center"><strong>PROYECTO EXPANSIÓN DE MERCADO</strong></h1>



<p align="center">
  <img src="https://github.com/user-attachments/assets/9171bac5-2e2b-4a5c-a7ae-e8c05cea53e1" alt="Expansión de negocio a EE.UU." width="300">
</p>


## **Descripción**  

El objetivo de este proyecto es garantizar que [**Nordsee**](https://github.com/karenb54/Proyecto_Final_Yelp/blob/main/Documentacion%20cliente/Cliente.pdf) se posicione exitosamente en el mercado estadounidense, adaptando su oferta sin perder su identidad.  

A través del análisis de reseñas de **Google Maps** y **Yelp**, complementado con datos poblacionales y económicos de fuentes oficiales, se busca identificar expectativas del mercado en mariscos y comida rápida. Esto permitirá a **Nordsee** desarrollar estrategias basadas en calidad, sostenibilidad y frescura, con un enfoque en estados clave.  

El entregable final incluye un **dashboard interactivo** para visualizar insights y un **modelo de machine learning** que analizará las expectativas de los consumidores, apoyando decisiones estratégicas para la expansión inicial.  

## **Tabla de Contenidos**

- [Instalación y Requisitos](#instalación-y-requisitos)
- [Stack Tecnológico](#stack-tecnológico)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Metodología del Proyecto](#metodología-del-proyecto)
- [KPIs](#kpis)
- [Resultados Obtenidos](#resultados-obtenidos)
- [Recomendaciones](#recomendaciones)
- [Autores](#autores)

---

## **Instalación y Requisitos**

### Pasos para instalar el proyecto:

1. Clonar el repositorio:
   
    ```bash
    git clone https://github.com/karenb54/Proyecto_Final_Yelp.git
    ```

2. Crear un entorno virtual: 

    ```bash
    python -m venv entorno_virtual
    ```

3. Activar el entorno virtual:
     - Windows: 
       ```bash
       entorno_virtual\Scripts\activate 
       ```
     - macOS/Linux: 
       ```bash
       source venv/bin/activate
       ```

4. Instalar las dependencias: 
   
    ```bash
    pip install -r requirements.txt
    ```

5. Instalación de Power BI:
   - Windows: Descargar directamente de la tienda de Microsoft.
   - macOS/Linux: Crear un entorno virtual Windows para realizar la descarga o usar la versión web de Power BI.

---

## Stack Tecnológico

- **ETL**: Realizado con librerías como *Pandas*, *Polars*, *Spark* y *google-cloud* para extraer, transformar y cargar datos.
- **EDA de reseñas**: Uso de *Polars*, *Pandas*, *Plotly*, *TextBlob* y *Pygwalker* para identificar preferencias de los consumidores.
- **EDA de fuentes externas**: Uso de *requests*, *NumPy* y *Seaborn* para analizar datos poblacionales y económicos.
- **Almacenamiento**: *Google Cloud Storage* para centralizar datos de forma segura.
- **Automatización**: Pipeline ETL diseñado con *Google Composer*.
- **Data Warehouse**: Organización eficiente de datos en *Google BigQuery*.
- **Análisis de Sentimiento**: Uso de *Google Cloud Natural Language API*.
- **Visualización**: Dashboards interactivos creados con *Google Data Studio*.

---

## Estructura del Proyecto

- **Notebooks**: Archivos con el código de ETL, EDA y análisis.
- **Datasets**: Readme con imagenes demostrativas de los datos almacenador y organizados en google cloud storage.
- **Ayuda Visual**: Se incluyen todas las imágenes pertinentes para el proyecto.
- **Documentación del cliente**: Contiene un espacio dedicado a la documentación necesaria para contextualizar al cliente.
- **README.md**: Documentación completa del proyecto.
- **requirements.txt**: Requisitos a nivel técnico para ver y modificar el proyecto.

---

## Metodología del Proyecto  

El proceso se desarrolla a través del siguiente pipeline establecido:  

![Pipeline del Proyecto](Notebooks/pipline.png)  

---

### 1. Fuente de Datos  
- **Origen de los datos**:  
  - *Google* y *Yelp*: Bases de datos con información sobre reseñas y comercios.  
  - **APIs externas**:  
    - Economía: *[FRED API](https://api.stlouisfed.org/fred/series/observations)*.  
    - Población: *[Census API](https://api.census.gov/data/{0}/acs/acs5?get=NAME,{1}&for=us:*&key={2})*.  

---

### 2. Carga de Datos  
- **Herramienta**: Script en Python.  
- **Procesos**:  
  - Extracción de datos desde las APIs mencionadas.  
  - Preprocesamiento inicial.  
  - Carga de los datos crudos al *Google Cloud Storage*.  

---

### 3. Datos Crudos  
- **Descripción**:  
  - Carpeta en *Google Cloud Storage* que contiene todos los datasets en su formato original, sin modificaciones.  

---

### 4. Preprocesamiento  
- **Herramienta**: Script en Python.  
- **Procesos**:  
  - Extracción de datos desde la carpeta *Datos Crudos* en *Google Cloud Storage*.  
  - Limpieza inicial, que incluye:  
    - Manejo de valores nulos y duplicados.  
    - Normalización y transformación de campos según los requerimientos del análisis.  
  - Carga de los datos procesados a la carpeta *datos-preprocesados* en *Google Cloud Storage*.  

---

### 5. Datos Preprocesados  
- **Descripción**:  
  - Carpeta en *Google Cloud Storage* que almacena los datos preprocesados.  
  - Utilizados como base para:  
    - Análisis exploratorio (*EDA*) realizado en *Jupyter Notebook*.  
    - Identificación de insights clave.  
    - Selección de datos relevantes para el cliente.  

---

### 6. Limpieza de Datos  
- **Herramienta**: Script en Python.  
- **Procesos**:  
  - Extracción de datos desde la carpeta *Datos Preprocesados* en *Google Cloud Storage*.  
  - Limpieza y filtrado final de la información.  
  - Estructuración de los datos que serán utilizados en producción.  
  - Carga de los datos limpios a la carpeta *datos-limpios* en *Google Cloud Storage*.  

---

### 7. Datos Limpios  
- **Descripción**:  
  - Carpeta en *Google Cloud Storage* que contiene los datos finales listos para ser utilizados en el pipeline de producción.  

---

### 8. Google Cloud Composer  
- **Función**:  
  - Orquestación del pipeline.  
  - Automatización de los scripts mediante *DAGs*, asignando tareas paso a paso en el flujo de trabajo.  

---

### 9. Google BigQuery  
- **Descripción**:  
  - *Data Warehouse* que organiza y almacena la información limpia.  
  - Estructurado con un modelo entidad-relación preestablecido, optimizado para consultas analíticas.  

---

### 10. Power BI  
- **Función**:  
  - Creación de análisis interactivos y dashboards.  
  - Proporciona al cliente información clave para la toma de decisiones.  

---

### 11. Natural Language ML y Looker  
- **Función**:  
  - Implementación de herramientas de Machine Learning para análisis de sentimientos basado en los datos almacenados.  
  - Proporcionan insights avanzados sobre el comportamiento y las preferencias de los consumidores.  

---

### 12. Carga Incremental  
- **Herramienta**: Script en Python.  
- **Función**:  
  - Configuración de un disparador mensual para incorporar nuevos datos de forma incremental al pipeline.  

## Proceso de Desarrollo  

### GOOGLE  
- **ETL Google Maps**  
  [ETL_MAPS.py](https://github.com/karenb54/Proyecto_Final_Yelp/blob/main/Notebooks/ETL_MAPS.py)  
- **EDA Datos Externos**  
  *(Enlace pendiente o no proporcionado)*  
- **README ETL Maps**  
  [README_ETL_MAPS.md](https://github.com/karenb54/Proyecto_Final_Yelp/blob/main/Notebooks/README_ETL_MAPS.md)  

---

### YELP  
- **ETL Yelp**  
  [ETL_YELP.py](https://github.com/karenb54/Proyecto_Final_Yelp/blob/main/Notebooks/ETL_YELP.py)  
- **EDA Datos Internos**  
  [EDA_yelp_Final.ipynb](https://github.com/karenb54/Proyecto_Final_Yelp/blob/main/Notebooks/EDA_yelp_Final.ipynb)  
- **README ETL Yelp**  
  [README_ETL_YELP.md](https://github.com/karenb54/Proyecto_Final_Yelp/blob/main/Notebooks/README_ETL_YELP.md)  

---

### DATOS EXTERNOS  
- **README Datos Externos**  
  [README_DATOS_EXTERNOS.md](https://github.com/karenb54/Proyecto_Final_Yelp/blob/main/Notebooks/README_DATOS_EXTERNOS.md)  
- **ETL/EDA Datos Económicos**  
  [economic-us-data.ipynb](https://github.com/karenb54/Proyecto_Final_Yelp/blob/main/Notebooks/economic-us-data.ipynb)  
- **ETL/EDA Datos Poblacionales**  
  [demographic-data.ipynb](https://github.com/karenb54/Proyecto_Final_Yelp/blob/main/Notebooks/demographic-data.ipynb)  

---  


## KPIs  

### 1. **Porcentaje de Reseñas de Mariscos vs. Total de Reseñas de Restaurantes**  
- **Objetivo**:  
  Determinar la visibilidad y relevancia del mercado de mariscos en EE. UU. en comparación con el mercado general de restaurantes.  
- **Métrica**:  
  Porcentaje de reseñas de restaurantes de mariscos respecto al total de reseñas de restaurantes.  
- **Cálculo**:  
  - **Fórmula**:  
    ```plaintext
    (Cantidad de reseñas de restaurantes de mariscos por mes / Cantidad total de reseñas de restaurantes por mes) × 100
    ```  
- **Frecuencia**: Mensual.  

---

### 2. **Análisis de Sentimiento de Reseñas de Competencia**  
- **Objetivo**:  
  Entender la percepción del cliente sobre la calidad, frescura y sostenibilidad de la oferta de la competencia.  
- **Métrica**:  
  Promedio de puntaje de reseñas positivas (≥4 estrellas) relacionadas con calidad, servicio y sostenibilidad.  
- **Cálculo**:  
  - **Fórmula**:  
    ```plaintext
    (Total de reseñas positivas de la competencia por mes / Total de reseñas de la competencia por mes) × 100
    ```  
- **Frecuencia**: Mensual.  

---

### 3. **Posicionamiento Potencial de Nordsee en Estados Clave**  
- **Objetivo**:  
  Identificar los estados con mayor interés en mariscos, donde Nordsee podría posicionarse favorablemente.  
- **Métrica**:  
  Volumen de reseñas de mariscos en estados clave como indicador del interés de la población en esta categoría.  
- **Cálculo**:  
  - **Fórmula**:  
    ```plaintext
    (Porcentaje de reseñas sobre mariscos en los estados seleccionados por mes / Volumen total de reseñas en cada estado por mes) × 100
    ```  
- **Frecuencia**: Mensual.  

## Resultados Obtenidos
- **Reducción del tamaño de los datos**: Filtrar los usuarios top permitió reducir el conjunto de datos, facilitando un análisis más eficiente.
- **Estandarización de los datos**: El manejo de valores nulos y la expansión de atributos mejoraron la calidad de los datos.
- **Preparación para el Análisis**: El archivo `meta_df.parquet` resultante contiene un conjunto de datos limpio y optimizado, listo para el análisis exploratorio.

---

## Recomendaciones

Basado en los KPIs analizados, se sugieren las siguientes recomendaciones:

1. **Aumentar la visibilidad del mercado de mariscos**: Dado que el porcentaje de reseñas de mariscos es bajo en comparación con el total de reseñas, se recomienda implementar campañas de marketing que destaquen la oferta única de Nordsee y su compromiso con la sostenibilidad.

2. **Mejorar la calidad y frescura de los productos**: Los análisis de sentimiento indican que la calidad y frescura son aspectos cruciales para los consumidores. Nordsee debería enfocar sus esfuerzos en garantizar la frescura de los productos y mejorar la percepción de calidad a través de pruebas de degustación y promociones.

3. **Seleccionar estados estratégicos para la expansión**: Basándose en el volumen de reseñas de mariscos y el interés del mercado, se sugiere priorizar la expansión en estados como California y Florida, donde la demanda de mariscos es más alta.

4. **Monitorear y adaptar la oferta según las reseñas**: Establecer un sistema para monitorear las reseñas de los clientes en tiempo real permitirá a Nordsee adaptar su menú y servicio de acuerdo a las expectativas y preferencias cambiantes de los consumidores.

5. **Fomentar la lealtad del cliente**: Implementar programas de fidelización o recompensas para clientes frecuentes podría aumentar la tasa de retorno y la frecuencia de compra, mejorando así la tasa de crecimiento de ventas comparables.

---

## Conclusión

Este proceso de limpieza asegura que los datos estén en las mejores condiciones para el análisis, reduciendo el ruido y enfocándose en la información más relevante. Esto permite realizar análisis precisos y extraer insights valiosos para el negocio.

---

## Autores

✦ Este proyecto fue realizado por **Karen Barbosa**, **Matías Oviedo**, **Fabián Gutiérrez**, **Julia Catalina Gastellu** y **Hugo Zaquelli**.

