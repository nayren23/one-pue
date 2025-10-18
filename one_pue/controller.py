from prometheus_client import start_http_server, Gauge
from one_pue.agents.weather_agent import WeatherAgent
from one_pue.agents.energy_meter_agent import EnergyMeterAgent


class Controller:
    # partie entiere
    def init_agents(self):
        """Lancement des agents"""
        self.start_prometheus_client()

        weather_agent = WeatherAgent("tgbt_agent", "weather")
        weather_gauge = Gauge("exterior_temperature", "Temperature outside the datacenter in C°")
        weather_gauge.set_function(lambda: weather_agent.get_weather_temperature())

        tgbt_agent = EnergyMeterAgent("tgbt_agent", "puissance", "192.168.1.83", 5555, [0x4D83, 0x4D85])
        tgbt_gauge = Gauge("global_energy_meter", "Total energy consummed by the datacenter in kWh")
        tgbt_gauge.set_function(lambda: tgbt_agent.get_global_energy_meter())

        pdu_agent = EnergyMeterAgent("pdu_agent", "puissance", "192.168.1.83", 5556, [0x1000, 0x1002])
        pdu_gauge = Gauge("energy_consumption", "Total energy consumption by the PDU in kWh")
        pdu_gauge.set_function(lambda: pdu_agent.get_global_energy_meter())

        # Jout des autres métriques

    def start_prometheus_client(self):
        """Mise en place d'une communication avec prometheus"""

        server, thread = start_http_server(8000)
        self.prometheus_server = server
        self.prometheus_thread = thread

    def stop_prometheus_client(self):
        self.prometheus_server.shutdown()
        self.prometheus_thread.join()
