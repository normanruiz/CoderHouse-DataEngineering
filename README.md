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

## Ejecucion del script
Para la correcta ejecucion se requieren las sigueintes importaqciones:
- DATE
- OS
- REQUESTS
- XMLTODICT
- TIME

Dentro de la raiz del proyecto ejecutar como root:
~~~
python3 app.py
~~~

## Detalle de la API

Pagina Oficial: [NASA APIs](https://api.nasa.gov/)

Asteroids - NeoWs

NeoWs (Near Earth Object Web Service) es un servicio web RESTful para información de asteroides cercanos a la Tierra. Con NeoWs, un usuario puede: buscar asteroides según su fecha de aproximación más cercana a la Tierra, buscar un asteroide específico con su identificación de cuerpo pequeño JPL de la NASA y explorar el conjunto de datos general.

Conjunto de datos: Todos los datos provienen del equipo de asteroides JPL de la NASA (http://neo.jpl.nasa.gov/).


