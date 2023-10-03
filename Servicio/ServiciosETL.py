from datetime import date
import json
import pandas as pd
from pandas import json_normalize
from Servicio.ServiciosConexionApi import ServiciosConexionApi
from Servicio.ServiciosConexionDB import ServiciosConexionDB


class ServiciosETL:
    def __init__(self):
        self._datos_crudos = {}
        self._dataframe = None

    @property
    def datos_crudos(self):
        return self._datos_crudos

    @datos_crudos.setter
    def datos_crudos(self, datos_crudos):
        self._datos_crudos = datos_crudos

    @property
    def dataframe(self):
        return self._dataframe

    @dataframe.setter
    def dataframe(self, dataframe):
        self._dataframe = dataframe

    def extract(self, servicioslog, api):
        estado = True
        try:
            mensaje = f"Extrayendo datos desde origen..."
            servicioslog.escribir(mensaje)

            serviciosconexionapi = ServiciosConexionApi(api)
            estado, self.datos_crudos = serviciosconexionapi.consultar(servicioslog)
            if estado is False:
                return

            mensaje = f"Registros recuperados: {str(self.datos_crudos['element_count'])}"
            servicioslog.escribir(mensaje)

            mensaje = f"Subproceso finalizado..."
            servicioslog.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Extrayendo datos desde origen: {type(excepcion)} - {str(excepcion)}"
            servicioslog.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            servicioslog.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            servicioslog.escribir(mensaje, tiempo=False)
            return estado

    def transform(self, servicioslog):
        estado = True
        try:
            mensaje = f"Transformando datos..."
            servicioslog.escribir(mensaje)

            df = json_normalize(
                self.datos_crudos['near_earth_objects'][str(date.today())],
                'close_approach_data',
                [['links', 'self'],
                'id',
                'neo_reference_id',
                'name',
                'nasa_jpl_url',
                'absolute_magnitude_h',
                ['estimated_diameter', 'kilometers', 'estimated_diameter_min'],
                ['estimated_diameter', 'kilometers', 'estimated_diameter_max'],
                ['estimated_diameter', 'meters', 'estimated_diameter_min'],
                ['estimated_diameter', 'meters', 'estimated_diameter_max'],
                ['estimated_diameter', 'miles', 'estimated_diameter_min'],
                ['estimated_diameter', 'miles', 'estimated_diameter_max'],
                ['estimated_diameter', 'feet', 'estimated_diameter_min'],
                ['estimated_diameter', 'feet', 'estimated_diameter_max'],
                'is_potentially_hazardous_asteroid',
                'is_sentry_object'],
                max_level=3
                )
            df = df.rename(columns={
                'links.self': 'links',
                'estimated_diameter.kilometers.estimated_diameter_min': 'estimated_diameter_kilometers_min',
                'estimated_diameter.kilometers.estimated_diameter_max': 'estimated_diameter_kilometers_max',
                'estimated_diameter.meters.estimated_diameter_min': 'estimated_diameter_meters_min',
                'estimated_diameter.meters.estimated_diameter_max': 'estimated_diameter_meters_max',
                'estimated_diameter.miles.estimated_diameter_min': 'estimated_diameter_miles_min',
                'estimated_diameter.miles.estimated_diameter_max': 'estimated_diameter_miles_max',
                'estimated_diameter.feet.estimated_diameter_min': 'estimated_diameter_feet_min',
                'estimated_diameter.feet.estimated_diameter_max': 'estimated_diameter_feet_max',
                'relative_velocity.kilometers_per_second': 'relative_velocity_kilometers_per_second',
                'relative_velocity.kilometers_per_hour': 'relative_velocity_kilometers_per_hour',
                'relative_velocity.miles_per_hour': 'relative_velocity_miles_per_hour',
                'miss_distance.astronomical': 'miss_distance_astronomical',
                'miss_distance.lunar': 'miss_distance_lunar',
                'miss_distance.kilometers': 'miss_distance_kilometers',
                'miss_distance.miles': 'miss_distance_miles'
            })
            df = df.astype({
                'id': 'int32',
                'neo_reference_id': 'int32',
                'absolute_magnitude_h': 'float',
                'estimated_diameter_kilometers_min': 'float',
                'estimated_diameter_kilometers_max': 'float',
                'estimated_diameter_meters_min': 'float',
                'estimated_diameter_meters_max': 'float',
                'estimated_diameter_miles_min': 'float',
                'estimated_diameter_miles_max': 'float',
                'estimated_diameter_feet_min': 'float',
                'estimated_diameter_feet_max': 'float',
                'is_potentially_hazardous_asteroid': 'bool',
                'epoch_date_close_approach': 'int64',
                'relative_velocity_kilometers_per_second': 'float',
                'relative_velocity_kilometers_per_hour': 'float',
                'relative_velocity_miles_per_hour': 'float',
                'miss_distance_astronomical': 'float',
                'miss_distance_lunar': 'float',
                'miss_distance_kilometers': 'float',
                'miss_distance_miles': 'float',
                'is_sentry_object': 'bool',
            })
            df['close_approach_date'] = pd.to_datetime(df['close_approach_date'])
            df['close_approach_date_full'] = pd.to_datetime(df['close_approach_date_full'])
            self.dataframe = df.drop_duplicates()

            mensaje = f"Subproceso finalizado..."
            servicioslog.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Transformando datos: {type(excepcion)} - {str(excepcion)}"
            servicioslog.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            servicioslog.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            servicioslog.escribir(mensaje, tiempo=False)
            return estado

    def load(self, servicioslog, conexion):
        estado = True
        try:
            mensaje = f"Cargando datos..."
            servicioslog.escribir(mensaje)

            serviciosconexiondb = ServiciosConexionDB(conexion)
            serviciosconexiondb.conectar(servicioslog)
            serviciosconexiondb.ejecutar_insert_update(servicioslog, self.dataframe)

            mensaje = f"Subproceso finalizado..."
            servicioslog.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Cargando datos: {type(excepcion)} - {str(excepcion)}"
            servicioslog.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            servicioslog.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            servicioslog.escribir(mensaje, tiempo=False)
            return estado
