from Modelo.Log import Log
from Servicio.ServiciosLog import ServiciosLog


class ServiciosBot:
    def __init__(self, bot):
        self._bot = bot

    @property
    def bot(self):
        return self._bot

    @bot.setter
    def bot(self, bot):
        self._bot = bot

    def iniciar(self):
        servicioslog = None
        try:
            log = Log()
            servicioslog = ServiciosLog(log)
            self.bot.estado = servicioslog.verificar_archivo_log()
            if self.bot.estado is False:
                return
            mensaje = f" {'='*128 }"
            servicioslog.escribir(mensaje, tiempo=False)
            mensaje = f"Iniciando Bot CoderHouse Data Engineering..."
            servicioslog.escribir(mensaje)
            mensaje = f" {'~'*128 }"
            servicioslog.escribir(mensaje, tiempo=False)

        except Exception as excepcion:
            self.bot.estado = False
            mensaje = f" {'-'*128 }"
            servicioslog.escribir(mensaje, tiempo=False)
            mensaje = f"ERROR - Ejecucion principal: {str(excepcion)}"
            servicioslog.escribir(mensaje)
        finally:
            if not self.bot.estado:
                mensaje = f" {'-' * 128}"
                servicioslog.escribir(mensaje, tiempo=False)
                mensaje = f"WARNING!!! - Proceso principal interrumpido, no se realizaran mas acciones..."
                servicioslog.escribir(mensaje)

            mensaje = f" {'~' * 128}"
            servicioslog.escribir(mensaje, tiempo=False)
            mensaje = f"Finalizando Bot CoderHouse Data Engineering..."
            servicioslog.escribir(mensaje)
            mensaje = f" {'='*128 }"
            servicioslog.escribir(mensaje, tiempo=False)
            return 0 if self.bot.estado else 1
