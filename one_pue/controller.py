import time

from one_pue.agents.weather_agent import WeatherAgent
from one_pue.agents.tgbt_agent import TgbtAgent
from one_pue.agents.pdu_agent import PduAgent
from prometheus_client import start_http_server, Gauge


class Controller:
    # partie entiere
    def init_agents(self):
        """Lancement des agents"""
        self.start_prometheus_client()

        weather_agent = WeatherAgent(5, "tgbt_agent", "capteur", "weather")
        weather_gauge = Gauge("exterior_temperature", "Temperature outside the datacenter in C°")
        weather_gauge.set_function(lambda: weather_agent.get_weather_temperature())

        tgbt_agent = TgbtAgent(5, "tgbt_agent", "capteur", "puissance", "192.168.1.83")
        tgbt_gauge = Gauge("global_energy_meter", "Total energy consummed by the datacenter in kWh")
        tgbt_gauge.set_function(lambda: tgbt_agent.get_global_energy_meter())

        pdu_agent = PduAgent(5, "pdu_agent", "capteur", "puissance", "192.168.1.83")
        pdu_gauge = Gauge("energy_consumption", "Total energy consumption by the PDU in kWh")
        pdu_gauge.set_function(lambda: pdu_agent.get_energy_consumption())

    def start_prometheus_client(self):
        """Mise en place d'une communication avec prometheus"""

        server, thread = start_http_server(8000)
        self.prometheus_server = server
        self.prometheus_thread = thread

    def stop_prometheus_client(self):
        self.prometheus_server.shutdown()
        self.prometheus_thread.join()
