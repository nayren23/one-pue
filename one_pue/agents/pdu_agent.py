"""Agent pour récupérer les données du capteur PDU"""

# weather_agent.py
from one_pue.agent import Agent


class PduAgent(Agent):
    """Classe fille pour récupérer les infos du PDU"""

    # Ajouter constructeur pour set tout sauf value
    def __init__(self, interval, name, agent_type, metric_type, modbus_host):
        """
        interval : intervalle de mise à jour (s ou min)
        name     : nom de l'agent (ex: 'Station Berlin')
        type     : type d'agent (ex: 'Weather Agent')
        metric_type     : Type métrique (ex: 'Puissance')
        time     : heure associée (string 'HH:MM:SS' ou ISO)
        latitude/longitude : position utilisée pour l'appel API
        """
        super().__init__(interval, name, agent_type, metric_type)
        self.modbus_host = modbus_host

    def get_energy_consumption(self):
        """Récupération de l'energie globale grace au modbus"""
        self.modbus_client = self.init_modbus_connection(5556)  # intialisation connexion
        first_regs = self.modbus_client.read_holding_registers(0x1000, 2)
        second_regs = self.modbus_client.read_holding_registers(0x1002, 1)
        value = self.format_value_modbus(first_regs, second_regs)
        if first_regs and second_regs:
            return value
        else:
            print("read error")
