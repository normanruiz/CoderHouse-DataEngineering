from sqlalchemy import create_engine


class ServiciosConexionDB:
    def __init__(self, configuracion=None):
        self._conexion = None
        self._configuracion = configuracion

    @property
    def configuracion(self):
        return self._configuracion

    @configuracion.setter
    def configuracion(self, configuracion):
        self._configuracion = configuracion

    @property
    def conexion(self):
        return self._conexion

    @conexion.setter
    def conexion(self, conexion):
        self._conexion = conexion

    def conectar(self, servicioslog):
        estado = True
        try:
            mensaje = f"Conectando a base de datos {self.configuracion.database}..."
            servicioslog.escribir(mensaje)

            self.conexion = create_engine(f"redshift+psycopg2://{self.configuracion.user}:{self.configuracion.password}@{self.configuracion.host}:{self.configuracion.port}/{self.configuracion.database}")

            mensaje = f"Conexion establecida con base de datos {self.configuracion.database}..."
            servicioslog.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Conectando a base de datos: {type(excepcion)} - {str(excepcion)}"
            servicioslog.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            servicioslog.escribir(mensaje)
        finally:
            return estado

    def desconectar(self, servicioslog):
        estado = True
        try:
            mensaje = f"Cerrando conexion con base de datos {self.configuracion.database}..."
            servicioslog.escribir(mensaje)

            self.conexion.close()

            mensaje = f"Conexion a base de datos {self.configuracion.database} cerrada..."
            servicioslog.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Cerrando conexion a base de datos {self.configuracion.database}: {type(excepcion)} - {str(excepcion)}"
            servicioslog.escribir(mensaje)
        finally:
            return estado

    def ejecutar_insert(self, servicioslog, dataframe):
        estado = True
        try:
            mensaje = f"Insertando datos en base de datos: {self.configuracion.database}..."
            servicioslog.escribir(mensaje)
            dataframe.to_sql("asteroides", self.conexion, if_exists='append', index=False)
            mensaje = f"Datos insertados correctamente..."
            servicioslog.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Insertando datos: {type(excepcion)} - {str(excepcion)}"
            servicioslog.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            servicioslog.escribir(mensaje)
        finally:
            return estado
