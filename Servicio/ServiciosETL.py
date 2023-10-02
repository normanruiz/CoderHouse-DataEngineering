from datetime import date
import pandas as pd
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

            dflvl1 = pd.DataFrame(self.datos_crudos['near_earth_objects'][str(date.today())])
            self.dataframe = dflvl1[['id', 'neo_reference_id', 'name', 'nasa_jpl_url', 'absolute_magnitude_h', 'is_potentially_hazardous_asteroid', 'is_sentry_object']]
            self.dataframe = self.dataframe.astype({'id': 'int32', 'neo_reference_id': 'int32'})
            self.dataframe = self.dataframe.drop_duplicates()

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
            serviciosconexiondb.ejecutar_insert(servicioslog, self.dataframe)

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
