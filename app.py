from Modelo.Bot import Bot
from Servicio.ServiciosBot import ServiciosBot

bot = Bot()
servicios_bot = ServiciosBot(bot)
servicios_bot.iniciar()
