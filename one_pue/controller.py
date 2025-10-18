import os
import json
from prometheus_client import start_http_server, Gauge
from one_pue.agents.weather_agent import WeatherAgent
from one_pue.agents.energy_meter_agent import EnergyMeterAgent


class Controller:

    def __init__(self):
        self.gauge_list = []

    # partie entiere
    def init_agents(self):
        """Lancement des agents"""
        agents = self.load_agents()
        for agent in agents:
            self.create_agent_gauge(
                agent["name"],
                agent["description"],
                agent["modbus_host"],
                agent["modbus_port"],
                agent["modbus_register"],
            )
        self.start_prometheus_client()

        weather_agent = WeatherAgent()
        weather_gauge = Gauge("exterior_temperature", "Temperature outside the datacenter in C°")
        weather_gauge.set_function(weather_agent.get_weather_temperature)

        # tgbt_agent = EnergyMeterAgent("172.18.146.98", 5555, [0x4D83, 0x4D85])
        # tgbt_gauge = Gauge("global_energy_meter", "Total energy consummed by the datacenter in kWh")
        # tgbt_gauge.set_function(lambda: tgbt_agent.get_global_energy_meter())

        # pdu_agent = EnergyMeterAgent("172.18.146.98", 5556, [0x1000, 0x1002])
        # pdu_gauge = Gauge("it_energy_meter", "Total energy consumption by the PDU in kWh")
        # pdu_gauge.set_function(lambda: pdu_agent.get_global_energy_meter())

        # groupe_froid_agent = EnergyMeterAgent("172.18.146.98", 5557, [4100, 4102])
        # groupe_froid_gauge = Gauge("group_froid_1_consumption", "Total energy consumption by the  groupe_froid in kWh")
        # groupe_froid_gauge.set_function(groupe_froid_agent.get_global_energy_meter)

    def create_agent_gauge(self, gauge_name, gauge_description, modbus_host, modbus_port, modbus_register):
        print("je pass iciiiii")
        """Crée un agent et un gauge Prometheus associé"""
        tgbt_agent = EnergyMeterAgent(modbus_host, modbus_port, [modbus_register[0], modbus_register[1]])
        tgbt_gauge = Gauge(gauge_name, gauge_description)
        tgbt_gauge.set_function(tgbt_agent.get_global_energy_meter)
        self.gauge_list.append(tgbt_gauge)

    def start_prometheus_client(self):
        """Mise en place d'une communication avec prometheus"""

        server, thread = start_http_server(8000)
        self.prometheus_server = server
        self.prometheus_thread = thread

    def stop_prometheus_client(self):
        self.prometheus_server.shutdown()
        self.prometheus_thread.join()

    def load_agents(self):
        """Lire les agents depuis le fichier JSON."""
        DATA_FILE = "agents.json"

        if not os.path.exists(DATA_FILE):
            return []
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def get_gauge_list(self):
        return self.gauge_list
