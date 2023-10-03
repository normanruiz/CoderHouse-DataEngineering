import json
from datetime import date
import requests


class ServiciosConexionApi:
    def __init__(self, api=None):
        self._api = api

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, api):
        self._api = api

    def consultar(self, servicioslog):
        estado = True
        registros = {}
        try:
            mensaje = f"Consultando API..."
            servicioslog.escribir(mensaje)

            url_start = self.api.url.replace("START_DATE", str(date.today()))
            url_end = url_start.replace("END_DATE", str(date.today()))
            url = url_end.replace("API_KEY", str(self.api.key))
            respuesta = requests.get(url)
            registros = json.loads(respuesta.text)

            mensaje = f"Subproceso finalizado..."
            servicioslog.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Consultando API: {type(excepcion)} - {str(excepcion)}"
            servicioslog.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            servicioslog.escribir(mensaje)
        finally:
            return estado, registros
