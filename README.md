<h1 align="center"><strong>PROYECTO EXPANSIÓN DE MERCADO</strong></h1>

<p align="center">
  ![Logo de InsightPro Consulting](path/to/logo.png) <!-- Reemplaza con la ruta del logo -->
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/42ea0531-a046-4082-b38f-80e370fd0a05" alt="Diferencias entre privacidad y protección de datos en EE.UU. y Europa" />
</p>

## Descripción

Este proyecto tiene como objetivo asegurar que Nordsee se posicione exitosamente en EE. UU., adaptando su oferta sin perder su identidad y alcanzando una mayor penetración en los segmentos clave. Utilizando datos de reseñas de consumidores obtenidos a través de las APIs de Google Maps y Yelp, identificamos las expectativas y preferencias en el mercado de mariscos, así como oportunidades y desafíos para la marca en su expansión.

Actualmente, en el primer sprint del proyecto, nos estamos enfocando en la creación de un ETL y un análisis exploratorio de datos (EDA). Este análisis inicial le proporcionará a Nordsee una visión detallada sobre la competencia y ayudará a determinar los estados donde la marca podría establecerse en un inicio, considerando tanto el análisis de la competencia como los gustos de la población a través de las reseñas.

---

## Tabla de Contenidos

- [Instalación y Requisitos](#instalación-y-requisitos)
- [Stack Tecnológico](#stack-tecnológico)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Metodología del Proyecto](#metodología-del-proyecto)
- [Datos y Fuentes](#datos-y-fuentes)
- [Resultados](#resultados)

---

## Instalación y Requisitos

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

- **ETL**: Realizado en Visual Studio Code y Jupyter Notebook, utilizando librerías de Python como Spark y Pandas para la extracción, transformación y carga de los datos de reseñas.

- **EDA (Análisis Exploratorio de Datos)**: Desarrollado en Visual Studio Code y Jupyter Notebook, con el uso de librerías como *Polars*, *Pandas*, *NumPy*, *Pygwalker*, *Plotly* y *TextBlob* para un análisis detallado de la competencia y las preferencias de los consumidores.

- **Presentación**: Las visualizaciones y la presentación del proyecto se realizaron en Canva, facilitando la comunicación de los hallazgos clave.

- **Almacenamiento**: Google Cloud Storage se utilizó para almacenar los datos obtenidos de las APIs, garantizando seguridad y fácil acceso.

- **Data Warehouse**: Google BigQuery se implementará para organizar y consultar los datos de manera eficiente, escalando con el crecimiento del dataset.

- **Machine Learning**: Google Cloud Natural Language API y Google Recommendation se usarán para analizar el sentimiento en las reseñas y recomendar estrategias de acuerdo con las preferencias del cliente.

- **Visualización**: Se utilizará Google Data Studio para crear dashboards interactivos y comunicar métricas clave de rendimiento.

- **Despliegue**: Looker Studio se empleará para el despliegue final de las visualizaciones, permitiendo al cliente acceder a los insights en tiempo real.

---

## Estructura del Proyecto

- **Notebooks**: Archivos que contienen el código usado en cada paso del proceso.
- **Datasets**: Archivos utilizados para visualizar y analizar los datos, divididos en datos de Google y de Yelp.
- **Ayuda Visual**: Se incluyen todas las imágenes pertinentes para el proyecto.
- **Documentación del cliente**: Contiene un espacio dedicado a la documentación necesaria para contextualizar al cliente.
- **README.md**: Documentación completa del proyecto.
- **requirements.txt**: Requisitos a nivel técnico para ver y modificar el proyecto.

---

## Metodología del Proyecto

### Herramientas Utilizadas

### Proceso de Desarrollo

Ver el README de la carpeta Notebooks: [Notebooks](https://github.com/karenb54/Proyecto_Final_Yelp/tree/main/Notebooks)

---

## KPIs

### 1. KPI 1: Porcentaje de Reseñas de Mariscos vs. Total de Reseñas de Restaurantes
- **Objetivo**: Determinar la visibilidad y relevancia del mercado de mariscos en EE. UU. en comparación con el mercado general de restaurantes.
- **Métrica**: Porcentaje de reseñas de restaurantes de mariscos respecto al total de reseñas de restaurantes.
- **Cálculo**: 
  - Fórmula: 
  ```plaintext
  (Cantidad de reseñas de restaurantes de mariscos / Cantidad total de reseñas de restaurantes) × 100

---

### 2. KPI 2: Análisis de Sentimiento de Reseñas de Competencia
- **Objetivo**: Entender la percepción del cliente sobre la calidad, frescura y sostenibilidad de la oferta de la competencia.
- **Métrica**: Promedio de puntaje de reseñas positivas (≥4 estrellas) en temas de calidad, servicio y sostenibilidad.
- **Cálculo**:
  - Fórmula:
  ```plaintext
  (Total de reseñas positivas / Total de reseñas de la competencia) × 100

---

### 3. KPI 3: Posicionamiento Potencial de Nordsee en Estados Clave
- **Objetivo**: Identificar los estados con mayor interés en mariscos donde Nordsee podría posicionarse favorablemente.
- **Métrica**: Volumen de reseñas de mariscos en estados clave como indicador de interés de la población en esta categoría.
- **Cálculo**:
  - Fórmula:
  ```plaintext
  (Porcentaje de reseñas positivas en los estados seleccionados / Volumen total de reseñas en cada estado) × 100

---

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

