"""Agent pour récupérer les données du capteur TGBT"""

import struct as s
from one_pue.agent import Agent


class EnergyMeterAgent(Agent):
    """Classe fille pour récupérer la météo (température horaire)."""

    modbus_port: int
    modbus_register: list

    # Ajouter constructeur pour set tout sauf value
    def __init__(self, name, metric_type, modbus_host, modbus_port, modbus_register):
        """
        name     : nom de l'agent (ex: 'Station Berlin')
        type     : type d'agent (ex: 'Weather Agent')
        metric_type     : Type métrique (ex: 'Puissance')
        time     : heure associée (string 'HH:MM:SS' ou ISO)
        latitude/longitude : position utilisée pour l'appel API
        """
        super().__init__(name, metric_type)
        self.modbus_host = modbus_host
        self.modbus_port = modbus_port
        self.modbus_register = modbus_register

    def get_global_energy_meter(self):
        """Récupération de l'energie globale grace au modbus"""
        self.modbus_client = self.init_modbus_connection(self.modbus_port)  # intialisation connexion
        first_regs = self.modbus_client.read_holding_registers(self.modbus_register[0], 2)
        second_regs = self.modbus_client.read_holding_registers(self.modbus_register[1], 1)
        value = self.format_value_modbus(first_regs, second_regs)
        if first_regs and second_regs:
            return value
        else:
            print("read error")

    def format_value_modbus(self, first_regs, second_regs):
        """Format de la valeur récupérer via modbus poru la mettre dans le bon format"""
        return s.unpack(">I", s.pack(">HH", *first_regs))[0] + second_regs[0] / 10000
