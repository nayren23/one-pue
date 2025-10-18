"""Agent pour récupérer les données du capteur TGBT"""

import struct as s
from one_pue.agent import Agent


class EnergyMeterAgent(Agent):
    """Classe fille pour récupérer la météo (température horaire)."""

    modbus_port: int
    modbus_register: list

    # Ajouter constructeur pour set tout sauf value
    def __init__(self, modbus_host, modbus_port, modbus_register):
        """ """
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
        print("Affichage regs")
        print(first_regs)
        print(second_regs)
        return s.unpack(">I", s.pack(">HH", *first_regs))[0] + second_regs[0] / 10000

    # Getter pour modbus_port
    def get_modbus_port(self):
        return self.modbus_port

    # Getter pour modbus_register
    def get_modbus_register(self):
        return self.modbus_register
