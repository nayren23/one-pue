"""Agent Mother Class"""

from pyModbusTCP.client import ModbusClient


class Agent:
    """Classe mère représentant un agent générique (capteur, sonde, etc.)."""

    modbus_client: ModbusClient
    modbus_host: str

    def init_modbus_connection(self, modbus_port):
        """TCP auto connect on first modbus request"""
        return ModbusClient(host=self.modbus_host, port=modbus_port, unit_id=1, auto_open=True)

    # Getter pour modbus_host
    def get_modbus_host(self):
        return self.modbus_host
