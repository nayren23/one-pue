"""Agent pour récupérer les données du capteur TGBT"""

# weather_agent.py
from pyModbusTCP.client import ModbusClient
import struct as s
from one_pue.agent import Agent
from one_pue.agent_dto import AgentDTO


class TgbtAgent(Agent):
    """Classe fille pour récupérer la météo (température horaire)."""

    modbus_client: ModbusClient
    modbus_host: str
    modbus_adress: int
    modbus_port: int

    # Ajouter constructeur pour set tout sauf value
    def __init__(self, interval, name, agent_type, metric_type, modbus_host, modbus_adress, modbus_port):
        """
        interval : intervalle de mise à jour (s ou min)
        name     : nom de l'agent (ex: 'Station Berlin')
        type     : type d'agent (ex: 'Weather Agent')
        metric_type     : Type métrique (ex: 'Puissance')
        time     : heure associée (string 'HH:MM:SS' ou ISO)
        latitude/longitude : position utilisée pour l'appel API
        """
        super().__init__(interval, name, agent_type, metric_type)
        self.modbus_port = modbus_port
        self.modbus_host = modbus_host
        self.modbus_adress = modbus_adress

        self.modbus_client = self.init_modbus_connection()  # intialisation connexion

    def init_modbus_connection(self):
        """TCP auto connect on first modbus request"""

        return ModbusClient(host=self.modbus_host, port=self.modbus_port, unit_id=1, auto_open=True)

    def get_data(self):
        """Lecture de 2 registres de 16 bits à l'adresse Modbus 0 :"""
        regs = self.modbus_client.read_holding_registers(self.modbus_adress, 2)
        regs2 = self.modbus_client.read_holding_registers(0x1002, 1)  # 0x4D85

        value = s.unpack(">I", s.pack(">HH", *regs))[0] + regs2[0] / 10000
        print(value)
        if regs:
            return value
        else:
            print("read error")
