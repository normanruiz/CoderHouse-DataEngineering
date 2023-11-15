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

## Entregable 4

### Objetivos generales
- Partiendo del último entregable, el script ya debería funcionar correctamente dentro de Airflow en un contenedor Docker. En este entregable, añadiremos alertas en base a thresholds de los valores que estemos analizando.

### Objetivos específicos
- Incorporar código que envíe alertas mediante SMTP.
- Incorporar una forma fácil de configurar thresholds que van a ser analizados para el envío de alertas.

### Formato
- Dockerfile y código con todo lo necesario para correr (si es necesario incluir un manual de instrucciones o pasos para correrlo), subido en repositorio de Github o en Google Drive.
- Proporcionar screenshot de un ejemplo de un correo envíado habiendo utilizado el código.

### Sugerencias
- La base de datos donde estará esta tabla no hace falta que viva en el container, sino que se tiene en cuenta que es un Redshift en la nube.
- Investigar sobre Docker Compose para facilitar la tarea.
- NO añadan ningún tipo de credencial al código. Usen variables de entorno.
- Revisar la rúbrica

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

## Ecosistema Con Docker

El ecosistema fue desarrollado probado en Debian 12.

Antes de echar a andar todo debemos ejecutar el siguiente comando: 

~~~
sudo chmod 777 /var/run/docker.sock
~~~

### Generacion de contenedor asteriodes-etl

Una vez dentro de la carpeta del proyecto ejecutaremos:

~~~
cd asteroides-etl
docker build -t asteroides-etl .
~~~

### Airflow

Ubicado en la raiz del proyecto ejecutar:

~~~
cd airflow
docker compose up 
~~~

*Para acceder al portal dirijase a http://localhost:8080/ en su navegador preferido y registrese con las siguientes credenciales: usr: airflow pwd: airflow*

## Envio de alertas

Para el envio de alertas se deberan realizar dos configuraciones adicionales

### Conexion a Redshift en la UI

En el menu principal nos dirigimos a Admin - Conecciones 

![image](https://github.com/normanruiz/CoderHouse-DataEngineering/assets/28979800/01b31a8f-3dfb-4384-8f94-ce45ca369d0d)

Le damos click al boton "+", que nos mostrara un formulario de carga, en este cargamos los datos requeridos y guardamos.

### Conexion a Servidor de SMTP

Se debe agregar en el docker-compose.yaml en la seccion environment de x-airflow-common despues de la linea AIRFLOW__CORE__ENABLE_XCOM_PICKLING el siguiente bloque de configuraciones:

~~~
    AIRFLOW__SMTP__SMTP_HOST: ''
    AIRFLOW__SMTP__SMTP_USER: ''
    AIRFLOW__SMTP__SMTP_PASSWORD: ''
    AIRFLOW__SMTP__SMTP_PORT: 
    AIRFLOW__SMTP__SMTP_MAIL_FROM: ''
~~~

Carque los datos de su proveedor de correo y guarde.

Una ves realizadas estas configuraciones procederemos a reiniciar el ambiente con los siguientes comandos, dentro de la carpera airflow del proyecto:

~~~
docker compose down
docker compose up
~~~

