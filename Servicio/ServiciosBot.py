from Modelo.Bot import Bot
from Servicio.ServiciosConfiguracion import ServiciosConfiguracion
from Servicio.ServiciosETL import ServiciosETL
from Servicio.ServiciosLog import ServiciosLog


class ServiciosBot:
    def __init__(self):
        self._bot = Bot()

    @property
    def bot(self):
        return self._bot

    @bot.setter
    def bot(self, bot):
        self._bot = bot

    def iniciar(self):
        servicioslog = None
        try:
            servicioslog = ServiciosLog()
            self.bot.estado = servicioslog.verificar_archivo_log()
            if self.bot.estado is False:
                return
            mensaje = f" {'='*128 }"
            servicioslog.escribir(mensaje, tiempo=False)
            mensaje = f"Iniciando Bot CoderHouse Data Engineering..."
            servicioslog.escribir(mensaje)
            mensaje = f" {'~'*128 }"
            servicioslog.escribir(mensaje, tiempo=False)

            serviciosconfiguracion = ServiciosConfiguracion()
            self.bot.estado = serviciosconfiguracion.cargar(servicioslog)
            if self.bot.estado is False:
                return
            self.bot.estado = serviciosconfiguracion.configuracion.bot.estado
            if self.bot.estado is False:
                mensaje = f"Bot apagado por configuracion..."
                servicioslog.escribir(mensaje)
                return

            serviciosetl = ServiciosETL()
            self.bot.estado = serviciosetl.extract(servicioslog, serviciosconfiguracion.configuracion.conexiones[0])
            if self.bot.estado is False:
                return

        except Exception as excepcion:
            self.bot.estado = False
            mensaje = f" {'-'*128 }"
            servicioslog.escribir(mensaje, tiempo=False)
            mensaje = f"ERROR - Ejecucion principal: {type(excepcion)} - {str(excepcion)}"
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
