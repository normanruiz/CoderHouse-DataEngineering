# CoderHouse - Data Engineering

## Entregable 01

### Objetivos generales
- Tener un código inicial que será usado en el proyecto final como un script ETL inicial.

### Objetivos específicos
- El script debería extraer datos en JSON y poder leer el formato en un diccionario de Python.
- La entrega involucra la creación de una versión inicial de la tabla donde los datos serán cargados posteriormente.

### Formato
- Código en Python subido ya sea en repositorio de GitHub o en Google Drive.
- Tabla creada en Redshift.

### Sugerencias
- Consultar la documentación del módulo requests en Python.
- Se sugiere ampliamente la creatividad del estudiante. Usar Apis que les resulten interesantes y están relacionadas a su contexto.
- Revisar el instrumento de evaluación

## Entregable 02

### Objetivos generales
- El script de la entrega 1 deberá adaptar datos leídos de la API y cargarlos en la tabla creada en la pre-entrega anterior en Redshift.

### Objetivos específicos
- Implementar funcionalidades de la librería Pandas en el código cargándolos en la tabla creada en la misma.
- Solucionar una situación real de ETL donde puedan llegar a aparecer duplicados durante la ingesta de los datos.

### Formato
- Código en Python subido ya sea en repositorio de GitHub o en Google Drive.
- Tabla creada en Redshift con los datos de muestra que hayan sido cargados mediante el script.

### Sugerencias
- Consultar la documentación oficial de Pandas; profundizar en su uso.
- Revisar el instrumento de evaluación

## Entregable 3

### Objetivos generales
- El script de la 2da entrega debe correr en un container de Docker y estará embebido en un DAG de Airﬂow dentro del container.

### Objetivos especíﬁcos
- El container debe ser lo más liviano posible como para que el script funcione sin problemas. Cualquier usuario podría correr el container y que el script esté listo para su ejecución.

### Formato
- Dockerﬁle y código con todo lo necesario para correr (si es necesario incluir un manual de instrucciones o pasos para correrlo), subido en repositorio de Github o en Google Drive.

### Sugerencias
- La base de datos donde estará esta tabla no hace falta que viva en el container, sino que se tiene en cuenta que es un Redshift en la nube.
- Investigar sobre Docker Compose para facilitar la tarea.
- Revisar el instrumento de evaluación

## Ejecucion del script
Para la correcta ejecucion se requieren las sigueintes importaqciones:
- DATE
- OS
- REQUESTS
- XMLTODICT
- TIME
- Pandas
- Sqlalchemy
- Sqlalchemy-Redshift
- Redshift_connector
- Psycopg2

Dentro de la raiz del proyecto ejecutar como root:
~~~
python3 app.py
~~~

## Detalle de la API

Pagina Oficial: [NASA APIs](https://api.nasa.gov/)

Asteroids - NeoWs

NeoWs (Near Earth Object Web Service) es un servicio web RESTful para información de asteroides cercanos a la Tierra. Con NeoWs, un usuario puede: buscar asteroides según su fecha de aproximación más cercana a la Tierra, buscar un asteroide específico con su identificación de cuerpo pequeño JPL de la NASA y explorar el conjunto de datos general.

Conjunto de datos: Todos los datos provienen del equipo de asteroides JPL de la NASA (http://neo.jpl.nasa.gov/).


