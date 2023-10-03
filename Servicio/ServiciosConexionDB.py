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

    def ejecutar_insert_update(self, servicioslog, dataframe):
        estado = True
        try:
            mensaje = f"Insertando y actualizando datos en base de datos: {self.configuracion.database}..."
            servicioslog.escribir(mensaje)
            dataframe.to_sql("staging", self.conexion, if_exists='replace', index=False)
            self.conexion.execute(f"DELETE FROM norman_ruiz_coderhouse.asteroides USING norman_ruiz_coderhouse.staging WHERE asteroides.id = staging.id")
            self.conexion.execute(f"INSERT INTO norman_ruiz_coderhouse.asteroides (links, id, neo_reference_id, name, nasa_jpl_url, absolute_magnitude_h, estimated_diameter_kilometers_min, estimated_diameter_kilometers_max, estimated_diameter_meters_min, estimated_diameter_meters_max, estimated_diameter_miles_min, estimated_diameter_miles_max, estimated_diameter_feet_min, estimated_diameter_feet_max, is_potentially_hazardous_asteroid, close_approach_date, close_approach_date_full, epoch_date_close_approach, relative_velocity_kilometers_per_second, relative_velocity_kilometers_per_hour, relative_velocity_miles_per_hour, miss_distance_astronomical, miss_distance_lunar, miss_distance_kilometers, miss_distance_miles, orbiting_body, is_sentry_object) SELECT links, id, neo_reference_id, name, nasa_jpl_url, absolute_magnitude_h, estimated_diameter_kilometers_min, estimated_diameter_kilometers_max, estimated_diameter_meters_min, estimated_diameter_meters_max, estimated_diameter_miles_min, estimated_diameter_miles_max, estimated_diameter_feet_min, estimated_diameter_feet_max, is_potentially_hazardous_asteroid, close_approach_date, close_approach_date_full, epoch_date_close_approach, relative_velocity_kilometers_per_second, relative_velocity_kilometers_per_hour, relative_velocity_miles_per_hour, miss_distance_astronomical, miss_distance_lunar, miss_distance_kilometers, miss_distance_miles, orbiting_body, is_sentry_object FROM norman_ruiz_coderhouse.staging;")
            mensaje = f"Datos insertados y actualizados correctamente..."
            servicioslog.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Insertando y actualizando datos: {type(excepcion)} - {str(excepcion)}"
            servicioslog.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            servicioslog.escribir(mensaje)
        finally:
            return estado
