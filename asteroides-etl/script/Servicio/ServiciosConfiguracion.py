import xmltodict

from Modelo.Configuracion import Autor, Bot, Api, ConexionDB
from Modelo.Configuracion import Configuracion


class ServiciosConfiguracion:
    def __init__(self):
        self._configuracion = Configuracion()

    @property
    def configuracion(self):
        return self._configuracion

    def cargar(self, servicioslog):
        estado = True
        try:
            mensaje = f"Cargando configuracion..."
            servicioslog.escribir(mensaje)
            with open(self.configuracion.configfile, 'r', encoding='utf8') as xmlfile:
                xmlconfig = xmlfile.read()
                config = xmltodict.parse(xmlconfig)
                autor = Autor(config["parametros"]["bot"]["autor"]["nombre"],
                              config["parametros"]["bot"]["autor"]["correo"])
                bot = Bot(config["parametros"]["bot"]["nombre"],
                          True if config["parametros"]["bot"]["estado"] == 'True' else False,
                          int(config["parametros"]["bot"]["hilos"]), autor)
                self.configuracion.bot = bot
                api = Api(config["parametros"]["conexiones"]["datos_origen"]["url"],
                          config["parametros"]["conexiones"]["datos_origen"]["key"])
                self.configuracion.conexiones.append(api)
                db_conexion = ConexionDB(config["parametros"]["conexiones"]["datos_destino"]["host"],
                                         config["parametros"]["conexiones"]["datos_destino"]["port"],
                                         config["parametros"]["conexiones"]["datos_destino"]["database"],
                                         config["parametros"]["conexiones"]["datos_destino"]["user"],
                                         config["parametros"]["conexiones"]["datos_destino"]["password"],
                                         config["parametros"]["conexiones"]["datos_destino"]["schema"])
                self.configuracion.conexiones.append(db_conexion)

            mensaje = f"Configuracion cargada correctamente..."
            servicioslog.escribir(mensaje)
            mensaje = f"Subproceso finalizado..."
            servicioslog.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Cargando configuracion: {type(excepcion)} - {str(excepcion)}"
            servicioslog.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            servicioslog.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            servicioslog.escribir(mensaje, tiempo=False)
            return estado
